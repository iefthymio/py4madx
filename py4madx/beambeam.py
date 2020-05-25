#
# --- BeamBeam Functions for LHC studies
#
# (c) I.E - September 2019
#
# MADX scripts to run with cpymad 
#
# Entry functions:
#   - define_BB_elements
#           - define_BBho_ip, define_BBlr_ip
#       returns DF with the basic parameters of each bb element
#       bbeldf : elname(index), spos, charge, ip, type(ho/lr)
#
#   - define_BB_lenses
#           - install_BB_markers
#           - survey_BB_markers
#           - calculate_BB_lenses
#           - init_BB_lenses
#           - install_BB_lenses
#           - enable_BB_lenses
#           - update_BB_lenses
#       installs the defined BB elements in both beams
#       returns DFs with twiss, tsumm, bblens and survey data
#

Version = '2.00 - (ie) 18.05.2020'

import os
import shutil
import numpy as np
import pandas as pd
import subprocess
import re
import itertools

import py4madx
from py4madx import pmadx
from py4madx import qslice


ipside = {-1:'l', 1:'r', 0:''}

# ------- Elements ---------------------

def define_BB_elements(bbho={'ip1':0,'ip2':0,'ip5':0,'ip8':0},
                       bblr={'ip1':[],'ip2':[],'ip5':[],'ip8':[]},
                       sigmaz=1.0,
                       lrsdist=26658.8832/35640*5):
    ''' Define BB elements - name = [ho/lr]ipX[l/r/'']_n'''
    lbbeldf = []
    _tmp = pd.DataFrame()
    lbbeldf.append(_tmp)  
    for ip in bbho:
        if bbho[ip] == 0 :
            continue
        _hodf = define_BBho_ip(ip, bbho[ip], sigmaz)
        lbbeldf.append(_hodf)

    for ip in bblr:
        if bblr[ip] == 0 :
            continue
        _lrdf = define_BBlr_ip(ip, bblr[ip], lrsdist)
        lbbeldf.append(_lrdf)
    _tmp = pd.concat(lbbeldf, sort=False)
    _tmp.set_index('elname', drop=False, inplace=True)
    return _tmp

def define_BBho_ip(ip, nho, sigma):
    _aux = qslice.qslice(qtot=1.0, sigma=sigma, nslices=nho)
    _aux['elname'] = 'ho'+_aux['id'].apply(lambda j: ip.lower()+ipside[np.sign(j)]+'_'+str(np.abs(j)))
    _aux['ip'] = ip.lower()
    _aux['type'] = 'ho'
    return _aux

def define_BBlr_ip(ip, bblr, sep):
    spos = [sep*x for x in bblr]
    chrg = np.ones(len(bblr))
    eln = [*['lr'+ip.lower()+'l_'+str(np.abs(j)) for j in bblr if j < 0], 
           *['lr'+ip.lower()+'r_'+str(np.abs(j)) for j in bblr if j > 0]]
    elip = [ip.lower()]*len(bblr)
    _aux = pd.DataFrame({'spos':spos,'charge':chrg,'id':bblr, 'elname':eln, 'ip':elip})
    _aux['type'] = 'lr'
    return _aux

# ------- Markers -----------------------

def install_BB_markers(mmad, bbeldf, lbeam, clean=False):
    ''' define BB markers per beam - name : 'bbmk_[ho/lr]ipX[l//r/'']bY.n '''
    bm = lbeam.replace('lhc','')
   
    if clean :
        pmadx.removeElementsFromSeq(mmad, lbeam, 'bbmarker', f'bbmk_')
    bbmrkdf = bbeldf.copy()
    bbmrkdf['elname'] = bbmrkdf.elname.apply(lambda x : 'bbmk_'+x.replace('_',bm+'.'))
    bbmrkdf['beam'] = lbeam

    cmd = [f'install element={row.elname}, class=bbmarker, at={row.spos}, from={row.ip};' for i,row in bbmrkdf.iterrows()]
    _instcmd = '\n'.join(cmd)
    mmad.input(f'''
    option, warn, info;
    bbmarker : marker;
    seqedit, sequence={lbeam};
        {_instcmd}
        flatten;
    endedit;
    option, -warn, -info;
    ''')
    assert bbeldf.shape[0] == pmadx.countElementsInSeq(mmad, 'bbmk', lbeam), \
        f' {lbeam}: Number of installed bb markers  does not match that of bbel '
    return bbmrkdf

