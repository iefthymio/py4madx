#
# --- BeamBeam Functions for cpymad
#
# (c) I.E - September 2019
#
# MADX scripts to run with cpymad
#
#

import os
import shutil
import numpy as np
import pandas as pd
import subprocess
import re

import matplotlib
import matplotlib.patches as patches
import matplotlib.dates as md
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.tri import Triangulation
from matplotlib.patches import Polygon
from scipy import special

import py4madx
pmadx = py4madx.py4madx

def fnorm(x):
    ''' normal function with zero mean and sigma=1 '''
    return np.exp(-0.5*x*x)/np.sqrt(2*np.pi)

def myerf(x): # --- Normal distribution integral (half range [0,inf]) with u=0, sigma=1
    return 0.5*special.erf(x/np.sqrt(2)) 

def arcerf(y): # --- Inverse error function of normal distribution (Quantile function)
    return np.sqrt(2)*special.erfinv(2*y)

def bari(y1, y2):
    x1 = arcerf(y1)
    x2 = arcerf(y2)
    bari = np.abs(fnorm(x2)-fnorm(x1))/(y2-y1)
    return bari

def qslice(n):
    '''
        slice the z-distribuiton to equal charge N slices
        returns DF with s positions and charge wrt center
    '''
    Nmax = 100
    if n > Nmax :
        print ('>>> slice : too many slices requested - reduced to 100')
        n = 100
    if n < 0 :
        print ('>>> slice : n must be a positive number ! - set to 0')

    spos = []
    charge = []
    scharge = 1.0/(2*n+1)       # -- equal charge per slice + central bin
    y1 = 0.5*scharge
    y2 = y1 + scharge
    for i in range(1,n):
        spos.append(bari(y1,y2))
        y1 = y2
        y2 = y2 + scharge
        charge.append(scharge)
    x = arcerf(y1)
    # spos.append(np.exp(-0.5*x*x)/scharge/ractwopi)
    spos.append(fnorm(x)/scharge)
    charge.append(scharge)

    df = pd.DataFrame()
    df['spos'] = spos
    df['charge'] = charge
    return df

def calculateXScheme(twdf, halo, ip):
    ''' Calculate on_sep value to assure the correct hallo collisions in the non-xsing plane of ip'''
    return

def define_BB_el(bbconfig):
    '''
        Prepare the BB configuration
        Input :
            bbconf    : dictionary with IPs and number of HO collisions to consider
                        if > 1, 2n+1 lenses are created spaced around the IP on equal charge distances.
                        The central lens is at 1.0e-9 distance from IP
        Returns:
            bbdf      : dataframe with BB interactions for the ip
                        columns : [ip, name, spos, charge]
                        The name of the BB element is = ip{x}{l/r}_ho_{n}
                        Empty DF if no HO defined.
    '''
    bbdfl = []
    for ip in bbconfig:
        nho = bbconfig[ip]
        print ('>>> define_BB_el: nHO={} slices defined for {}'.format(nho,ip))
        if nho == 0 :
            continue
        elif nho % 2 == 0 :
            continue
        elif nho == 1 :
            elname = ip.lower()+'ho_0'
            _aux = pd.DataFrame({'ip':ip,'name':elname,'spos':[1.0e-9],'charge':1.0})
            bbdfl.append(_aux)
        elif (nho > 1) & (nho % 2 == 1) :
            nsl = int(nho/2)
            _sldf = qslice(nsl)
            spos = _sldf.spos.values
            chrg = _sldf.charge.values
            eln = [ip.lower()+'ho_0',*[ip.lower()+'rho_'+str(j+1) for j in _sldf.index],*[ip.lower()+'lho_'+str(j+1) for j in _sldf.index]]
            els = [1.0e-9, *spos, *-spos]
            elch = [1.0/(2*nsl+1), *chrg, *chrg]
            elip = [ip.lower()]*len(els)
            _aux = pd.DataFrame({'ip':elip,'name':eln,'spos':els,'charge':elch})
            bbdfl.append(_aux)
    if len(bbdfl) > 0 :
        bbdf = pd.concat(bbdfl,sort=True)
        bbdf = bbdf.reset_index(drop=True)
    else:
        print ('>>> define_BB_el : no elements defined! Return empty df')
        bbdf = pd.DataFrame()
    return bbdf

