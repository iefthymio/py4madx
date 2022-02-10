#
# -- Script to save LHC optics to external file for re-use by MAD-X
#
# Copied from similar madx macro of the repository
#
import numpy as np

__version__ = '1.0 - (ie) 20.01.2022'

optics_data = {

    'IR1' : {
        '!***IR1 Optics***': [
            'KQX.L1', 'KTQX1.L1', 'KTQX2.L1', 'KQX.R1', 'KTQX1.R1','KTQX2.R1'
            ],
        
        '!Beam 1': [
            'KQ4.L1B1' ,'KQ4.R1B1',
            'KQ5.L1B1', 'KQ5.R1B1', 
            'KQ6.L1B1', 'KQ6.R1B1',
            'KQ7.L1B1', 'KQ7.R1B1',
            'KQ8.L1B1', 'KQ8.R1B1',
            'KQ9.L1B1', 'KQ9.R1B1',
            'KQ10.L1B1', 'KQ10.R1B1',
            'KQTL11.L1B1', 'KQTL11.R1B1',
            'KQT12.L1B1', 'KQT12.R1B1',
            'KQT13.L1B1','KQT13.R1B1'
            ],
        
        '!Beam 2': [
            'KQ4.L1B2', 'KQ4.R1B2', 
            'KQ5.L1B2', 'KQ5.R1B2', 
            'KQ6.L1B2', 'KQ6.R1B2', 
            'KQ7.L1B2', 'KQ7.R1B2', 
            'KQ8.L1B2', 'KQ8.R1B2', 
            'KQ9.L1B2', 'KQ9.R1B2', 
            'KQ10.L1B2', 'KQ10.R1B2', 
            'KQTL11.L1B2', 'KQTL11.R1B2', 
            'KQT12.L1B2', 'KQT12.R1B2', 
            'KQT13.L1B2', 'KQT13.R1B2'
            ],
                
        '!*** IR1 X-scheme***' : [
            'ACBXV1.L1x', 'ACBXV1.L1s', 'ACBXV1.L1', 'ACBXV1.R1x', 'ACBXV1.R1s', 'ACBXV1.R1', 
            'ACBXH1.L1x', 'ACBXH1.L1s', 'ACBXH1.L1', 'ACBXH1.R1x', 'ACBXH1.R1s', 'ACBXH1.R1', 
            'ACBXV2.L1x', 'ACBXV2.L1s', 'ACBXV2.L1', 'ACBXV2.R1x', 'ACBXV2.R1s', 'ACBXV2.R1', 
            'ACBXH2.L1x', 'ACBXH2.L1s', 'ACBXH2.L1', 'ACBXH2.R1x', 'ACBXH2.R1s', 'ACBXH2.R1', 
            'ACBXV3.L1x', 'ACBXV3.L1s', 'ACBXV3.L1', 'ACBXV3.R1x', 'ACBXV3.R1s', 'ACBXV3.R1', 
            'ACBXH3.L1x', 'ACBXH3.L1s', 'ACBXH3.L1', 'ACBXH3.R1x', 'ACBXH3.R1s', 'ACBXH3.R1'
            ],
        
        '!Beam 1 x' : [
            'ACBYVS4.L1B1x', 'ACBYVS4.L1B1s', 'ACBYVS4.L1B1ov', 'ACBYVS4.L1B1', 
            'ACBYVS4.R1B1x', 'ACBYVS4.R1B1s', 'ACBYVS4.R1B1ov', 'ACBYVS4.R1B1', 
            'ACBCV5.L1B1x', 'ACBCV5.L1B1s', 'ACBCV5.L1B1ov', 'ACBCV5.L1B1', 
            'ACBCV6.R1B1x', 'ACBCV6.R1B1s', 'ACBCV6.R1B1ov', 'ACBCV6.R1B1', 
            'ACBYHS4.L1B1x', 'ACBYHS4.L1B1s', 'ACBYHS4.L1B1oh', 'ACBYHS4.L1B1', 
            'ACBYHS4.R1B1x', 'ACBYHS4.R1B1s', 'ACBYHS4.R1B1oh', 'ACBYHS4.R1B1', 
            'ACBCH6.L1B1x', 'ACBCH6.L1B1s', 'ACBCH6.L1B1oh', 'ACBCH6.L1B1', 
            'ACBCH5.R1B1x', 'ACBCH5.R1B1s', 'ACBCH5.R1B1oh', 'ACBCH5.R1B1', 
            'ACBCH8.L1B1oh', 'ACBCH8.L1B1', 
            'ACBCV7.L1B1ov', 'ACBCV7.L1B1', 
            'ACBCH7.R1B1oh', 'ACBCH7.R1B1', 
            'ACBCV8.R1B1ov', 'ACBCV8.R1B1'],
        
        '!Beam 2 x' : [
            'ACBYVS4.L1B2x', 'ACBYVS4.L1B2s', 'ACBYVS4.L1B2ov', 'ACBYVS4.L1B2', 
            'ACBYVS4.R1B2x', 'ACBYVS4.R1B2s', 'ACBYVS4.R1B2ov', 'ACBYVS4.R1B2', 
            'ACBCV6.L1B2x', 'ACBCV6.L1B2s', 'ACBCV6.L1B2ov', 'ACBCV6.L1B2', 
            'ACBCV5.R1B2x', 'ACBCV5.R1B2s', 'ACBCV5.R1B2ov', 'ACBCV5.R1B2', 
            'ACBYHS4.L1B2x', 'ACBYHS4.L1B2s', 'ACBYHS4.L1B2oh', 'ACBYHS4.L1B2', 
            'ACBYHS4.R1B2x', 'ACBYHS4.R1B2s', 'ACBYHS4.R1B2oh', 'ACBYHS4.R1B2', 
            'ACBCH5.L1B2x', 'ACBCH5.L1B2s', 'ACBCH5.L1B2oh', 'ACBCH5.L1B2', 
            'ACBCH6.R1B2x', 'ACBCH6.R1B2s', 'ACBCH6.R1B2oh', 'ACBCH6.R1B2', 
            'ACBCV8.L1B2ov', 'ACBCV8.L1B2', 
            'ACBCH7.L1B2oh', 'ACBCH7.L1B2', 
            'ACBCV7.R1B2ov', 'ACBCV7.R1B2', 
            'ACBCH8.R1B2oh', 'ACBCH8.R1B2'
            ]
    },
        
    'IR5' : {
        ' !***IR5 Optics***' : [
            'KQX.L5', 'KTQX1.L5', 'KTQX2.L5', 'KQX.R5', 'KTQX1.R5', 'KTQX2.R5'
            ],
        
        '!Beam 1' :[
            'KQ4.L5B1', 'KQ4.R5B1', 
            'KQ5.L5B1', 'KQ5.R5B1', 
            'KQ6.L5B1', 'KQ6.R5B1', 
            'KQ7.L5B1', 'KQ7.R5B1', 
            'KQ8.L5B1', 'KQ8.R5B1', 
            'KQ9.L5B1', 'KQ9.R5B1', 
            'KQ10.L5B1', 'KQ10.R5B1', 
            'KQTL11.L5B1', 'KQTL11.R5B1', 
            'KQT12.L5B1', 'KQT12.R5B1', 
            'KQT13.L5B1', 'KQT13.R5B1'
            ],
        
        '!Beam 2' : [
            'KQ4.L5B2', 'KQ4.R5B2', 
            'KQ5.L5B2', 'KQ5.R5B2', 
            'KQ6.L5B2', 'KQ6.R5B2', 
            'KQ7.L5B2', 'KQ7.R5B2', 
            'KQ8.L5B2', 'KQ8.R5B2', 
            'KQ9.L5B2', 'KQ9.R5B2', 
            'KQ10.L5B2', 'KQ10.R5B2', 
            'KQTL11.L5B2', 'KQTL11.R5B2', 
            'KQT12.L5B2', 'KQT12.R5B2', 
            'KQT13.L5B2', 'KQT13.R5B2'
            ],
        
        '!***IR5 X-scheme***' : [
            'ACBXV1.L5x', 'ACBXV1.L5s', 'ACBXV1.L5', 'ACBXV1.R5x', 'ACBXV1.R5s', 'ACBXV1.R5', 
            'ACBXH1.L5x', 'ACBXH1.L5s', 'ACBXH1.L5', 'ACBXH1.R5x', 'ACBXH1.R5s', 'ACBXH1.R5', 
            'ACBXV2.L5x', 'ACBXV2.L5s', 'ACBXV2.L5', 'ACBXV2.R5x', 'ACBXV2.R5s', 'ACBXV2.R5', 
            'ACBXH2.L5x', 'ACBXH2.L5s', 'ACBXH2.L5', 'ACBXH2.R5x', 'ACBXH2.R5s', 'ACBXH2.R5', 
            'ACBXV3.L5x', 'ACBXV3.L5s', 'ACBXV3.L5', 'ACBXV3.R5x', 'ACBXV3.R5s', 'ACBXV3.R5', 
            'ACBXH3.L5x', 'ACBXH3.L5s', 'ACBXH3.L5', 'ACBXH3.R5x', 'ACBXH3.R5s', 'ACBXH3.R5'
            ],
        
        '!Beam 1 x' :[
            'ACBYVS4.L5B1x', 'ACBYVS4.L5B1s', 'ACBYVS4.L5B1ov', 'ACBYVS4.L5B1', 
            'ACBYVS4.R5B1x', 'ACBYVS4.R5B1s', 'ACBYVS4.R5B1ov', 'ACBYVS4.R5B1', 
            'ACBCV5.L5B1x', 'ACBCV5.L5B1s', 'ACBCV5.L5B1ov', 'ACBCV5.L5B1', 
            'ACBCV6.R5B1x', 'ACBCV6.R5B1s', 'ACBCV6.R5B1ov', 'ACBCV6.R5B1', 
            'ACBYHS4.L5B1x', 'ACBYHS4.L5B1s', 'ACBYHS4.L5B1oh', 'ACBYHS4.L5B1', 
            'ACBYHS4.R5B1x', 'ACBYHS4.R5B1s', 'ACBYHS4.R5B1oh', 'ACBYHS4.R5B1', 
            'ACBCH6.L5B1x', 'ACBCH6.L5B1s', 'ACBCH6.L5B1oh', 'ACBCH6.L5B1', 
            'ACBCH5.R5B1x', 'ACBCH5.R5B1s', 'ACBCH5.R5B1oh', 'ACBCH5.R5B1', 
            'ACBCH8.L5B1oh', 'ACBCH8.L5B1', 
            'ACBCV7.L5B1ov', 'ACBCV7.L5B1', 
            'ACBCH7.R5B1oh', 'ACBCH7.R5B1', 
            'ACBCV8.R5B1ov', 'ACBCV8.R5B1'
            ],
        
        '!Beam 2 x' : [
            'ACBYVS4.L5B2x', 'ACBYVS4.L5B2s', 'ACBYVS4.L5B2ov', 'ACBYVS4.L5B2', 
            'ACBYVS4.R5B2x', 'ACBYVS4.R5B2s', 'ACBYVS4.R5B2ov', 'ACBYVS4.R5B2', 
            'ACBCV6.L5B2x', 'ACBCV6.L5B2s', 'ACBCV6.L5B2ov', 'ACBCV6.L5B2', 
            'ACBCV5.R5B2x', 'ACBCV5.R5B2s', 'ACBCV5.R5B2ov', 'ACBCV5.R5B2', 
            'ACBYHS4.L5B2x', 'ACBYHS4.L5B2s', 'ACBYHS4.L5B2oh', 'ACBYHS4.L5B2', 
            'ACBYHS4.R5B2x', 'ACBYHS4.R5B2s', 'ACBYHS4.R5B2oh', 'ACBYHS4.R5B2', 
            'ACBCH5.L5B2x', 'ACBCH5.L5B2s', 'ACBCH5.L5B2oh', 'ACBCH5.L5B2', 
            'ACBCH6.R5B2x', 'ACBCH6.R5B2s', 'ACBCH6.R5B2oh', 'ACBCH6.R5B2',
            'ACBCV8.L5B2ov', 'ACBCV8.L5B2', 
            'ACBCH7.L5B2oh', 'ACBCH7.L5B2', 
            'ACBCV7.R5B2ov', 'ACBCV7.R5B2', 
            'ACBCH8.R5B2oh', 'ACBCH8.R5B2'
            ]
    },

    'IR2' : {
        ' !***IR2 Optics***' : [
            'KQX.L2', 'KTQX1.L2', 'KTQX2.L2', 'KQX.R2', 'KTQX1.R2', 'KTQX2.R2'
            ],
        '!Beam 1 ' : [
            'KQ4.L2B1', 'KQ4.R2B1', 
            'KQ5.L2B1', 'KQ5.R2B1', 
            'KQ6.L2B1', 'KQ6.R2B1', 
            'KQ7.L2B1', 'KQ7.R2B1', 
            'KQ8.L2B1', 'KQ8.R2B1', 
            'KQ9.L2B1', 'KQ9.R2B1', 
            'KQ10.L2B1', 'KQ10.R2B1', 
            'KQTL11.L2B1', 'KQTL11.R2B1', 
            'KQT12.L2B1', 'KQT12.R2B1', 
            'KQT13.L2B1', 'KQT13.R2B1'
            ],
        
        '!Beam 2' : [
            'KQ4.L2B2', 'KQ4.R2B2', 
            'KQ5.L2B2', 'KQ5.R2B2', 
            'KQ6.L2B2', 'KQ6.R2B2', 
            'KQ7.L2B2', 'KQ7.R2B2', 
            'KQ8.L2B2', 'KQ8.R2B2', 
            'KQ9.L2B2', 'KQ9.R2B2', 
            'KQ10.L2B2', 'KQ10.R2B2', 
            'KQTL11.L2B2', 'KQTL11.R2B2', 
            'KQT12.L2B2', 'KQT12.R2B2', 
            'KQT13.L2B2', 'KQT13.R2B2'
            ],
        
        '!***IR2 X-scheme***' : [
            'abxwt.l2', 'abwmd.l2', 'abaw.r2', 'abxwt.r2', 
            'ACBXV1.L2x', 'ACBXV1.L2s', 'ACBXV1.L2', 'ACBXV1.R2x', 'ACBXV1.R2s', 'ACBXV1.R2', 
            'ACBXH1.L2x', 'ACBXH1.L2s', 'ACBXH1.L2', 'ACBXH1.R2x', 'ACBXH1.R2s', 'ACBXH1.R2', 
            'ACBXV2.L2x', 'ACBXV2.L2s', 'ACBXV2.L2', 'ACBXV2.R2x', 'ACBXV2.R2s', 'ACBXV2.R2', 
            'ACBXH2.L2x', 'ACBXH2.L2s', 'ACBXH2.L2', 'ACBXH2.R2x', 'ACBXH2.R2s', 'ACBXH2.R2', 
            'ACBXV3.L2x', 'ACBXV3.L2s', 'ACBXV3.L2', 'ACBXV3.R2x', 'ACBXV3.R2s', 'ACBXV3.R2', 
            'ACBXH3.L2x', 'ACBXH3.L2s', 'ACBXH3.L2', 'ACBXH3.R2x', 'ACBXH3.R2s', 'ACBXH3.R2'
            ],
        
        '!Beam 1 x' : [
            'ACBYVS4.L2B1x', 'ACBYVS4.L2B1s', 'ACBYVS4.L2B1o', 'ACBYVS4.L2B1ov', 'ACBYVS4.L2B1', 
            'ACBYV4.L2B1', 
            'ACBYVS4.R2B1x', 'ACBYVS4.R2B1s', 'ACBYVS4.R2B1o', 'ACBYVS4.R2B1ov', 'ACBYVS4.R2B1', 
            'ACBYVS5.L2B1x', 'ACBYVS5.L2B1s', 'ACBYVS5.L2B1o', 'ACBYVS5.L2B1ov', 'ACBYVS5.L2B1', 
            'ACBCVS5.R2B1x', 'ACBCVS5.R2B1s', 'ACBCVS5.R2B1o', 'ACBCVS5.R2B1ov', 'ACBCVS5.R2B1', 
            'ACBCV5.R2B1', 
            'ACBYHS4.L2B1x', 'ACBYHS4.L2B1s', 'ACBYHS4.L2B1a', 'ACBYHS4.L2B1oh', 'ACBYHS4.L2B1', 
            'ACBYHS4.R2B1x', 'ACBYHS4.R2B1s', 'ACBYHS4.R2B1a', 'ACBYHS4.R2B1oh', 'ACBYHS4.R2B1', 
            'ACBYH4.R2B1', 
            'ACBYHS5.L2B1x', 'ACBYHS5.L2B1s', 'ACBYHS5.L2B1a', 'ACBYHS5.L2B1oh', 'ACBYHS5.L2B1', 'ACBYH5.L2B1', 
            'ACBCHS5.R2B1x', 'ACBCHS5.R2B1s', 'ACBCHS5.R2B1a', 'ACBCHS5.R2B1oh', 'ACBCHS5.R2B1', 'ACBCH6.R2B1oh', 
            'ACBCH6.R2B1', 
            'ACBCV6.L2B1ov', 'ACBCV6.L2B1', 'ACBCH7.L2B1oh', 'ACBCH7.L2B1', 'ACBCV7.R2B1ov', 'ACBCV7.R2B1'
            ],
        
        '!Beam 2 x' : [
            'ACBYVS4.L2B2x', 'ACBYVS4.L2B2s', 'ACBYVS4.L2B2o', 'ACBYVS4.L2B2ov', 'ACBYVS4.L2B2', 
            'ACBYVS4.R2B2x', 'ACBYVS4.R2B2s', 'ACBYVS4.R2B2o', 'ACBYVS4.R2B2ov', 'ACBYVS4.R2B2', 
            'ACBYV4.R2B2', 
            'ACBYVS5.L2B2x', 'ACBYVS5.L2B2s', 'ACBYVS5.L2B2o', 'ACBYVS5.L2B2ov', 'ACBYVS5.L2B2', 'ACBYV5.L2B2', 
            'ACBCVS5.R2B2x', 'ACBCVS5.R2B2s', 'ACBCVS5.R2B2o', 'ACBCVS5.R2B2ov', 'ACBCVS5.R2B2', 
            'ACBYHS4.L2B2x', 'ACBYHS4.L2B2s', 'ACBYHS4.L2B2a', 'ACBYHS4.L2B2oh', 'ACBYHS4.L2B2', 
            'ACBYH4.L2B2', 
            'ACBYHS4.R2B2x', 'ACBYHS4.R2B2s', 'ACBYHS4.R2B2a', 'ACBYHS4.R2B2oh', 'ACBYHS4.R2B2', 
            'ACBYHS5.L2B2x', 'ACBYHS5.L2B2s', 'ACBYHS5.L2B2a', 'ACBYHS5.L2B2oh', 'ACBYHS5.L2B2', 
            'ACBCHS5.R2B2x', 'ACBCHS5.R2B2s', 'ACBCHS5.R2B2a', 'ACBCHS5.R2B2oh', 'ACBCHS5.R2B2', 
            'ACBCH5.R2B2', 
            'ACBCH6.L2B2oh', 'ACBCH6.L2B2', 'ACBCV6.R2B2ov', 'ACBCV6.R2B2', 
            'ACBCH7.R2B2oh', 'ACBCH7.R2B2', 'ACBCV7.L2B2ov', 'ACBCV7.L2B2'
            ]
    },

    'IR8' : {
        '!***IR8 Optics***' : [
            'KQX.L8', 'KTQX1.L8', 'KTQX2.L8', 'KQX.R8', 'KTQX1.R8', 'KTQX2.R8'
            ],
        
        '!Beam 1 ' : [
            'KQ4.L8B1', 'KQ4.R8B1', 
            'KQ5.L8B1', 'KQ5.R8B1', 
            'KQ6.L8B1', 'KQ6.R8B1', 
            'KQ7.L8B1', 'KQ7.R8B1', 
            'KQ8.L8B1', 'KQ8.R8B1', 
            'KQ9.L8B1', 'KQ9.R8B1', 
            'KQ10.L8B1', 'KQ10.R8B1', 
            'KQTL11.L8B1', 'KQTL11.R8B1', 
            'KQT12.L8B1', 'KQT12.R8B1', 
            'KQT13.L8B1', 'KQT13.R8B1'
            ],
        
        '! Beam 2' : [
            'KQ4.L8B2', 'KQ4.R8B2', 
            'KQ5.L8B2', 'KQ5.R8B2', 
            'KQ6.L8B2', 'KQ6.R8B2', 
            'KQ7.L8B2', 'KQ7.R8B2', 
            'KQ8.L8B2', 'KQ8.R8B2', 
            'KQ9.L8B2', 'KQ9.R8B2', 
            'KQ10.L8B2', 'KQ10.R8B2', 
            'KQTL11.L8B2', 'KQTL11.R8B2', 
            'KQT12.L8B2', 'KQT12.R8B2', 
            'KQT13.L8B2', 'KQT13.R8B2'
            ],
        
        '!***IR8 X-scheme***' : [
            'abxws.l8', 'abxwh.l8', 'ablw.r8', 'abxws.r8', 
            'ACBXV1.L8x', 'ACBXV1.L8s', 'ACBXV1.L8', 
            'ACBXV1.R8x', 'ACBXV1.R8s', 'ACBXV1.R8', 
            'ACBXH1.L8x', 'ACBXH1.L8s', 'ACBXH1.L8', 
            'ACBXH1.R8x', 'ACBXH1.R8s', 'ACBXH1.R8', 
            'ACBXV2.L8x', 'ACBXV2.L8s', 'ACBXV2.L8', 
            'ACBXV2.R8x', 'ACBXV2.R8s', 'ACBXV2.R8', 
            'ACBXH2.L8x', 'ACBXH2.L8s', 'ACBXH2.L8', 
            'ACBXH2.R8x', 'ACBXH2.R8s', 'ACBXH2.R8', 
            'ACBXV3.L8x', 'ACBXV3.L8s', 'ACBXV3.L8', 
            'ACBXV3.R8x', 'ACBXV3.R8s', 'ACBXV3.R8', 
            'ACBXH3.L8x', 'ACBXH3.L8s', 'ACBXH3.L8', 
            'ACBXH3.R8x', 'ACBXH3.R8s', 'ACBXH3.R8'
            ],
        
        '! Beam 1 x' : [
            'ACBYVS4.L8B1x', 'ACBYVS4.L8B1s', 'ACBYVS4.L8B1a', 'ACBYVS4.L8B1ov', 'ACBYVS4.L8B1', 'ACBYV4.L8B1', 
            'ACBYVS4.R8B1x', 'ACBYVS4.R8B1s', 'ACBYVS4.R8B1a', 'ACBYVS4.R8B1ov', 'ACBYVS4.R8B1', 
            'ACBCVS5.L8B1x', 'ACBCVS5.L8B1s', 'ACBCVS5.L8B1a', 'ACBCVS5.L8B1ov', 'ACBCVS5.L8B1', 
            'ACBYVS5.R8B1x', 'ACBYVS5.R8B1s', 'ACBYVS5.R8B1a', 'ACBYVS5.R8B1ov', 'ACBYVS5.R8B1', 'ACBYV5.R8B1', 
            'ACBYHS4.L8B1x', 'ACBYHS4.L8B1s', 'ACBYHS4.L8B1o', 'ACBYHS4.L8B1oh', 'ACBYHS4.L8B1', 
            'ACBYHS4.R8B1x', 'ACBYHS4.R8B1s', 'ACBYHS4.R8B1o', 'ACBYHS4.R8B1oh', 'ACBYHS4.R8B1', 'ACBYH4.R8B1', 
            'ACBCHS5.L8B1x', 'ACBCHS5.L8B1s', 'ACBCHS5.L8B1o', 'ACBCHS5.L8B1oh', 'ACBCHS5.L8B1', 'ACBCH5.L8B1', 
            'ACBYHS5.R8B1x', 'ACBYHS5.R8B1s', 'ACBYHS5.R8B1o', 'ACBYHS5.R8B1oh', 'ACBYHS5.R8B1', 'ACBCH6.R8B1oh', 'ACBCH6.R8B1', 
            'ACBCV6.L8B1ov', 'ACBCV6.L8B1', 'ACBCH7.L8B1oh', 'ACBCH7.L8B1', 
            'ACBCV7.R8B1ov', 'ACBCV7.R8B1'
            ],
        
        '! Beam 2 x' : [
            'ACBYVS4.L8B2x', 'ACBYVS4.L8B2s', 'ACBYVS4.L8B2a', 'ACBYVS4.L8B2ov', 'ACBYVS4.L8B2', 
            'ACBYVS4.R8B2x', 'ACBYVS4.R8B2s', 'ACBYVS4.R8B2a', 'ACBYVS4.R8B2ov', 'ACBYVS4.R8B2', 'ACBYV4.R8B2', 
            'ACBCVS5.L8B2x', 'ACBCVS5.L8B2s', 'ACBCVS5.L8B2a', 'ACBCVS5.L8B2ov', 'ACBCVS5.L8B2', 'ACBCV5.L8B2', 
            'ACBYVS5.R8B2x', 'ACBYVS5.R8B2s', 'ACBYVS5.R8B2a', 'ACBYVS5.R8B2ov', 'ACBYVS5.R8B2', 
            'ACBYHS4.L8B2x', 'ACBYHS4.L8B2s', 'ACBYHS4.L8B2o', 'ACBYHS4.L8B2oh', 'ACBYHS4.L8B2', 'ACBYH4.L8B2', 
            'ACBYHS4.R8B2x', 'ACBYHS4.R8B2s', 'ACBYHS4.R8B2o', 'ACBYHS4.R8B2oh', 'ACBYHS4.R8B2', 
            'ACBCHS5.L8B2x', 'ACBCHS5.L8B2s', 'ACBCHS5.L8B2o', 'ACBCHS5.L8B2oh', 'ACBCHS5.L8B2', 
            'ACBYHS5.R8B2x', 'ACBYHS5.R8B2s', 'ACBYHS5.R8B2o', 'ACBYHS5.R8B2oh', 'ACBYHS5.R8B2', 'ACBYH5.R8B2', 
            'ACBCH6.L8B2oh', 'ACBCH6.L8B2', 
            'ACBCV6.R8B2ov', 'ACBCV6.R8B2', 'ACBCH7.R8B2oh', 'ACBCH7.R8B2', 
            'ACBCV7.L8B2ov', 'ACBCV7.L8B2'
            ]
    },

    'IR4' : {
        '!***IR4 Optics***' : [],
         
        '! Beam 1 ' : [
            'KQ5.L4B1', 'KQ5.R4B1', 
            'KQ6.L4B1', 'KQ6.R4B1', 
            'KQ7.L4B1', 'KQ7.R4B1', 
            'KQ8.L4B1', 'KQ8.R4B1', 
            'KQ9.L4B1', 'KQ9.R4B1', 
            'KQ10.L4B1', 'KQ10.R4B1', 
            'KQTL11.L4B1', 'KQTL11.R4B1', 
            'KQT12.L4B1', 'KQT12.R4B1', 
            'KQT13.L4B1', 'KQT13.R4B1'
            ],
        
        '! Beam 2 ' : [
            'KQ5.L4B2', 'KQ5.R4B2', 
            'KQ6.L4B2', 'KQ6.R4B2', 
            'KQ7.L4B2', 'KQ7.R4B2', 
            'KQ8.L4B2', 'KQ8.R4B2', 
            'KQ9.L4B2', 'KQ9.R4B2', 
            'KQ10.L4B2', 'KQ10.R4B2', 
            'KQTL11.L4B2', 'KQTL11.R4B2', 
            'KQT12.L4B2', 'KQT12.R4B2', 
            'KQT13.L4B2', 'KQT13.R4B2'
            ]
    },

    'IR6' : {
        '!***IR6 Optics***' : [],
    
        '! Beam 1 ' : [
            'KQ4.L6B1', 'KQ4.R6B1', 
            'KQ5.L6B1', 'KQ5.R6B1', 
            'KQ8.L6B1', 'KQ8.R6B1', 
            'KQ9.L6B1', 'KQ9.R6B1', 
            'KQ10.L6B1', 'KQ10.R6B1', 
            'KQTL11.L6B1', 'KQTL11.R6B1', 
            'KQT12.L6B1', 'KQT12.R6B1', 
            'KQT13.L6B1', 'KQT13.R6B1'
            ],
        '! Beam 2 ' : [
            'KQ4.L6B2', 'KQ4.R6B2', 
            'KQ5.L6B2', 'KQ5.R6B2', 
            'KQ8.L6B2', 'KQ8.R6B2', 
            'KQ9.L6B2', 'KQ9.R6B2', 
            'KQ10.L6B2', 'KQ10.R6B2', 
            'KQTL11.L6B2', 'KQTL11.R6B2', 
            'KQT12.L6B2', 'KQT12.R6B2', 
            'KQT13.L6B2', 'KQT13.R6B2'
            ]
    },

    'IR3' : {
        '!***IR3 Optics***' : [
            'KQ4.LR3', 'KQT4.L3', 'KQT4.R3', 
            'KQ5.LR3', 'KQT5.L3', 'KQT5.R3'
            ],
        '! Beam 1 ' : [
            'KQ6.L3B1', 'KQ6.R3B1', 
            'KQTL7.L3B1', 'KQTL7.R3B1', 
            'KQTL8.L3B1', 'KQTL8.R3B1', 
            'KQTL9.L3B1', 'KQTL9.R3B1', 
            'KQTL10.L3B1', 'KQTL10.R3B1', 
            'KQTL11.L3B1', 'KQTL11.R3B1', 
            'KQT12.L3B1', 'KQT12.R3B1', 
            'KQT13.L3B1', 'KQT13.R3B1'
            ],
        '! Beam 2 ' : [
            'KQ6.L3B2', 'KQ6.R3B2', 
            'KQTL7.L3B2', 'KQTL7.R3B2', 
            'KQTL8.L3B2', 'KQTL8.R3B2', 
            'KQTL9.L3B2', 'KQTL9.R3B2', 
            'KQTL10.L3B2', 'KQTL10.R3B2', 
            'KQTL11.L3B2', 'KQTL11.R3B2', 
            'KQT12.L3B2', 'KQT12.R3B2', 
            'KQT13.L3B2', 'KQT13.R3B2'
            ]   
    },

    'IR7' : {
        '!***IR7 Optics***' : [
            'KQ4.LR7', 'KQT4.L7', 'KQT4.R7', 
            'KQ5.LR7', 'KQT5.L7', 'KQT5.R7'
            ],
        '! Beam 1 ' : [
            'KQ6.L7B1', 'KQ6.R7B1', 
            'KQTL7.L7B1', 'KQTL7.R7B1', 
            'KQTL8.L7B1', 'KQTL8.R7B1', 
            'KQTL9.L7B1', 'KQTL9.R7B1', 
            'KQTL10.L7B1', 'KQTL10.R7B1', 
            'KQTL11.L7B1', 'KQTL11.R7B1', 
            'KQT12.L7B1', 'KQT12.R7B1', 
            'KQT13.L7B1', 'KQT13.R7B1'
            ],
        
        '! Beam 2 ' : [
            'KQ6.L7B2', 'KQ6.R7B2', 
            'KQTL7.L7B2', 'KQTL7.R7B2', 
            'KQTL8.L7B2', 'KQTL8.R7B2', 
            'KQTL9.L7B2', 'KQTL9.R7B2', 
            'KQTL10.L7B2', 'KQTL10.R7B2', 
            'KQTL11.L7B2', 'KQTL11.R7B2', 
            'KQT12.L7B2', 'KQT12.R7B2', 
            'KQT13.L7B2', 'KQT13.R7B2'
            ]   
    },

    'ARC' : {
        '!***Arc Optics***' : [],
        
        '!QF/QD' : [
            'KQF.A81', 'KQF.A12', 'KQF.A45', 'KQF.A56', 
            'KQD.A81', 'KQD.A12', 'KQD.A45', 'KQD.A56', 
            'KQF.A78', 'KQF.A23', 'KQF.A34', 'KQF.A67', 
            'KQD.A78', 'KQD.A23', 'KQD.A34', 'KQD.A67'
            ],
        
        '!QTF/QTD BEAM1' : [
            'dQx.b1', 'dQy.b1', 'dQx.b1_sq', 'dQy.b1_sq',
            'KQTF.A81B1', 'KQTF.A12B1', 'KQTF.A45B1', 'KQTF.A56B1', 
            'KQTD.A81B1', 'KQTD.A12B1', 'KQTD.A45B1', 'KQTD.A56B1', 
            'KQTF.A78B1', 'KQTF.A23B1', 'KQTF.A34B1', 'KQTF.A67B1', 
            'KQTD.A78B1', 'KQTD.A23B1', 'KQTD.A34B1', 'KQTD.A67B1'
            ],
        
        '!QTF/QTD BEAM2' : [
            'dQx.b2', 'dQy.b2', 'dQx.b2_sq', 'dQy.b2_sq',
            'KQTF.A81B2', 'KQTF.A12B2', 'KQTF.A45B2', 'KQTF.A56B2', 
            'KQTD.A81B2', 'KQTD.A12B2', 'KQTD.A45B2', 'KQTD.A56B2', 
            'KQTF.A78B2', 'KQTF.A23B2', 'KQTF.A34B2', 'KQTF.A67B2', 
            'KQTD.A78B2', 'KQTD.A23B2', 'KQTD.A34B2', 'KQTD.A67B2'
            ],
        
        '!Sextupole BEAM1' : [
            'dQpx.b1', 'dQpy.b1', 'dQpx.b1_sq', 'dQpy.b1_sq'
            ],
        '!Strong sextupoles of sectors 81/12/45/56 BEAM1' : [
            'KSF1.A81B1', 'KSF1.A12B1', 'KSF1.A45B1', 'KSF1.A56B1', 
            'KSD2.A81B1', 'KSD2.A12B1', 'KSD2.A45B1', 'KSD2.A56B1'
            ],
        
        '!Weak sextupoles of sectors 81/12/45/56 BEAM1' : [
            'KSF2.A81B1', 'KSF2.A12B1', 'KSF2.A45B1', 'KSF2.A56B1', 
            'KSD1.A81B1', 'KSD1.A12B1', 'KSD1.A45B1', 'KSD1.A56B1'
            ],
        
        '!Weak sextupoles of sectors 78/23/34/67 BEAM1' : [
            'KSF1.A78B1', 'KSF2.A78B1', 'KSF1.A23B1', 'KSF2.A23B1', 'KSF1.A34B1', 'KSF2.A34B1', 'KSF1.A67B1', 'KSF2.A67B1', 
            'KSD1.A78B1', 'KSD2.A78B1', 'KSD1.A23B1', 'KSD2.A23B1', 'KSD1.A34B1', 'KSD2.A34B1', 'KSD1.A67B1', 'KSD2.A67B1'
            ],
        
        '!Sextupole BEAM2' : [
            'dQpx.b2', 'dQpy.b2', 'dQpx.b2_sq', 'dQpy.b2_sq'
            ],
        
        '!Strong sextupoles of sectors 81/12/45/56 BEAM2' : [
            'KSF2.A81B2', 'KSF2.A12B2', 'KSF2.A45B2', 'KSF2.A56B2', 
            'KSD1.A81B2', 'KSD1.A12B2', 'KSD1.A45B2', 'KSD1.A56B2'
            ],
        
        '!Weak sextupoles of sectors 81/12/45/56 BEAM2' : [
            'KSF1.A81B2', 'KSF1.A12B2', 'KSF1.A45B2', 'KSF1.A56B2', 
            'KSD2.A81B2', 'KSD2.A12B2', 'KSD2.A45B2', 'KSD2.A56B2'
            ],
        
        '!Weak sextupoles of sectors 78/23/34/67 BEAM2' : [
            'KSF1.A78B2', 'KSF2.A78B2', 'KSF1.A23B2', 'KSF2.A23B2', 'KSF1.A34B2', 'KSF2.A34B2', 'KSF1.A67B2', 'KSF2.A67B2', 
            'KSD1.A78B2', 'KSD2.A78B2', 'KSD1.A23B2', 'KSD2.A23B2', 'KSD1.A34B2', 'KSD2.A34B2', 'KSD1.A67B2', 'KSD2.A67B2'
            ],
        
        '!MQS BEAM1' : [
            'CMRS.b1', 'CMIS.b1', 'CMRS.b1_sq', 'CMIS.b1_sq', 'ona2_b1', 
            'KQS.R1B1', 'KQS.L2B1', 'KQS.A23B1', 'KQS.R3B1', 'KQS.L4B1', 'KQS.A45B1', 
            'KQS.R5B1', 'KQS.L6B1', 'KQS.A67B1', 'KQS.R7B1', 'KQS.L8B1', 'KQS.A81B1'
            ],
        
        '!MQS BEAM2' : [
            'CMRS.b2', 'CMIS.b2', 'CMRS.b2_sq', 'CMIS.b2_sq', 'ona2_b2',
            'KQS.A12B2', 'KQS.R2B2', 'KQS.L3B2', 'KQS.A34B2', 'KQS.R4B2', 'KQS.L5B2', 
            'KQS.A56B2', 'KQS.R6B2', 'KQS.L7B2', 'KQS.A78B2', 'KQS.R8B2', 'KQS.L1B2'
            ],
        
        '!MSS BEAM1' : [
            'ona3_b1', 
            'KSS.A12B1', 'KSS.A23B1', 'KSS.A34B1', 'KSS.A45B1', 'KSS.A56B1', 'KSS.A67B1', 'KSS.A78B1', 'KSS.A81B1'
            ],
        
        '!MSS BEAM2' : [
            'ona3_b2',
            'KSS.A12B2', 'KSS.A23B2', 'KSS.A34B2', 'KSS.A45B2', 'KSS.A56B2', 'KSS.A67B2', 'KSS.A78B2', 'KSS.A81B2'
            ],
        
        '!OF/OD BEAM1' : [
            'ON_MO.b1', 
            'KOF.B1', 'KOD.B1', 'KOF.A12B1', 'KOF.A23B1', 'KOF.A34B1', 'KOF.A45B1', 'KOF.A56B1', 'KOF.A67B1', 'KOF.A78B1', 'KOF.A81B1', 
            'KOD.A12B1', 'KOD.A23B1', 'KOD.A34B1', 'KOD.A45B1', 'KOD.A56B1', 'KOD.A67B1', 'KOD.A78B1', 'KOD.A81B1'
            ],
        
        '!OF/OD BEAM2' : [
            'ON_MO.b2', 
            'KOF.B2', 'KOD.B2', 'KOF.A12B2', 'KOF.A23B2', 'KOF.A34B2', 'KOF.A45B2', 'KOF.A56B2', 'KOF.A67B2', 'KOF.A78B2', 'KOF.A81B2', 
            'KOD.A12B2', 'KOD.A23B2', 'KOD.A34B2', 'KOD.A45B2', 'KOD.A56B2', 'KOD.A67B2', 'KOD.A78B2', 'KOD.A81B2'
            ],
        
        '!! MCB-beam1 for spurious dispersion correction' : [],
        
        '!! MCB in sector 81 and 12 BEAM1' : [
            'acbh14.r8b1x', 'acbh14.r8b1s', 'acbh14.r8b1', 'acbh16.r8b1x', 'acbh16.r8b1s', 'acbh16.r8b1', 
            'acbh14.l1b1x', 'acbh14.l1b1s', 'acbh14.l1b1', 'acbh12.l1b1x', 'acbh12.l1b1s', 'acbh12.l1b1', 
            'acbh13.r1b1x', 'acbh13.r1b1s', 'acbh13.r1b1', 'acbh15.r1b1x', 'acbh15.r1b1s', 'acbh15.r1b1', 
            'acbh15.l2b1x', 'acbh15.l2b1s', 'acbh15.l2b1', 'acbh13.l2b1x', 'acbh13.l2b1s', 'acbh13.l2b1', 
            'acbv13.r8b1x', 'acbv13.r8b1s', 'acbv13.r8b1', 'acbv15.r8b1x', 'acbv15.r8b1s', 'acbv15.r8b1', 
            'acbv15.l1b1x', 'acbv15.l1b1s', 'acbv15.l1b1', 'acbv13.l1b1x', 'acbv13.l1b1s', 'acbv13.l1b1', 
            'acbv12.r1b1x', 'acbv12.r1b1s', 'acbv12.r1b1', 'acbv14.r1b1x', 'acbv14.r1b1s', 'acbv14.r1b1', 
            'acbv16.l2b1x', 'acbv16.l2b1s', 'acbv16.l2b1', 'acbv14.l2b1x', 'acbv14.l2b1s', 'acbv14.l2b1'
            ],
        
        '!! MCB in sector 45 and 56 BEAM1' : [
            'acbh14.r4b1x', 'acbh14.r4b1s', 'acbh14.r4b1', 'acbh16.r4b1x', 'acbh16.r4b1s', 'acbh16.r4b1', 
            'acbh14.l5b1x', 'acbh14.l5b1s', 'acbh14.l5b1', 'acbh12.l5b1x', 'acbh12.l5b1s', 'acbh12.l5b1', 
            'acbh13.r5b1x', 'acbh13.r5b1s', 'acbh13.r5b1', 'acbh15.r5b1x', 'acbh15.r5b1s', 'acbh15.r5b1', 
            'acbh15.l6b1x', 'acbh15.l6b1s', 'acbh15.l6b1', 'acbh13.l6b1x', 'acbh13.l6b1s', 'acbh13.l6b1', 
            'acbv13.r4b1x', 'acbv13.r4b1s', 'acbv13.r4b1', 'acbv15.r4b1x', 'acbv15.r4b1s', 'acbv15.r4b1', 
            'acbv15.l5b1x', 'acbv15.l5b1s', 'acbv15.l5b1', 'acbv13.l5b1x', 'acbv13.l5b1s', 'acbv13.l5b1', 
            'acbv12.r5b1x', 'acbv12.r5b1s', 'acbv12.r5b1', 'acbv14.r5b1x', 'acbv14.r5b1s', 'acbv14.r5b1', 
            'acbv16.l6b1x', 'acbv16.l6b1s', 'acbv16.l6b1', 'acbv14.l6b1x', 'acbv14.l6b1s', 'acbv14.l6b1'
            ],
        
        '!! MCB-beam2 for spurious dispersion correction' :  [],
        
        '!! MCB in sector 81 and 12 BEAM2' : [
            'acbh13.r8b2x', 'acbh13.r8b2s', 'acbh13.r8b2', 'acbh15.r8b2x', 'acbh15.r8b2s', 'acbh15.r8b2', 
            'acbh15.l1b2x', 'acbh15.l1b2s', 'acbh15.l1b2', 'acbh13.l1b2x', 'acbh13.l1b2s', 'acbh13.l1b2', 
            'acbh12.r1b2x', 'acbh12.r1b2s', 'acbh12.r1b2', 'acbh14.r1b2x', 'acbh14.r1b2s', 'acbh14.r1b2', 
            'acbh16.l2b2x', 'acbh16.l2b2s', 'acbh16.l2b2', 'acbh14.l2b2x', 'acbh14.l2b2s', 'acbh14.l2b2', 
            'acbv14.r8b2x', 'acbv14.r8b2s', 'acbv14.r8b2', 'acbv16.r8b2x', 'acbv16.r8b2s', 'acbv16.r8b2', 
            'acbv14.l1b2x', 'acbv14.l1b2s', 'acbv14.l1b2', 'acbv12.l1b2x', 'acbv12.l1b2s', 'acbv12.l1b2', 
            'acbv13.r1b2x', 'acbv13.r1b2s', 'acbv13.r1b2', 'acbv15.r1b2x', 'acbv15.r1b2s', 'acbv15.r1b2', 
            'acbv15.l2b2x', 'acbv15.l2b2s', 'acbv15.l2b2', 'acbv13.l2b2x', 'acbv13.l2b2s', 'acbv13.l2b2'
            ],
        
        '!! MCB in sector 45 and 56 BEAM2' : [
            'acbh13.r4b2x', 'acbh13.r4b2s', 'acbh13.r4b2', 'acbh15.r4b2x', 'acbh15.r4b2s', 'acbh15.r4b2', 
            'acbh15.l5b2x', 'acbh15.l5b2s', 'acbh15.l5b2', 'acbh13.l5b2x', 'acbh13.l5b2s', 'acbh13.l5b2', 
            'acbh12.r5b2x', 'acbh12.r5b2s', 'acbh12.r5b2', 'acbh14.r5b2x', 'acbh14.r5b2s', 'acbh14.r5b2', 
            'acbh16.l6b2x', 'acbh16.l6b2s', 'acbh16.l6b2', 'acbh14.l6b2x', 'acbh14.l6b2s', 'acbh14.l6b2', 
            'acbv14.r4b2x', 'acbv14.r4b2s', 'acbv14.r4b2', 'acbv16.r4b2x', 'acbv16.r4b2s', 'acbv16.r4b2', 
            'acbv14.l5b2x', 'acbv14.l5b2s', 'acbv14.l5b2', 'acbv12.l5b2x', 'acbv12.l5b2s', 'acbv12.l5b2', 
            'acbv13.r5b2x', 'acbv13.r5b2s', 'acbv13.r5b2', 'acbv15.r5b2x', 'acbv15.r5b2s', 'acbv15.r5b2', 
            'acbv15.l6b2x', 'acbv15.l6b2s', 'acbv15.l6b2', 'acbv13.l6b2x', 'acbv13.l6b2s', 'acbv13.l6b2'
            ], 
    },

    'SUMM' : {
        '!****OPTICS SUMMARY****' : [],
        
        '!Tune and Chroma' : [
            'Qxb1', 'Qyb1', 'Qpxb1', 'Qpyb1', 'dmux15b1', 'dmuy15b1', 
            'Qxb2', 'Qyb2', 'Qpxb2', 'Qpyb2', 'dmux15b2', 'dmuy15b2',
            ],
        
        '!IR Optics summary (phase, twiss param., dispersion)' : [
            'muxIP1b1', 'muyIP1b1', 'muxIP1b1_L', 'muyIP1b1_L', 'muxIP1b1_R', 'muyIP1b1_R', 'betxIP1b1', 'betyIP1b1', 'alfxIP1b1', 'alfyIP1b1', 'dxIP1b1', 'dpxIP1b1',  
            'muxIP1b2', 'muyIP1b2', 'muxIP1b2_L', 'muyIP1b2_L', 'muxIP1b2_R', 'muyIP1b2_R', 'betxIP1b2', 'betyIP1b2', 'alfxIP1b2', 'alfyIP1b2', 'dxIP1b2', 'dpxIP1b2',  
            'muxIP5b1', 'muyIP5b1', 'muxIP5b1_L', 'muyIP5b1_L', 'muxIP5b1_R', 'muyIP5b1_R', 'betxIP5b1', 'betyIP5b1', 'alfxIP5b1', 'alfyIP5b1', 'dxIP5b1', 'dpxIP5b1', 
            'muxIP5b2', 'muyIP5b2', 'muxIP5b2_L', 'muyIP5b2_L', 'muxIP5b2_R', 'muyIP5b2_R', 'betxIP5b2', 'betyIP5b2', 'alfxIP5b2', 'alfyIP5b2', 'dxIP5b2', 'dpxIP5b2',
            'muxIP2b1', 'muyIP2b1', 'betxIP2b1', 'betyIP2b1', 'alfxIP2b1', 'alfyIP2b1', 'dxIP2b1', 'dpxIP2b1', 
            'muxIP2b2', 'muyIP2b2', 'betxIP2b2', 'betyIP2b2', 'alfxIP2b2', 'alfyIP2b2', 'dxIP2b2', 'dpxIP2b2', 
            'muxIP8b1', 'muyIP8b1', 'betxIP8b1', 'betyIP8b1', 'alfxIP8b1', 'alfyIP8b1', 'dxIP8b1', 'dpxIP8b1',
            'muxIP8b2', 'muyIP8b2', 'betxIP8b2', 'betyIP8b2', 'alfxIP8b2', 'alfyIP8b2', 'dxIP8b2', 'dpxIP8b2',
            'muxIP4b1', 'muyIP4b1', 'betxIP4b1', 'betyIP4b1', 'alfxIP4b1', 'alfyIP4b1', 'dxIP4b1', 'dpxIP4b1',
            'muxIP4b2', 'muyIP4b2', 'betxIP4b2', 'betyIP4b2', 'alfxIP4b2', 'alfyIP4b2', 'dxIP4b2', 'dpxIP4b2',
            'muxIP6b1', 'muyIP6b1', 'betxIP6b1', 'betyIP6b1', 'alfxIP6b1', 'alfyIP6b1', 'dxIP6b1', 'dpxIP6b1', 
            'muxIP6b2', 'muyIP6b2', 'betxIP6b2', 'betyIP6b2', 'alfxIP6b2', 'alfyIP6b2', 'dxIP6b2', 'dpxIP6b2',
            'muxIP3b1', 'muyIP3b1', 'betxIP3b1', 'betyIP3b1', 'alfxIP3b1', 'alfyIP3b1', 'dxIP3b1', 'dpxIP3b1',
            'muxIP3b2', 'muyIP3b2', 'betxIP3b2', 'betyIP3b2', 'alfxIP3b2', 'alfyIP3b2', 'dxIP3b2', 'dpxIP3b2', 
            'muxIP7b1', 'muyIP7b1', 'betxIP7b1', 'betyIP7b1', 'alfxIP7b1', 'alfyIP7b1', 'dxIP7b1', 'dpxIP7b1',
            'muxIP7b2', 'muyIP7b2', 'betxIP7b2', 'betyIP7b2', 'alfxIP7b2', 'alfyIP7b2', 'dxIP7b2', 'dpxIP7b2',
            ], 
            
        '!Xscheme summary in IR1, IR2,IR5 and IR8' : [
            'xIP1b1', 'yIP1b1', 'pxIP1b1', 'pyIP1b1', 'xIP1b2', 'yIP1b2', 'pxIP1b2', 'pyIP1b2',
            'xIP2b1', 'yIP2b1', 'pxIP2b1', 'pyIP2b1', 'xIP2b2', 'yIP2b2', 'pxIP2b2', 'pyIP2b2',
            'xIP5b1', 'yIP5b1', 'pxIP5b1', 'pyIP5b1', 'xIP5b2', 'yIP5b2', 'pxIP5b2', 'pyIP5b2',
            'xIP8b1', 'yIP8b1', 'pxIP8b1', 'pyIP8b1', 'xIP8b2', 'yIP8b2', 'pxIP8b2', 'pyIP8b2'
            ],
        
        '!Arc Optics summary' : [
            'muxcell81b1', 'muycell81b1', 'mux81b1', 'muy81b1', 
            'muxcell45b1', 'muycell45b1', 'mux45b1', 'muy45b1',
            'muxcell12b2', 'muycell12b2', 'mux12b2', 'muy12b2', 
            'muxcell56b2', 'muycell56b2', 'mux56b2', 'muy56b2', 
            'muxcell12b1', 'muycell12b1', 'mux12b1', 'muy12b1', 
            'muxcell56b1', 'muycell56b1', 'mux56b1', 'muy56b1',
            'muxcell81b2', 'muycell81b2', 'mux81b2', 'muy81b2', 
            'muxcell45b2', 'muycell45b2', 'mux45b2', 'muy45b2', 
            'muxcell23b1', 'muycell23b1', 'mux23b1', 'muy23b1', 
            'muxcell78b2', 'muycell78b2', 'mux78b2', 'muy78b2',
            'muxcell34b1', 'muycell34b1', 'mux34b1', 'muy34b1',
            'muxcell67b2', 'muycell67b2', 'mux67b2', 'muy67b2', 
            'muxcell67b1', 'muycell67b1', 'mux67b1', 'muy67b1', 
            'muxcell34b2', 'muycell34b2', 'mux34b2', 'muy34b2', 
            'muxcell78b1', 'muycell78b1', 'mux78b1', 'muy78b1', 
            'muxcell23b2', 'muycell23b2', 'mux23b2', 'muy23b2',
            ]
    }
}