# ------- Survey -----------------------

def survey_BB_markers(mmad, ips):
    _dflist = []
    xoffset = {'ip1':-0.097, 'ip2':0.097, 'ip5':-0.097, 'ip8':0.097}
    for lbeam, ip in itertools.product(['lhcb1', 'lhcb2'], ips):
        _dflist.append(survey_BB_markersIP(mmad, ip, xoffset[ip], lbeam))
    return pd.concat(_dflist)  

def survey_BB_markersIP(mmad, ip, x0, lbeam):
    suir = 'su'+ip.replace('p','r')+lbeam[-2:]
    ipn = int(ip.replace('ip',''))
    if lbeam == 'lhcb2' :
        x0 = -1.0*x0
    mmad.input(f'''
    delete,table={suir};
    select,flag=survey,clear;
    select,flag=survey,class=bbmarker;
    use,sequence={lbeam},range=e.ds.l{ipn}.{lbeam[-2:]}/s.ds.r{ipn}.{lbeam[-2:]};
    survey,x0={x0},file=surveyaux.tfs;
    readmytable,file=surveyaux.tfs,table={suir};
    ''')
    _aux = pmadx.twiss2df(mmad.table[suir])
    _aux['beam'] = lbeam
    return _aux

def calculate_x_su(bbeldf, survdf):
    survb1 = survdf[survdf['beam'] == 'lhcb1']
    survb2 = survdf[survdf['beam'] == 'lhcb2']
        
    namho0b1 = 'bbmk_ho'+ipn+'b1.0'
    namho0b2 = 'bbmk_ho'+ipn+'b2.0'

    x_su = (survb2.loc[namb2].x - survb1.loc[namb1].x) - (survb2.loc[namho0b2].x - survb1.loc[namho0b1].x)
    return x_su

# ------- Lenses -----------------------

