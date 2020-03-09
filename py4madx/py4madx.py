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

# --- Functions in alphabetic order

def countElementsInSeq(mmad, sname, seq):
	''' Count the appearance of elements in sequence with name containing strings in sname'''
	elist = mmad.sequence[seq].element_names()
	f_elist = [e for e in elist if all(e.find(s)>=0 for s in sname)]
	return len(f_elist)

def getLHCBeamSigmaAtIP(mmad, twdf, ip, lbeam):
	''' 
		mmad 	: the Mad handler
		twdf 	: twiss dataframe 
		ip	 	: the name of the IP, eg 'ip1'
		lbeam 	: the beam to consider, eg. 'lhcb1' 
	'''
	beamdef = mmad.sequence[lbeam].beam
	epsx = beamdef.ex
	epsy = beamdef.ey
	_tmp = twdf[twdf['beam'] == lbeam]
	return np.sqrt(_tmp.loc[ip].betx * epsx), np.sqrt(_tmp.loc[ip].bety * epsy)

def getLHCBeamPosAtIP(twdf, lbeam):
	'''
		twdf : the twiss dataframe 
	'''
	ips = ['ip1','ip2','ip3','ip5','ip8']
	_tmp = twdf[twdf['beam'] == lbeam]
	xip = [_tmp.loc[i].x.values for i in ips]
	yip = [_tmp.loc[i].y.values for i in ips]
	return ips, xip, yip   

def removeElementsFromSeq(mmad,sequ,elclass,elptrn):
	''' 
		mmad 	: the MAD handler
		sequ	: sequence id, eg. 'lhcb1'
		elclass	: element class in sequence
		elptrn	: element name pattern - regular expression
	'''
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
	'''
		mmad 	: the MAD handler
		sletter	: starting letter 
	'''
	return dict((i, mmad.globals[i]) for i in mmad.globals.keys() if i.find(sletter)== 0 )

def table2df(mdtable, option='FULL'):
	''' Convert a cpyMADX table to DF
			My version of the function sicne the one in the package does not seem to work for all cases!
			option = 'FULL' (default), 'BASIC':name,s,x,y,betx,bety,sig11,sig12,sig22,sig33,sig34,sig44,sig13,sig14,sig23,sig24
	'''
	vsel = ['name','s','x','y','betx','bety','sig11','sig12','sig22','sig33','sig34','sig44','sig13','sig14','sig23','sig24']

	_df = pd.DataFrame()
	if option == 'BASIC' :
		for v in vsel:
			vv = np.array(mdtable[v])
			_df[v] = vv
	else:
		for v in list(mdtable):
			vv = np.array(mdtable[v])
			_df[v] = vv
	return _df

def mergeLHCBeamTwissTables(mmad, tb1, tb2):
	t_b1 = mmad.table[tb1].dframe()
	t_b1['beam'] = 'lhcb1'
	t_b2 = mmad.table[tb2].dframe()
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

def twissLHC(mmad, option=r'.', fout=''):
	'''
		mmmad 	: the MAD handler
		option	: optional rgex to select twiss elements or full table
		fout 	: optional to save twiss output to a .tfs file
	''' 
	b1df, s1df = twissLHCBeam(mmad, 'lhcb1', option, fout)
	b2df, s2df = twissLHCBeam(mmad, 'lhcb2', option, fout)

	_tdf = pd.concat([b1df, b2df])
	_sdf = pd.concat([s1df, s2df])
	return _tdf, _sdf

def twissLHCBeam(mmad, lbeam, option=r'.', fout=''):
	''' Execute twiss for for an LHC lbeam and return results in signle df selecting rows matching the option
			option  = regular expression to select rows, example r'^ip[12358]' to get the IPs only 
					  default : full twiss table
			fout = save twiss data to tfs file, 
			       default : no file
	''' 
	mmad.use(sequence=lbeam)
	if fout :
		_fsplit = fout.split('.')
		twiss = mmad.twiss(file='{}_{}.{}'.format(_fsplit[0], lbeam, _fsplit[1]))
	else:
		twiss = mmad.twiss()
	_twissdf = twiss.dframe()
	_twissdf = _twissdf.filter(regex=option, axis=0)
	assert _twissdf.shape[0] > 0 , '>> twissLHCBeam: twiss table selection %r results to empty table!' % option

	_twissdf['beam'] = lbeam

	_sumdf = mmad.table.summ.dframe()
	_sumdf['beam'] = lbeam
	# -- add the information from the beam definition as in the Twiss output file
	thead = ['particle','mass','charge','energy','pc','gamma','beta','brho','kbunch','bcurrent','sige',\
			 'sigt','npart','ex','ey','exn','eyn','et','bv',]
	_bdef = mmad.sequence[lbeam].beam
	for ihead in thead:
		_sumdf[ihead] = _bdef[ihead]
	_sumdf = _sumdf.set_index('beam')
	return _twissdf, _sumdf

def printLHCXsingScheme(mmad):
	print('\n LHC beam crossing scheme :')
	for v in LHCXsingKnobs:
		print ('\t {:.<15s} {}'.format(v, mmad.globals[v]))
	return

def printLHCGlobalConfig(mmad):
    print('>>> LHC Beam Configuration:')
    for v in ['NRJ','I_MO','ON_COLLISION','ON_BB_SWITCH','ON_BB_CHARGE']:
        print ('{:8s} = {:7.2f} '.format(v, mmad.globals[v]))
    print (' ')
    return

def setLHCXsingScheme(mmad, par, option=''):
    ''' 
	    mmad	: the cpyMAD handler
        par		: dict of the crossing parameters to set
        option 	: 'zero' = to set all values to zero, '' otherwise use the values in par
    '''
    cmnd = ''
    if option == 'zero' :
        cmnd = [' {} = 0;'.format(key) for key in LHCXsingKnobs]
        # cmnd.append(' on_sep2 = 1;') # -- add this to maintain separation at IP2
    else:
        cmnd = [' {} = {};'.format(key, par[key]) for key in LHCXsingKnobs]
    txt = '\n'.join(cmnd)
    mmad.input(txt)
    return