def madx_var_def(mymad, var):
    vv = mymad._libmadx.get_var(var)
    if isinstance(vv.definition, str):
        return (f'{var:20s}:= {vv.definition:20s};')
    if isinstance(vv.definition, (int, float)):
        return (f'{var:20s}:= {vv.definition:>19.12E};')

def global_variables(mymad):
    savelines = []
    for v in ['NRJ', 'ARC_SQUEEZE']:
        savelines.append(madx_var_def(mymad, v)) 
    return savelines
        
def ip15_betas(mymad):
    savelines = []
    savelines.append('\n! *** BETAS in IP1, IP2, IP5 and IP8**')
    for i in [1,2,5,8]:
        for p in ['x','y']:
            v = f"bet{p}_IP{str(i)}"
            savelines.append(madx_var_def(mymad, v)) 
    return savelines

def ip15_teleindex(mymad):
    savelines = []
    savelines.append('\n!***TELE-INDEX in IR1 and IR5***')
    for i in [1,5]:
        for p in ['x','y']:
            v = f"r{p}_IP{str(i)}"
            savelines.append(madx_var_def(mymad, v)) 
    return savelines

def exp_configuration(mymad):
    savelines = []
    savelines.append('\n!***Exp. configuration in IR1, IR2, IR5 and IR8***')
    for i in [1,5]:
        for p in ['on_x', 'on_sep', 'on_oh', 'on_ov', 'phi_IR'] :
            v = f"{p}{str(i)}"
            savelines.append(madx_var_def(mymad, v)) 
        for p in ['on_ssep', 'on_xx']:
            v = f"{p}{str(i)}"
            savelines.append(madx_var_def(mymad, v)) 
    return savelines

