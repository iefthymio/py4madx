#
# --- py4madx Script Library
#
# (c) I.E - September 2019
#
# MADX scripts to run with cpymad
#

__version__ = '2.11 - (ie) 20.01.2022'

import os
import numpy as np
import pandas as pd

LHCXsingKnobs = ['on_x1', 'on_sep1', 'on_o1', \
                 'on_x2', 'on_sep2', 'on_o2', 'on_oe2', 'on_a2', \
                 'on_x5', 'on_sep5', 'on_o5', 'on_ov5', \
                 'on_x8', 'on_sep8', 'on_o8',           'on_a8',\
                 'on_alice', 'on_lhcb']

LHCGlobals = ['NRJ','I_MO','ON_COLLISION','ON_BB_SWITCH','ON_BB_CHARGE']

ips = ['ip1','ip2','ip3','ip5','ip8']

def countElementsInSeq(mmad, elnames, seq):
    elist = mmad.sequence[seq].element_names()
    if type(elnames) != list:
        elnames = [elnames]
    f_elist = [e for e in elist if all(e.find(s)>=0 for s in elnames)]
    return len(f_elist)

def getLHCBeamSigmaAtIP(mmad, twissdf, ip, lbeam):
    beamdef = mmad.sequence[lbeam].beam
    epsx = beamdef.ex
    epsy = beamdef.ey
    _tmp = twissdf[twissdf['beam'] == lbeam]
    return np.sqrt(_tmp.loc[ip].betx * epsx), np.sqrt(_tmp.loc[ip].bety * epsy) 

def getLHCBeamPosAtIP(twissdf, lbeam='ALL'):
    if lbeam in ['lhcb1','lhcb2']:
        _tmp = twissdf[twissdf['beam'] == lbeam]
        xip = [_tmp.loc[i].x for i in ips]
        yip = [_tmp.loc[i].y for i in ips]
    else:
        xip = [twissdf.loc[i].x.values for i in ips]
        yip = [twissdf.loc[i].y.values for i in ips]
    return ips, xip, yip   

def removeElementsFromSeq(mmad, sequ, elclass, elptrn):
    opt_info = mmad.options.info 
    opt_warn = mmad.options.warn
    mmad.options.info = True
    mmad.options.warn = True
    mmad.input(f'''
        option, warn;
        seqedit,sequence={sequ};
        flatten;
        select,flag=seqedit,clear;
        select,flag=seqedit,class={elclass},pattern="{elptrn}*";
        remove,element=SELECTED;
        flatten;
        endedit; 
    ''')
    mmad.options.info = opt_info
    mmad.options.warn = opt_warn
    return

def getMadGlobals(mmad, sletter=''):
    return dict((i, mmad.globals[i]) for i in mmad.globals.keys() if i.find(sletter)== 0 )

def twiss2df(twisstable, fullname=False):
    _twdf = pd.DataFrame.from_dict(twisstable, orient='index').transpose()
    if fullname :
        _twdf['elname'] = _twdf['name']
    else:
        _twdf['elname'] = _twdf['name'].apply(lambda x : x.split(':')[0])
    return _twdf.set_index('elname')

def table2df(twisstable, fullname=False):
    _tdf = pd.DataFrame.from_dict(twisstable, orient='index').transpose()
    if fullname :
        _tdf['elname'] = _tdf['name']
    else:
        _tdf['elname'] = _tdf['name'].apply(lambda x : x.split(':')[0])
    return _tdf.set_index('elname')

def mergeLHCBeamTwissTables(mmad, twissb1, twissb2):
    t_b1 = mmad.table[twissb1].dframe()
    t_b1['beam'] = 'lhcb1'
    t_b2 = mmad.table[twissb2].dframe()
    t_b2['beam'] = 'lhcb2'
    return pd.concat([t_b1,t_b2])

def surveyLHC(mmad):
    mmad.use('lhcb1')
    survb1 = mmad.survey().dframe()
    survb1['beam'] = 'lhcb1'

    mmad.use('lhcb2')
    survb2 = mmad.survey().dframe()
    survb2['beam'] = 'lhcb2'

    return pd.concat([survb1, survb2])