def install_BB_mark(mmad, bbdf, lbeam):
    '''
        Install BB markers in all IPs for the selected beam
        BB marker names : bbmrk_b{beam}.ip{ip}{l/r}_ho_{n}
    '''
    ips = np.unique(bbdf.ip.values)
    logger.info('Install_BB_mark: for beam {} and IPs {}'.format(lbeam,ips))
    
    bm = lbeam.replace('lhc','')
    bdef = mmad.sequence[lbeam].beam
    sigz = bdef.sigt
    print('Scale Spositions by sigz/2 = {} except the central one!'.format(sigz/2))
    bbdf['spos'] = bbdf.apply(lambda row : row['spos']*sigz/2 if row['name'].find('_0')<0 else row['spos'], axis=1)
    # incmd = [f'''install element=bbmrk_b1.{name}, class=bbmarker, at={spos}, from={ip};''' for name,spos,ip in zip(bbdf['name'],bbdf['spos'],bbdf['ip'])]
    incmd = ['install element=bbmrk_{}.{}, class=bbmarker, at={}, from={};'.format(bm,row['name'],row['spos'],row['ip']) for i,row in bbdf.iterrows()]
    _dummy = '\n'.join(incmd)
    print('Install command : \n{}'.format(_dummy))
    mmad.input(f'''
        option, warn, info;
        bbmarker : marker;
        seqedit, sequence={lbeam};
            {_dummy}
            flatten;
        endedit;
        option, -warn, -info;
    ''')
    return

def calculate_BB_lens(mmad, bbdf, wbeam):
    '''
    Calculate the BB lenses for all IPs of the selected beam
    Input:
        bbdf            : df with the BB basic info 
        wbeam           : the beam to consider (weak beam), format lhcb1/lhcb2

    Returns:
        bblensdf        : dataframe with the BB lense data
                        ['name','sigx','sigy','xma','yma','charge','spos','ip','beam']
                        where name has the format 'bb_b*.ip*{l/r}ho*' l=left(before) of IP, r=right(after) of IP

    '''
    print ('>>> beambeam:calculate_BB_lens: wbeam={}, bbmarkers={}'.format(wbeam, bbdf.shape[0]))
    sbeam = 'lhcb2'
    bs = 'b2'
    bw = 'b1'
    sign_xsu = 1.0
    if wbeam == 'lhcb2' :
        sbeam = 'lhcb1'
        sign_xsu = -1.0
        bs = 'b1'
        bw = 'b2'

    twiss, _ = pmadx.twissLHC(mmad, option=r'^bbmrk_', fout='')
    
    survdf = pmadx.surveyLHC(mmad)
    strongdf = survdf[survdf['beam'] == sbeam]
    weakdf = survdf[survdf['beam'] == wbeam]

    # _stwdf = stdf[stdf['name'].str.contains('bbmrk')] # --- get the BBmarker elements of the strong beam
    mxbeam = mmad.sequence[sbeam].beam
    epsx = mxbeam.ex
    epsy = mxbeam.ey

    bblensdf = {'name':[],'xma':[],'yma':[],'sigx':[],'sigy':[],'charge':[],'spos':[],'ip':[],'xma0':[]}
    for i, row in twiss[twiss['beam']==sbeam].iterrows(): 
        print ('\t - [{}] sbeam el={}, position={}'.format(i, row['name'], row['s']))
        name = row['name'].split(':')[0]  
        nambb, nbbel = name.split('.')
        print('\t - bbdf name to search :{}'.format(nbbel))

        # -- marker name bbmrk_b{beam}.ip{ip}{l/r}_ho_{n}
        name_weak = name.replace(bs, bw)
        namho0_s = nambb + '.' + nbbel[0:3] + 'ho_0'
        namho0_w = namho0_s.replace(bs, bw)
        x_su = strongdf.loc[name].x - weakdf.loc[name_weak].x - \
            (strongdf.loc[namho0_s].x - weakdf.loc[namho0_w].x)
        # print(x_su, 'nam:', strongdf.loc[name].x, weakdf.loc[name_weak].x, 'ho0:', strongdf.loc[namho0_s].x, weakdf.loc[namho0_w].x)
        _aux = bbdf[bbdf['name'] == nbbel]
        if not _aux.empty :
            j = _aux['ip'].values[0]
            s = _aux['spos'].values[0]
            chrg = _aux['charge'].values[0]
            print ('\t - BB element found in df : {} {} {}'.format(j,s,chrg))
        else:
            print ('\t - Not matching BB element found in df!!!')
            continue
        # bbnam.append('bb_'+lbeam.replace('lhc','')+'.'+nbbel)
        bblensdf['name'].append(name_weak.replace('bbmrk','bb'))
        bblensdf['sigx'].append(np.sqrt(epsx * row['betx']))
        bblensdf['sigy'].append(np.sqrt(epsy * row['bety']))
        bblensdf['xma0'].append(row['x'])
        bblensdf['xma'].append(row['x']-x_su*sign_xsu)
        bblensdf['yma'].append(row['y'])
        bblensdf['ip'].append(j)
        bblensdf['charge'].append(chrg)
        bblensdf['spos'].append(s)

    bblensdf = pd.DataFrame(bblensdf)
    bblensdf['beam'] = wbeam
    print ('elements defined : {}'.format(bblensdf))
    return bblensdf