def disp_correction(mymad):
    savelines = []
    savelines.append('\n!**Spurious dispersion correction')
    v = 'on_disp'
    savelines.append(madx_var_def(mymad, v)) 
    return savelines

def xing_scheme(mymad):
    savelines = []
    savelines.append('\n')
    for i in [2, 8]:
        for p in ['h', 'v']:
            v = f"on_x{str(i)}{p}"
            savelines.append(madx_var_def(mymad, v))
            v = f"on_sep{str(i)}{p}"
            savelines.append(madx_var_def(mymad, v))
        v = f"on_a{str(i)}"
        savelines.append(madx_var_def(mymad, v))
        v = f"on_o{str(i)}"
        savelines.append(madx_var_def(mymad, v))
        for p in ['h', 'v']:
            v = f"on_o{p}{str(i)}"
            savelines.append(madx_var_def(mymad, v))
        v = f"phi_IR{str(i)}"
        savelines.append(madx_var_def(mymad, v))
    return savelines

def exp_solenoids(mymad):
    savelines = []
    savelines.append('\n!** Experimental solenoids')
    for v in ['abas', 'abls', 'abcs']:
        savelines.append(madx_var_def(mymad, v)) 
    return savelines
        
def ring_geometry(mymad):
    savelines = []
    savelines.append('\n!***Ring Geometry***')
    savelines.append('\n!Separation/recombination dipoles')
    for v in mymad.globals :
        if v.find('kd')==0 or v.find('ksumd') == 0 :
            savelines.append(madx_var_def(mymad, v)) 
    savelines.append('\n!Main dipoles')
    for v in mymad.globals :
        if v.find('kb')==0 :
            savelines.append(madx_var_def(mymad, v)) 
    return savelines