def define_BB_lenses(mmad, bbeldf, option='LAST'):
 
    ipsbb = np.unique(bbeldf.ip.values)
    
    ltwiss = []
    ltsumm = []
    lbblen = []

    bbmrkb1 = install_BB_markers(mmad, bbeldf, 'lhcb1', clean=True)
    bbmrkb2 = install_BB_markers(mmad, bbeldf, 'lhcb2', clean=True)
    
    mmad.input(f'''
    select,flag=twiss,clear;
    select,flag=twiss,class=bbmarker,      column=name,x,y,px,py,betx,bety,sig11,sig12,sig22,sig33,sig34,sig44,sig13,sig14,sig23,sig24;
    select,flag=twiss,pattern="IP[12358]$",column=name,x,y,px,py,betx,bety,sig11,sig12,sig22,sig33,sig34,sig44,sig13,sig14,sig23,sig24;
    use,sequence=lhcb1;twiss,file="temp/twissb1_bb0.tfs";
    !readmytable,file="temp/twissb1_bb0.tfs",table=twissb1;
    use,sequence=lhcb2;twiss,file="temp/twissb2_bb0.tfs";
    !readmytable,file="temp/twissb2_bb0.tfs",table=twissb2;
    ''')
    twissb1_0, tsummb1_0 = pmadx.tfs2df('temp/twissb1_bb0.tfs')
    twissb2_0, tsummb2_0 = pmadx.tfs2df('temp/twissb2_bb0.tfs') 
    # twiss0, tsumm0 = pmadx.twissLHC(mmad, selection=re.compile('|'.join(['^ip[12358]','^bbmk_'])), fout='')
    twiss0 = pd.concat([twissb1_0, twissb2_0])
    tsumm0 = pd.concat([tsummb1_0, tsummb2_0])
    twiss0['iter'] = -1
    tsumm0['iter'] = -1
    ltwiss.append(twiss0)
    ltsumm.append(tsumm0)
    twiss0.to_pickle('twissbb0.pkl')
    tsumm0.to_pickle('tsummbb0.pkl')

    survdf = survey_BB_markers(mmad, ipsbb)
    survdf.to_pickle('survdbb0.pkl')

    bblensb1 = calculate_BB_lenses(mmad, bbeldf, 'lhcb1', 'lhcb2', twiss0, tsumm0, survdf)
    bblensb2 = calculate_BB_lenses(mmad, bbeldf, 'lhcb2', 'lhcb1', twiss0, tsumm0, survdf)
    bblens = pd.concat([bblensb1, bblensb2])
    bblens['iter'] = -1
    lbblen.append(bblens)
    bblens.to_pickle('bblens0.pkl')

    madxbbelb1 = init_BB_lenses(mmad, bblensb1)
    madxbbelb2 = init_BB_lenses(mmad, bblensb2)
    
    install_BB_lenses(mmad, madxbbelb1, 'lhcb1')
    install_BB_lenses(mmad, madxbbelb2, 'lhcb2')
    assert bbeldf.shape[0] == pmadx.countElementsInSeq(mmad, 'bb_', 'lhcb1'), \
        f' lhcb1: Number of installed bb markers  does not match that of bbel' 
    assert bbeldf.shape[0] == pmadx.countElementsInSeq(mmad, 'bb_', 'lhcb2'), \
        f' lhcb1: Number of installed bb markers  does not match that of bbel' 

    ips0, xip0, yip0 = pmadx.getLHCBeamPosAtIP(twiss0)
    np.set_printoptions(formatter={'float': '{: 12.5g}'.format})
    [print(f'{ip} : x = {x} --> sep0_x = {np.diff(x)} y={y} -->sep0_y = {np.diff(y)}') for ip,x,y in zip(ips0,xip0,yip0)]

    mmad.globals.on_bb_charge = 1

    enable_BB_lenses(mmad, np.unique(bblensb1['qflag'].values))
    enable_BB_lenses(mmad, np.unique(bblensb2['qflag'].values))

    delta = 1.0e14
    j = 1
    while delta > 1.0e-14:
        print(f'\n>>>> loop [{j}]\n')
        
        mmad.input(f'''
        select,flag=twiss,clear;
        select,flag=twiss,class=bbmarker,      column=name,x,y,px,py,betx,bety,sig11,sig12,sig22,sig33,sig34,sig44,sig13,sig14,sig23,sig24;
        select,flag=twiss,pattern="IP[12358]$",column=name,x,y,px,py,betx,bety,sig11,sig12,sig22,sig33,sig34,sig44,sig13,sig14,sig23,sig24;
        use,sequence=lhcb1;twiss,file="temp/twissb1_bb{j}.tfs";
        !readmytable,file="temp/twissb1_bb{j}.tfs",table=twissb1;
        use,sequence=lhcb2;twiss,file="temp/twissb2_bb{j}.tfs";
        !readmytable,file="temp/twissb2_bb{j}.tfs",table=twissb2;
        ''')
        twissb1_j, tsummb1_j = pmadx.tfs2df(f'temp/twissb1_bb{j}.tfs')
        twissb2_j, tsummb2_j = pmadx.tfs2df(f'temp/twissb2_bb{j}.tfs')
        twiss_j = pd.concat([twissb1_j, twissb2_j])
        tsumm_j = pd.concat([tsummb1_j, tsummb2_j])
        #twiss_j, tsumm_j = pmadx.twissLHC(mmad, selection=re.compile('|'.join(['^ip[12358]','^bbmk_','^bb_'])), fout='')
        twiss_j['iter'] = j
        tsumm_j['iter'] = j
        twiss_j.to_pickle(f'twissbb_{j}.pkl')
        tsumm_j.to_pickle(f'tsummbb_{j}.pkl')

        bblensb1_j = calculate_BB_lenses(mmad, bbeldf, 'lhcb1', 'lhcb2', twiss0, tsumm0, survdf)
        bblensb2_j = calculate_BB_lenses(mmad, bbeldf, 'lhcb2', 'lhcb1', twiss0, tsumm0, survdf)
        bblens_j = pd.concat([bblensb1_j, bblensb2_j])
        bblens_j['iter'] = j
        bblens_j.to_pickle(f'bblens_{j}.pkl')

        update_BB_lenses(mmad, bblensb1_j)
        update_BB_lenses(mmad, bblensb2_j)

        ips, xip, yip = pmadx.getLHCBeamPosAtIP(twiss_j)
        [print(f'{i} : x = {x} --> sep0_x = {np.diff(x)} y={y} -->sep0_y = {np.diff(y)}') for i,x,y in zip(ips,xip,yip)]
        
        if option == 'ALL' :
            lbblen.append(bblens_j)
            ltwiss.append(twiss_j)
            ltsumm.append(tsumm_j)

        delta_x = np.asarray(xip).ravel() - np.asarray(xip0).ravel()
        delta_y = np.asarray(yip).ravel() - np.asarray(yip0).ravel()
        delta = np.dot(delta_x, delta_x) + np.dot(delta_y, delta_y)
        
        xip0 = xip
        yip0 = yip
        j += 1

    print(f'\t - convergence reached after {j} iterrations')
    pmadx.removeElementsFromSeq(mmad, 'lhcb1', 'bbmarker', 'bbmk_')
    pmadx.removeElementsFromSeq(mmad, 'lhcb2', 'bbmarker', 'bbmk_')
    
    if option == 'LAST':
        ltwiss.append(twiss_j)
        ltsumn.append(tsumm_j)
        lbblen.append(bblens_j)

    return pd.concat(ltwiss), pd.concat(ltsumm), pd.concat(lbblen), survdf