def twissLHC(mmad, selection=r'.', fout=''):
    ''' 
        Combined twiss of the two LHC beams.
        Examples of selection:
            selection = r'^ip[1258]'    							 # --- simple selection
            selection = re.compile('|'.join(['^ip[1258]','^bbmk']))  # --- for multiple criteria
    '''
    b1df, s1df = twissLHCBeam(mmad, 'lhcb1', selection, fout.replace('.','_b1.'))
    b2df, s2df = twissLHCBeam(mmad, 'lhcb2', selection, fout.replace('.','_b2.'))

    _tdf = pd.concat([b1df, b2df])
    _sdf = pd.concat([s1df, s2df])
    return _tdf, _sdf

def twissLHCBeam(mmad, lbeam, selection=r'.', fout=''):
    mmad.use(sequence=lbeam)
    _twissdf = mmad.twiss().dframe()
    # _twissdf = _twissdf.filter(regex=selection, axis=0)
    # assert _twissdf.shape[0] > 0 , '>> twissLHCBeam: twiss table selection %r results to empty table!' % selection
    _twissdf['beam'] = lbeam
    
    _sumdf = mmad.table['summ'].dframe()
    _sumdf = _sumdf.set_index(pd.Index([lbeam]))
    return _twissdf, _sumdf

def setLHCXsingScheme(mmad, knobs, option=''):
    cmnd = ''
    if option == 'zero' :
        cmnd = [' {} = 0;'.format(key) for key in LHCXsingKnobs]
        # cmnd.append(' on_sep2 = 1;') # -- add this to maintain separation at IP2
    else:
        cmnd = [' {} = {};'.format(key, knobs[key]) for key in LHCXsingKnobs]
    txt = '\n'.join(cmnd)
    mmad.input(txt)
    return

def string_or_number(s):
    try:
        z = int(s)
        return z
    except ValueError:
        try:
            z = float(s)
            return z
        except ValueError:
            return s.strip('"')

def tfs2df(ftfs):
    with open(ftfs) as fin:
        i = 0
        sumdata = {}
        header = fin.readline()
        while header.find('*') < 0 :
            cdata = header.strip().lower().split()
            sumdata[cdata[1]] = string_or_number(cdata[3])
            header = fin.readline()
            
        cnames = header.strip().lower()
        data = pd.read_csv(fin, delim_whitespace=True, header=0, index_col=False, names=cnames.split()[1:], quoting=2)
    data['beam'] = sumdata['sequence']
    data['name'] = data['name'].str.lower()
    data.set_index('name', inplace=True, drop=False )

    sumdf = pd.DataFrame.from_dict(sumdata, orient='index').T
    sumdf['beam'] = sumdata['sequence']
    sumdf.set_index('beam', inplace=True, drop=True)
    return data, sumdf

def compare_summ_df(df1, df2):
    ''' check if the two summd dataframes are identical '''
    identical = True
    for i in df1.index:
        x1 = df1.loc[i].values
        x2 = df2.loc[i].values
        if np.sum(x1 - x2) :
            identical = False
    return identical

def compare_twiss_df(df1, df2):
    ''' check if the two twiss dataframes are identical '''
    identical = True
    for beam in ['lhcb1', 'lhcb2']:
        aux1 = df1[df1['beam'] == beam].select_dtypes(include='float64')
        aux2 = df2[df2['beam'] == beam].select_dtypes(include='float64')
        for i in aux1.index:
            x1 = aux1.loc[i].values
            x2 = aux2.loc[i].values
            if np.sum(x1-x2) > 0 :
                identical = False
    return identical

def select_ip(df, nir, bim):
    ''' Select twiss df around IR for bim'''
    return df[df['beam']==bim].loc[f's.ds.l{nir}.b{bim[-1]}':f'e.ds.r{nir}.b{bim[-1]}']

def twiss_select_srange(df, bim, srange):
    return df[df['beam']==bim].loc[srange[0]:srange[1]]