def get_optics(mymad, what):
    savelines = []
    for w in optics_data[what].keys():
            savelines.append(w)
            for v in optics_data[what][w]:
                savelines.append(madx_var_def(mymad, v))
    return savelines

def ir_optics(mymad, ip):
    ip = ip.upper()
    return get_optics(mymad, ip)

def arc_optics(mymad):
    return get_optics(mymad, 'ARC')

def summ_optics(mymad):
    return get_optics(mymad, 'SUMM')
    
def save_lhc_optics(mymad, fout, verbose=False):
    savelines = []
    
    savelines.append(global_variables(mymad))
    savelines.append(ip15_betas(mymad))
    savelines.append(ip15_teleindex(mymad))
    savelines.append(exp_configuration(mymad))
    savelines.append(disp_correction(mymad))
    savelines.append(xing_scheme(mymad))
    savelines.append(exp_solenoids(mymad))
    savelines.append(ring_geometry(mymad))
    for i in [1, 5, 2, 8, 4, 6, 3, 7]:
        savelines.append(ir_optics(mymad, f'IR{i}'))
    savelines.append(arc_optics(mymad))
    savelines.append(summ_optics(mymad))
    
    savelines.append(['\nreturn;'])
    
    savelines = "\n".join([j for i in savelines for j in i])
    if fout :
        print(f' --- current LHC optics will be saved to {fout}')
        OF =  open(fout, 'w')
        OF.write(savelines)
        OF.close()
    if verbose:
        print(savelines)
        
    return savelines