def calculate_BB_lenses(mmad, bbeldf, lbeamw, lbeams, twissdf, tsummdf, survdf):

    bnw = lbeamw.replace('lhc','')
    bns = lbeams.replace('lhc','')

    twissw = twissdf[twissdf['beam'] == lbeamw]
    twisss = twissdf[twissdf['beam'] == lbeams]
    tsummw = tsummdf.loc[lbeamw]
    tsumms = tsummdf.loc[lbeams]

    egxw = tsummw.ex
    egyw = tsummw.ey
    egxs = tsumms.ex
    egys = tsumms.ey

    bblensdf = bbeldf.copy()
    bblensdf['namew'] = bblensdf.elname.apply(lambda x : x.replace('_',bnw+'.'))
    bblensdf['markerw'] = bblensdf.elname.apply(lambda x : 'bbmk_'+x.replace('_',bnw+'.'))
    bblensdf['markers'] = bblensdf.elname.apply(lambda x : 'bbmk_'+x.replace('_',bns+'.'))
    bblensdf['lens'] = bblensdf.markerw.apply(lambda x : x.replace('bbmk_','bb_'))

    bblensdf['sigx'] = bblensdf.markers.apply(lambda x : np.sqrt(egxs*twisss.loc[x].betx))
    bblensdf['sigy'] = bblensdf.markers.apply(lambda x : np.sqrt(egys*twisss.loc[x].bety))

    def x_su(elname, ip, survdf):
        survb1 = survdf[survdf['beam'] == 'lhcb1']
        survb2 = survdf[survdf['beam'] == 'lhcb2']
            
        namho0b1 = 'bbmk_ho'+ip+'b1.0'
        namho0b2 = 'bbmk_ho'+ip+'b2.0'
        namb1 = 'bbmk_'+elname.replace('_','b1.')
        namb2 = 'bbmk_'+elname.replace('_','b2.')

        x_su = (survb2.loc[namb2].x - survb1.loc[namb1].x) - (survb2.loc[namho0b2].x - survb1.loc[namho0b1].x)
        return x_su

    bblensdf['x_su'] = bblensdf.apply(lambda row: x_su(row['elname'], row['ip'], survdf), axis=1)
    if lbeamw == 'lhcb1' :
        bblensdf['xma'] = bblensdf.apply(lambda row: twisss.loc[row['markers']].x + row['x_su'], axis=1)
    else:
        bblensdf['xma'] = bblensdf.apply(lambda row: twisss.loc[row['markers']].x - row['x_su'], axis=1)
    bblensdf['yma'] = bblensdf.markers.apply(lambda x : twissdf.loc[x].y)
    bblensdf['lbeamw'] = lbeamw
    bblensdf['lbeams'] = lbeams

    def onqflag(ip, bbtype, id):
        if bbtype == 'lr':
            return 'ON_BB_Q'+(bbtype+ip+ipside[np.sign(id)]).upper()
        else:
            return 'ON_BB_Q'+(bbtype+ip).upper()
    bblensdf['qflag'] = bblensdf.apply(lambda row : onqflag(row['ip'], row['type'], row['id']), axis=1)
    return bblensdf