def install_BB_lens(mmad, ldf, lbeam):
    ''' Install the BB lenses with parameters in ldf for lbeam '''

    print ('>>> Install_BB_lenses: for beam {}'.format(lbeam))
    bldf = ldf[ldf['beam'] == lbeam ]
    if bldf.empty:
        print ('>>> No lenses defined for beam = {}'.format(lbeam))
        return

    bbeldef = ['{} : beambeam, sigx={}, sigy={},xma={}, yma={},bbshape=1,bbdir=-1,charge:={}*on_bb_charge;'.format(
        row['name'],row['sigx'],row['sigy'],row['xma'],row['yma'],row['charge']) for i,row in bldf.iterrows()]
    bbelpar = ['install, element={}, at={}, from={};'.format(row['name'],row['spos'],row['ip']) for i,row in bldf.iterrows()]

    print ('>>> {} BB elements defined - going to insert them into the sequence for beam {}'.format(len(bbeldef),lbeam))

    _def = '\n'.join(bbeldef)
    _ins = '\n'.join(bbelpar)
    print ('\t BBel definiton command : \n\t {}'.format(_def))
    print ('\t BBel install command : \n\t {}'.format(_ins))

    mmad.input(f'''
        option, warn, info;
        {_def}
        seqedit, sequence={lbeam};
            flatten;
            {_ins}
            flatten;
        endedit;
        option, -warn, -info;
    ''')
    return