#########################################################################
# Test functions used to 
#  - get the MAD-X variables
#  - save the data
#########################################################################

def get_variables_from_optiics_file(f):
    ''' get the variables stored in the selected file'''
    INF = open(f'run/temp/{f}.madx')
    optinj = INF.readlines()
    f0 = False
    f1  = False
    to_print = False
    var_list = []
    for line in optinj:
        if line.find('***Arc Optics***')>0:
            to_print = True
        if line.find('***OPTICS SUMARY***')>0:
            to_print = False
            
        if to_print:
            # print(line)
            var_list.append(line[:line.find(':=')].rstrip())
    print(var_list)
    return

            
def print_ip15_optics(mymad, ip):
    print (f'\n!***IR{str(ip)} Optics***')
    for k in ['KQX.L', 'KTQX1.L', 'KTQX2.L']:
        v = f"{k}{str(ip)}"
        print(f'{v:12s}:= {mymad._libmadx.get_var(v)():>19.12E};')
    for k in ['KQX.R', 'KTQX1.R', 'KTQX2.R']:
        v = f"{k}{str(ip)}"
        print(f'{v:12s}:= {mymad._libmadx.get_var(v)():13s};')

    for beam in [1, 2]:
        print (f'\n !Beam{beam}')
        for n in np.arange(4, 14):
            for side in ['L', 'R']:
                if n < 11 :
                    v = f'KQ{n}.{side}{ip}B{beam}'
                elif n == 11:
                    v = f'KQTL11.{side}{ip}B{beam}'
                else:
                    v = f'KQT{n}.{side}{ip}B{beam}'

                print(f'{v:12s}:= {mymad._libmadx.get_var(v)():>19.12E};')

    print (f'\n !***IR{ip} X-scheme***')
    if ip == 2:
        for v in ['ABXWT.L2', 'ABWMD.L2', 'ABAW.R2', 'ABXWT.R2']:
            print(f'{v:12s}:= {mymad._libmadx.get_var(v)():20s};')
    for n in np.arange(1, 4):
        for p in ['V','H']:
            for side in ['L','R']:
                v = f'ACBX{p}{n}.{side}{ip}x'
                print(f'{v:12s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'ACBX{p}{n}.{side}{ip}s'
                print(f'{v:12s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'ACBX{p}{n}.{side}{ip}'
                print(f'{v:12s}:= {mymad._libmadx.get_var(v)():80s};')

    for beam in [1, 2]:
        print(f'\n!Beam1')
        k  = 'ACBYVS4'
        for side in ['L', 'R']:
            v = f'{k}.{side}{ip}B{beam}x'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.{side}{ip}B{beam}s'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.{side}{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.{side}{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
   
        if beam == 1 :
            k = 'ACBCV5'
            for x in ['x', 's', 'ov']:
                v = f'{k}.L{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV6'
            for x in ['x', 's', 'ov']:
                v = f'{k}.R{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k  = 'ACBYHS4'
            for side in ['L', 'R']:
                v = f'{k}.{side}{ip}B{beam}x'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}s'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            
            k = 'ACBCH6'
            for x in ['x', 's', 'oh']:
                v = f'{k}.L{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH5'
            for x in ['x', 's', 'oh']:
                v = f'{k}.R{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH8'
            v = f'{k}.L{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV7'
            v = f'{k}.L{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH7'
            v = f'{k}.R{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV8'
            v = f'{k}.R{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
        else:
            k = 'ACBCV6'
            for x in ['x', 's', 'ov']:
                v = f'{k}.L{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV5'
            for x in ['x', 's', 'ov']:
                v = f'{k}.R{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k  = 'ACBYHS4'
            for side in ['L', 'R']:
                v = f'{k}.{side}{ip}B{beam}x'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}s'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            
            k = 'ACBCH5'
            for x in ['x', 's', 'oh']:
                v = f'{k}.L{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH6'
            for x in ['x', 's', 'oh']:
                v = f'{k}.R{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV8'
            v = f'{k}.L{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH7'
            v = f'{k}.L{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV7'
            v = f'{k}.R{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH8'
            v = f'{k}.R{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')



