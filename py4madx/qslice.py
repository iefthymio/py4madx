#
# -- code to slice a normal distribution to equal area (charge) slices
#
import numpy as np
import pandas as pd
from scipy import special

def fnorm(x):
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