def init_BB_lenses(mmad, bblensdf):
    
    bblpar = []
    bbldef = []
    bblins = []
    qflags = []
    
    for i, row in bblensdf.iterrows(): 
        qbb = row.charge
        qflags.append(f'{row.qflag}')
        bblpar.append(f'''sigx_{row.namew} = {row.sigx:<15.8g}; sigy_{row.namew} = {row.sigy:<15.8g}; xma_{row.namew} = {row.xma:<15.8g}; yma_{row.namew} = {row.yma:<15.8g};''')
        # bbldef.append(f'''bb_{_name}: beambeam, charge:={qbb}*{_qflag}, sigx:=sigx_{_name}, sigy:=sigy_{_name}, xma:=xma_{_name}, yma:=yma_{_name}, bbshape=1, bbdir=-1;''')
        bbldef.append(f'''bb_{row.namew}: beambeam, charge:={qbb}*{row.qflag}, sigx:=sigx_{row.namew}, sigy:=sigy_{row.namew}, xma:=xma_{row.namew}, yma:=yma_{row.namew}, bbshape=1, bbdir=-1;''')
        bblins.append(f'''install, element=bb_{row.namew},at={row.spos},from={row.ip};''')

    bblenses = {}
    bblenses['elpar'] = bblpar
    bblenses['eldef'] = bbldef
    bblenses['elins'] = bblins
    bblenses['qflag'] = qflags
    return bblenses

def disable_BB_lenses(mmad, qflags):

    _qval = [f'{q}=0;' for q in qflags]
    _mcmd = '\n'.join(_qval)
    mmad.input(f'''
    option, warn, info;
    {_mcmd}
    option, -warn, -info;
    ''')
    return

def enable_BB_lenses(mmad, qflags):

    _qval = [f'{q}=1;' for q in qflags]
    _mcmd = '\n'.join(_qval)
    mmad.input(f'''
    option, warn, info;
    {_mcmd}
    option, -warn, -info;
    ''')
    return

def install_BB_lenses(mmad, madxbbel, lbeam):

    _cmd_bbldef = '\n'.join(madxbbel['elpar'])
    _cmd_bblele = '\n'.join(madxbbel['eldef'])
    _cmd_bblins = '\n'.join(madxbbel['elins'])
    qflags0 = [ f'{x} = 0;' for x in madxbbel['qflag']]
    _cmd_qfzero = '\n'.join(qflags0)
    mmad.input(f'''
    option, echo, warn, info;
    {_cmd_qfzero}
    {_cmd_bbldef}
    {_cmd_bblele}
    seqedit, sequence={lbeam};
    flatten;
    {_cmd_bblins}
    flatten;
    endedit;
    option, -echo, -warn, -info;
    ''')
    return

def update_BB_lenses(mmad, bblensdf):
    bblpar = []
    for i, row in bblensdf.iterrows(): 
        bblpar.append(f'''sigx_{_row.namew} = {row.sigx:<15.8g}; sigy_{row.namew} = {row.sigy:<15.8g}; xma_{row.namew} = {row.xma:<15.8g}; yma_{row.namew} = {row.yma:<15.8g};''')

    _cmd_bblpar = '\n'.join(bblpar)
    mmad.input(f'''
    option, echo, warn, info;
    {_cmd_bblpar}
    option, -echo, -warn, -info;
    ''')
    return

# ------- Prepare SixTrack -----------------------

