#
#######################################################################################
# printing functions
#######################################################################################

import numpy as np
import pandas as pd
import itertools

from . import pmadx

__version__ = '1.0 - (ie) 28.01.2022'

'''
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
'''

def print_tune_values(summdf): 
    print (f'---- print tune values :')
    for ib in ['lhcb1','lhcb2']:
        _aux = summdf.loc[ib]
        print (f'\t  {ib} :  q1 = {_aux.q1:9.5f}, q2 = {_aux.q2:9.5f}, dq1 = {_aux.dq1:9.5f}, dq2 = {_aux.dq2:9.5f}')
      
def print_phase_advance(twissdf, fout='ipphaseadvance.txt'):
    OF =  open(fout, 'w')
    
    def printing(text, end='\n'):
        print (text, end=end)
        if end :
            OF.write(text + '\n')
        else:
            OF.write(text)
        return

    for bim in ['lhcb1', 'lhcb2']:
        _aux = twissdf[twissdf['beam']==bim]
        for w in ['mux', 'muy']:
            printing (f' {bim:5s} - {w:5s} ')
            xx = ' '*12
            printing (f'{xx}', end='')
            for ip2 in ['ip1','ip2','ip5','ip8']:
                printing (f'{ip2:^12s} ', end='')
            printing('')
            for ip1 in ['ip1','ip2','ip5','ip8']:
                printing (f' {ip1: ^12s}', end='')
                for ip2 in ['ip1','ip2','ip5','ip8']:
                    printing (f'{_aux.loc[ip1][w] - _aux.loc[ip2][w]:12.5f}', end='')
                printing('')
    OF.close()
    print(f' >>>> data saved to {fout}')
    return