def define_BB_LensesAtIP(mmad, ip, bbel, option='LAST'):
    ''' Define the BB lenses for an IP
            - alternate b1/b2 until the orbit doesn't change
        Input :
            mmad     the MADX instance
            bbel     DF with the BB names and relative positions for the IP
            option   LAST return the info from the initial and final iteration
                     ALLL retrun the info for each iteration
        Return :
            bbtws    DF list with the Twiss tables for the iterations
            bbsum    DF list with the Twiss summ tables for the iterations
            bblen    DF list with the BB lenses definition for the iterations
    '''

    bbtws = []
    bbsum = []
    bblen = []
    bbsrv = []

    print ('>>> define_BB_LensesAtIP : ip={}'.format(ip))
    # --- remove any BB markers or lenses at the IP
    # n = pmadx.countElementsInSeq(mmad, ['bbmrk',ip], lb)
    # n = pmadx.countElementsInSeq(mmad, ['bb_',ip], lb)
    for lb in ['lhcb1','lhcb2']:
        bm = lb.replace('lhc','')
        print ('\t - [{}] : remove existing bb markers and elements, and install {} new BB markers !'.format(lb, bbel.shape[0]))
        pmadx.removeElementsFromSeq(mmad, lb, 'bbmarker', 'bbmrk_{}.{}'.format(bm, ip))
        pmadx.removeElementsFromSeq(mmad, lb, 'beambeam', 'bb_{}.{}'.format(bm, ip))
        install_BB_mark(mmad, bbel, lb)
        n = pmadx.countElementsInSeq(mmad, ['bbmrk',ip], lb)
        assert bbel.shape[0] == n, \
            'Number of installed markers {} does not match that of bbel {} '.format(n, bbel.shape[0])
    
    print ('\t - initial twiss')

    twissb1, summb1 = pmadx.twissLHCBeam(mmad, 'lhcb1', option=r'^ip|bbmrk_')
    twissb2, summb2 = pmadx.twissLHCBeam(mmad, 'lhcb2', option=r'^ip|bbmrk_')
    #print ('\t BB markers in twiss : b1={} b2={}'.format(twissb1[twissb1['name'].str.find('bbmrk_')>=0].shape[0],
    #                                                     twissb2[twissb2['name'].str.find('bbmrk_')>=0].shape[0]))
    print ('\t BB markers in twiss : b1={} b2={}'.format(twissb1[twissb1.index.str.startswith('bbmrk_')].shape[0],
                                                         twissb2[twissb2.index.str.startswith('bbmrk_')].shape[0]))

    _auxt = pd.concat([twissb1, twissb2])
    _auxt['iter'] = -1
    bbtws.append(_auxt)

    _auxs = pd.concat([summb1, summb2])
    _auxs['iter'] = -1
    bbsum.append(_auxs)

    survdf = pmadx.surveyLHC(mmad)
    survdf['iter'] = -1
    bbsrv.append(survdf)

    x0b1 = twissb1.loc[ip].x; x0b2 = twissb2.loc[ip].x
    y0b1 = twissb1.loc[ip].y; y0b2 = twissb2.loc[ip].y
    print ('\t Initial beam coordinates at IP:')
    print ('\t\t x = {} {} y={} {}'.format(x0b1, x0b2, y0b1, y0b2))

    mmad.globals.on_bb_charge = 1
    print('\t flag ON_BB_CHARGE set to 1')
    for j in np.arange(0,10,1):
        bl1 = calculate_BB_lens(mmad, bbel, twissb2, 'lhcb1')
        # apply_surv_corr_BB_lens(twissb1, twissb2, bl1,'lhcb1')
        install_BB_lens(mmad, bl1, 'lhcb1')
        twissb1, summb1 = pmadx.twissLHCBeam(mmad, 'lhcb1', option=r'^ip|bb')
        n = pmadx.countElementsInSeq(mmad, ['bbmrk', ip], 'lhcb1')
        assert bbel.shape[0] == n, \
            'lhcb1 : bb markers in sequence {} - does not match that of bbel {}'.format(n, bbel.shape[0])

        xb1 = twissb1.loc[ip].x
        yb1 = twissb1.loc[ip].y

        bl2 = calculate_BB_lens(mmad, bbel, twissb1, 'lhcb2')
        # apply_surv_corr_BB_lens(twissb1, twissb2, bl2, 'lhcb2')
        install_BB_lens(mmad, bl2, 'lhcb2')
        twissb2, summb2 = pmadx.twissLHCBeam(mmad, 'lhcb2', option=r'^ip|bb')
        n = pmadx.countElementsInSeq(mmad, ['bbmrk', ip], 'lhcb2')
        assert bbel.shape[0] == n, \
            'lhcb2 : bb markers in sequence {} - does not match that of bbel {}'.format(n, bbel.shape[0])

        xb2 = twissb2.loc[ip].x
        yb2 = twissb2.loc[ip].y

        print (' [{}] : x = {} {}  y={} {}'.format(j,xb1, xb2, yb1, yb2))

        _auxt = pd.concat([twissb1, twissb2]); _auxt['iter'] = j
        _auxs = pd.concat([summb1, summb2]);   _auxs['iter'] = j
        _tmp = pd.concat([bl1, bl2]);  _tmp['iter'] = j

        if option == 'ALL' :
            bbtws.append(_auxt)
            bbsum.append(_auxs)
            bblen.append(_tmp)

        if (xb1-x0b1)**2 + (xb2-x0b2)**2 + (yb1-y0b1)**2 + (yb2-y0b2)**2 < 1.0e-14 :
            print('\t - convergence reached - end of loop')
            pmadx.removeElementsFromSeq(mmad, 'lhcb1', 'bbmarker', 'bbmrk_b1.{}'.format(ip))
            pmadx.removeElementsFromSeq(mmad, 'lhcb2', 'bbmarker', 'bbmrk_b2.{}'.format(ip))
            break
        x0b1 = xb1; y0b1 = yb1
        x0b2 = xb2; y0b2 = yb2
        
        print ('\t - removing beambeam elements from both sequences')
        for bm in ['b1','b2']:
            pmadx.removeElementsFromSeq(mmad, 'lhc'+bm, 'beambeam', 'bb_{}.{}'.format(bm, ip))
            assert pmadx.countElementsInSeq(mmad, ['bb_'], 'lhc'+bm) == 0, \
                'lhc{} : bb elements still present in sequence at loop end!'.format(bm)

    if option == 'LAST':
        bbtws.append(_auxt)
        bbsum.append(_auxs)
        bblen.append(_tmp)

    return pd.concat(bbtws), pd.concat(bbsum), pd.concat(bblen), survdf