def sixtrack_Input_BBLenses(mmad, btwdf, lbeam, ibeco=1, ibtyp=0, lhc=2, ibbc=0):
    ''' Generate the SixTrack Input for the bblens and lbeam
        for the keywrds look at http://sixtrack.web.cern.ch/SixTrack/docs/user_full/manual.php#Ch6.S6

        Save the data to the bb_lenses.dat file in the current directory. 
    '''
    fout = open('bb_lenses.dat','w')
    bblock = []
    beam = mmad.sequence[lbeam].beam
    b_part = beam.npart
    b_exn = beam.exn*1e6
    b_eyn = beam.eyn*1e6
    b_sigt = beam.sigt
    b_sige = beam.sige
    bblock_head = f'''BEAM\nEXPERT\n  {b_part:7.3e} {b_exn:15.9f} {b_eyn:15.9f} {b_sigt:15.9f} {b_sige:15.9f} {ibeco:1d} {ibtyp:1d} {lhc:1d} {ibbc:1d}\n'''
    bblock.append(bblock_head)
    fout.write(bblock_head)

    # --- use the twiss of the two beams to calculate the BB lense parameters
    sbeam = 'lhcb2' if lbeam == 'lhcb1' else 'lhcb1'
    for i, row in btwdf[btwdf['beam'] == lbeam].iterrows():
        name = row['name'].split(':')[0]
        bbname = name.split('.')[1]
        print ('>> bb element in twiss = {}, basename = {}'.format(name, bbname))
        _tb2 = btwdf[(btwdf['beam'] == sbeam) & (btwdf['name'].str.find(bbname)> 0)]
        ox = (_tb2.x[0] - row['x'])*1e3
        oy = (_tb2.y[0] - row['y'])*1e3
        if ( (ox > 0) and (ox < 1e-7)) : ox = 1e-7  # -- this to avoid numberical instabilities in SixTrack
        if ( (oy > 0) and (oy < 1e-7)) : oy = 1e-7

        pxb1 = row['px']; pxb2 = _tb2.px[0]
        pyb1 = row['py']; pyb2 = _tb2.py[0]
        dlt_px = pxb1 - pxb2
        dlt_py = pyb1 - pyb2
        xang = 0.5*np.sqrt(dlt_px**2+dlt_py**2)
        if dlt_px == 0 :
            xplane = np.pi/2
        else:
            xplane = np.arctan(dlt_py/dlt_px)
        h_sep = -ox
        v_sep = -oy
        s_xx    = _tb2.sig11[0]*1e6
        s_xxp   = _tb2.sig12[0]*1e6
        s_xpxp  = _tb2.sig22[0]*1e6
        s_yy    = _tb2.sig33[0]*1e6
        s_yyp   = _tb2.sig34[0]*1e6
        s_ypyp  = _tb2.sig44[0]*1e6
        s_xy    = _tb2.sig13[0]*1e6
        s_xyp   = _tb2.sig14[0]*1e6
        s_xpy   = _tb2.sig23[0]*1e6
        s_xpyp  = _tb2.sig24[0]*1e6
        s_ratio = 1/15
        ibsix   = 1

        bblock_el = f'''{name:20s} {ibsix:2d} {xang:13.10g} {xplane:13.10g} {h_sep:15.9f} {v_sep:15.9f}\n'''
        fout.write(bblock_el)
        bblock.append(bblock_el)
        bblock_el = f'''  {s_xx:13.10g} {s_xxp:13.10g} {s_xpxp:13.10g} {s_yy:13.10g} {s_yyp:13.10g}\n'''
        fout.write(bblock_el)
        bblock.append(bblock_el)
        bblock_el = f'''  {s_ypyp:13.10g} {s_xy:13.10g} {s_xyp:13.10g} {s_xpy:13.10g} {s_xpyp:13.10g} {s_ratio:13.10g}\n'''
        fout.write(bblock_el)
        bblock.append(bblock_el)
    fout.close()
    print(bblock)
    return

def sixtrack_Save_BBLenses(bblock,fout):
    ''' Save the SixTrack Format BB lenses data to a file '''
    f = open(fout,'w')
    for txt in bblock:
        f.write(txt)
    f.close()
    return

def sixtrack_Update_BbeamSElementDef():
    ''' Update the single element definition to use the BEAM EXPERT block data'''
    # os.rename(r'fc.2',r'fc.2.original')
    shutil.copy2('fc.2','fc.2.original')
    import subprocess
    subprocess.call(["sed","-r","-i",'s/ 20 .+/ 20 0.0 0.0 0.0 0.0 0.0 0.0/g',"fc.2"])
    # subprocess.call(["sed -r -i 's/ 20 .+/ 20  10.0 20.0 30.0 40.0 50.0 60.0/g' fc.2"], shell=True)
    return