def select(df, nir, bim):
    return df[df['beam']==bim].loc[f's.ds.l{nir}.b{bim[-1]}':f'e.ds.r{nir}.b{bim[-1]}']

def get_twiss_at_element(df, regex, varlist=['name','keyword','s','betx','bety']):
    ''' get twiss df line for selected element(s) based on regular expression
                regex_q7 = r'mqm.a7[l,r]5'
                _aux = get_betas_at_element(twiss_match, regex_q5)
    '''
    return df[df.index.str.contains(regex)][varlist]

def deltaphase(tdf, beam, el1, el2, var, verbose=False):
    dphase = tdf[tdf['beam']==beam].loc[el2][var] - tdf[tdf['beam']==beam].loc[el1][var]
    if verbose:
        print(f' phase: {el1} -> {el2}, {var} : {dphase:0<12.10g}')
    return dphase

def get_dphase_ir(twdf, nir):
    if twdf.index[0].find('ip') >= 0:
        ip_start = int(twdf.index[0][-1:])
    if nir == ip_start:
        _elb1 = twdf[twdf['beam']=='lhcb1'].index[-1]
        _elb2 = twdf[twdf['beam']=='lhcb2'].index[-1]
        return {'lhcb1': {
            'mux' : deltaphase(twdf, 'lhcb1', f's.ds.l{nir}.b1', _elb1, 'mux') + deltaphase(twdf, 'lhcb1', f'ip{nir}', f'e.ds.r{nir}.b1', 'mux'),
            'muy' : deltaphase(twdf, 'lhcb1', f's.ds.l{nir}.b1', _elb1, 'muy') + deltaphase(twdf, 'lhcb1', f'ip{nir}', f'e.ds.r{nir}.b1', 'muy')
            },
            'lhcb2': {
            'mux' : deltaphase(twdf, 'lhcb2', f's.ds.l{nir}.b2', _elb2, 'mux') + deltaphase(twdf, 'lhcb2', f'ip{nir}', f'e.ds.r{nir}.b2', 'mux'),
            'muy' : deltaphase(twdf, 'lhcb2', f's.ds.l{nir}.b2', _elb2, 'muy') + deltaphase(twdf, 'lhcb2', f'ip{nir}', f'e.ds.r{nir}.b2', 'muy')
            }
        }
    else:
        return {'lhcb1': { 
            'mux' :  deltaphase(twdf, 'lhcb1', f's.ds.l{nir}.b1', f'e.ds.r{nir}.b1', 'mux'),
            'muy' :  deltaphase(twdf, 'lhcb1', f's.ds.l{nir}.b1', f'e.ds.r{nir}.b1', 'muy')
            },
            'lhcb2': {
            'mux' :  deltaphase(twdf, 'lhcb2', f's.ds.l{nir}.b2', f'e.ds.r{nir}.b2', 'mux'),
            'muy' :  deltaphase(twdf, 'lhcb2', f's.ds.l{nir}.b2', f'e.ds.r{nir}.b2', 'muy')}
        }

def get_dphase_ssring(twdf):
    _dflist = []
    for ss in np.arange(1, 9):
        dd = {'ip' : ss}
        dd.update(get_dphase_ir(twdf, ss))
        _dflist.append(pd.DataFrame(dd))
    return pd.concat(_dflist)

def twiss_rel_ip(tdf, nir, beam, 
                 vars=['beam','name','s','keyword','betx','bety','mux','muy']):
    _tmpir = select(tdf, nir, beam).copy()
    if vars :
        _tmpir = _tmpir[vars]
    non_numeric_columns = [ c for c in _tmpir.columns if pd.api.types.is_object_dtype(_tmpir[c])]
    _tmpnum = _tmpir.drop(columns=non_numeric_columns)
    _tmpnum = _tmpnum.subtract(_tmpnum.loc[f'ip{nir}'], axis=1)
    _tmpnonnum = _tmpir[non_numeric_columns]
    
    return _tmpnonnum.join(_tmpnum, how='outer')