def _define_BB_Lenses(mmad, bbel, option='LAST'):
    '''
        Define the BB lenses for a given configuration.
         - Loop over defined IPs
         - Alternate lhcb1/lhcb2 lenses to verify orbit convergence (strong-strong approx.)
         - for option=LAST, return only the first (iter=-1, no bb) and final twiss data  
    '''
    if bbel.empty :
        print ('>>> define_BB_Lenses: input BB elements DF is empty! ... do nothing! ')
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    btwiss = []
    btsumm = []
    bblens = []

    ipsbb = np.unique(bbel.ip.values)
    print ('>>> define_BB_Lenses: define BB lenses for both beams at IPs : {} '.format(ipsbb))
    for ip in ipsbb:
        a, b, c,d = define_BB_LensesAtIP(mmad, ip, bbel[bbel['ip'] == ip], option)
        btwiss.append(a); btsumm.append(b), bblens.append(c), bbsurv.append(d)
    return pd.concat(btwiss), pd.concat(btsumm), pd.concat(bblens)

def define_BB_Lenses(mmad, bbel, option='LAST'):
    '''
        Define the BB lenses for a given configuration.
         - Alternate lhcb1/lhcb2 lenses to verify orbit convergence (strong-strong approx.)
         - for option=LAST, return only the first (iter=-1, no bb) and final twiss data 
        
        Returns : twiss, summ and bblens dataframes with the results
    '''
    if bbel.empty :
        print ('>>> define_BB_Lenses: input BB elements DF is empty! ... do nothing! ')
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    ipsbb = np.unique(bbel.ip.values)
    print ('>>> define_BB_Lenses: define BB lenses for both beams at IPs : {} '.format(ipsbb))
    
    bbtws = []
    bbsum = []
    bblen = []
    bbsrv = []

    for lb in ['lhcb1','lhcb2']:
        bm = lb.replace('lhc','')
        print ('\t - [{}] : remove existing bb markers and elements, and install {} new BB markers !'.format(lb, bbel.shape[0]))
        pmadx.removeElementsFromSeq(mmad, lb, 'bbmarker', 'bbmrk_{}'.format(bm))
        pmadx.removeElementsFromSeq(mmad, lb, 'beambeam', 'bb_{}'.format(bm))
        install_BB_mark(mmad, bbel, lb)
        n = pmadx.countElementsInSeq(mmad, ['bbmrk'], lb)
        assert bbel.shape[0] == n, \
            '{} : Number of installed markers {} does not match that of bbel {} '.format(lb, n, bbel.shape[0])
    
    print ('\t - initial twiss')
    twiss0, summ0 = pmadx.twissLHC(mmad, option=r'^ip|bbmrk_', fout='')
    print ('\t BB markers in LHC twiss : b1/b2 = {}'.format(twiss0[twiss0.index.str.startswith('bbmrk_')].shape[0]))
    twiss0['iter'] = -1
    summ0['iter'] = -1

    ips0, xip0, yip0 = pmadx.getLHCBeamPosAtIP(twiss0)
    [print('{} : x = {} --> sep0_x = {} y={} -->sep0_y = {}'.format(ip.upper(), x, np.diff(x), y, np.diff(y))) for ip,x,y in zip(ips0,xip0,yip0)]

    mmad.globals.on_bb_charge = 1
    print('\t flag ON_BB_CHARGE set to 1')

    for j in np.arange(0,10,1):
        print('\n>>>> loop [{}]\n'.format(j))
        bblensb1 = calculate_BB_lens(mmad, bbel, 'lhcb1')
        bblensb2 = calculate_BB_lens(mmad, bbel, 'lhcb2')
        bblens = pd.concat([bblensb1, bblensb2])

        install_BB_lens(mmad, bblens, 'lhcb1')
        install_BB_lens(mmad, bblens, 'lhcb2')

        twiss_j, summ_j = pmadx.twissLHC(mmad, option=r'^ip|bb')
        n = pmadx.countElementsInSeq(mmad, ['bbmrk'], 'lhcb1')
        assert bblensb1.shape[0] == n, \
            'lhcb1 : bb markers in sequence {} - does not match that of bbel {}'.format(n, bblensb1.shape[0])
        n = pmadx.countElementsInSeq(mmad, ['bbmrk'], 'lhcb2')
        assert bblensb2.shape[0] == n, \
            'lhcb2 : bb markers in sequence {} - does not match that of bbel {}'.format(n, bblensb2.shape[0])

        ips, xip, yip = pmadx.getLHCBeamPosAtIP(twiss_j)
        [print('{} : x = {} --> sep0_x = {} y={} -->sep0_y = {}'.format(i.upper(), x, np.diff(x), y, np.diff(y))) for i,x,y in zip(ips,xip,yip)]
        
        bblens['iter'] = j
        twiss_j['iter'] = j
        summ_j['iter'] = j
        if option == 'ALL' :
            bbtws.append(twiss_j)
            bbsum.append(summ_j)
            bblen.append(bblens)

        delta_x = np.asarray(xip).ravel() - np.asarray(xip0).ravel()
        delta_y = np.asarray(yip).ravel() - np.asarray(yip0).ravel()
        delta = np.dot(delta_x, delta_x) + np.dot(delta_y, delta_y)
        if delta < 1.0e-14 :
            print('\t - convergence reached - end of loop')
            pmadx.removeElementsFromSeq(mmad, 'lhcb1', 'bbmarker', 'bbmrk_')
            pmadx.removeElementsFromSeq(mmad, 'lhcb2', 'bbmarker', 'bbmrk_')
            break
        xip0 = xip
        yip0 = yip
        
        print ('\t - removing beambeam elements from both sequences')
        pmadx.removeElementsFromSeq(mmad, 'lhcb1', 'beambeam', 'bb_')
        pmadx.removeElementsFromSeq(mmad, 'lhcb2', 'beambeam', 'bb_')

    if option == 'LAST':
        bbtws.append(twiss_j)
        bbsum.append(summ_j)
        bblen.append(bblens)

    return pd.concat(bbtws), pd.concat(bbsum), pd.concat(bblen)


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

    # --- use the twiss of tee two beams to calculate the BB lense parameters
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