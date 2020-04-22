#
# --- py4madx Script Library
#
# (c) I.E - September 2019
#
# MADX scripts to run with cpymad
#

import os
import numpy as np
import pandas as pd

LHCXsingKnobs = ['on_x1', 'on_sep1', 'on_o1', \
				'on_x2', 'on_sep2', 'on_o2', 'on_oe2', 'on_a2', \
				'on_x5', 'on_sep5', 'on_o5', 'on_ov5', \
				'on_x8', 'on_sep8', 'on_o8',           'on_a8']

LHCGlobals = ['NRJ','I_MO','ON_COLLISION','ON_BB_SWITCH','ON_BB_CHARGE']

def countElementsInSeq(mmad, elnames, seq):
	elist = mmad.sequence[seq].element_names()
	f_elist = [e for e in elist if all(e.find(s)>=0 for s in elnames)]
	return len(f_elist)

def getLHCBeamSigmaAtIP(mmad, twissdf, ip, lbeam):
	beamdef = mmad.sequence[lbeam].beam
	epsx = beamdef.ex
	epsy = beamdef.ey
	_tmp = twissdf[twissdf['beam'] == lbeam]
	return np.sqrt(_tmp.loc[ip].betx * epsx), np.sqrt(_tmp.loc[ip].bety * epsy)

def getLHCBeamPosAtIP(twissdf, lbeam):
	ips = ['ip1','ip2','ip3','ip5','ip8']
	_tmp = twissdf[twissdf['beam'] == lbeam]
	xip = [_tmp.loc[i].x.values for i in ips]
	yip = [_tmp.loc[i].y.values for i in ips]
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

def twiss2df(twisstable):
	_twdf = pd.DataFrame.from_dict(twisstable, orient='index').transpose()
	_twdf['elname'] = _twdf['name'].apply(lambda x : x.split(':')[0])
	return _twdf.set_index('elname')

def table2df(twisstable):
	_tdf = pd.DataFrame.from_dict(twisstable, orient='index').transpose()
	#_tdf['elname'] = _tdf['name'].apply(lambda x : x.split(':')[0])
	return _tdf.set_index('name')

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
	_ttable = mmad.twiss(file=fout)
	_twissdf = twiss2df(_ttable)
	_twissdf = _twissdf.filter(regex=selection, axis=0)
	assert _twissdf.shape[0] > 0 , '>> twissLHCBeam: twiss table selection %r results to empty table!' % selection
	_twissdf['beam'] = lbeam

	_sumdf = pd.DataFrame.from_dict(mmad.table.summ, orient='index')
	_beamdf = pd.DataFrame.from_dict(mmad.sequence[lbeam].beam, orient='index')
	_gdf = pd.concat([_sumdf, _beamdf]).transpose().set_index('sequence') 
	return _twissdf, _gdf

def printLHCXsingScheme(mmad):
	print('\n LHC beam crossing scheme :')
	for v in LHCXsingKnobs:
		print ('\t {:.<15s} {}'.format(v, mmad.globals[v]))
	return

def printLHCGlobalConfig(mmad):
    print('>>> LHC Beam Configuration:')
    for v in LHCGlobals:
        print ('{:8s} = {:7.2f} '.format(v, mmad.globals[v]))
    print (' ')
    return

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