def print_ip2_optics(mymad, ip):
    print (f'\n!***IR{str(ip)} Optics***')
    for k in ['KQX.L', 'KTQX1.L', 'KTQX2.L']:
        v = f"{k}{str(ip)}"
        print(f'{v:12s}:= {mymad._libmadx.get_var(v)():>19.12E};')
    for k in ['KQX.R', 'KTQX1.R', 'KTQX2.R']:
        v = f"{k}{str(ip)}"
        print(f'{v:12s}:= {mymad._libmadx.get_var(v)():13s};')

    for beam in [1, 2]:
        print (f'\n !Beam{beam}')
        for n in np.arange(4, 14):
            for side in ['L', 'R']:
                if n < 11 :
                    v = f'KQ{n}.{side}{ip}B{beam}'
                elif n == 11:
                    v = f'KQTL11.{side}{ip}B{beam}'
                else:
                    v = f'KQT{n}.{side}{ip}B{beam}'

                print(f'{v:12s}:= {mymad._libmadx.get_var(v)():>19.12E};')

    print (f'\n !***IR{ip} X-scheme***')
    if ip == 2:
        for v in ['ABXWT.L2', 'ABWMD.L2', 'ABAW.R2', 'ABXWT.R2']:
            print(f'{v:12s}:= {mymad._libmadx.get_var(v)():20s};')
    for n in np.arange(1, 4):
        for p in ['V','H']:
            for side in ['L','R']:
                v = f'ACBX{p}{n}.{side}{ip}x'
                print(f'{v:12s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'ACBX{p}{n}.{side}{ip}s'
                print(f'{v:12s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'ACBX{p}{n}.{side}{ip}'
                print(f'{v:12s}:= {mymad._libmadx.get_var(v)():80s};')

    for beam in [1, 2]:
        print(f'\n!Beam1')
        k  = 'ACBYVS4'
        for side in ['L', 'R']:
            v = f'{k}.{side}{ip}B{beam}x'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.{side}{ip}B{beam}s'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.{side}{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.{side}{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
   
        if beam == 1 :
            k = 'ACBCV5'
            for x in ['x', 's', 'ov']:
                v = f'{k}.L{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV6'
            for x in ['x', 's', 'ov']:
                v = f'{k}.R{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k  = 'ACBYHS4'
            for side in ['L', 'R']:
                v = f'{k}.{side}{ip}B{beam}x'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}s'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            
            k = 'ACBCH6'
            for x in ['x', 's', 'oh']:
                v = f'{k}.L{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH5'
            for x in ['x', 's', 'oh']:
                v = f'{k}.R{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH8'
            v = f'{k}.L{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV7'
            v = f'{k}.L{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH7'
            v = f'{k}.R{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV8'
            v = f'{k}.R{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
        else:
            k = 'ACBCV6'
            for x in ['x', 's', 'ov']:
                v = f'{k}.L{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV5'
            for x in ['x', 's', 'ov']:
                v = f'{k}.R{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k  = 'ACBYHS4'
            for side in ['L', 'R']:
                v = f'{k}.{side}{ip}B{beam}x'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}s'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
                v = f'{k}.{side}{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            
            k = 'ACBCH5'
            for x in ['x', 's', 'oh']:
                v = f'{k}.L{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH6'
            for x in ['x', 's', 'oh']:
                v = f'{k}.R{ip}B{beam}{x}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV8'
            v = f'{k}.L{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH7'
            v = f'{k}.L{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.L{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCV7'
            v = f'{k}.R{ip}B{beam}ov'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
            k = 'ACBCH8'
            v = f'{k}.R{ip}B{beam}oh'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():>19.12E};')
            v = f'{k}.R{ip}B{beam}'; print(f'{v:16s}:= {mymad._libmadx.get_var(v)():20s};')
    