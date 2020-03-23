#
# -- code to slice a normal distribution to equal area (charge) slices
#
import numpy as np
import pandas as pd
from scipy import special

def fnorm(x,mu,sig):   # --- normal distribution with (mu, sigma)
    return 1/(sig*np.sqrt(2*np.pi))*np.exp(-0.5*(x-mu)**2/sig**2)

def normzp(p, mu, sig):  # --- Quantile function of normal distribution with (mu, sigma)
    return mu + sig*np.sqrt(2)*special.erfinv(2*p-1)

def bari(x1, x2, mu, sig, scharge): 
    return sig**2*(fnorm(x1, mu, sig) - fnorm(x2, mu, sig))/scharge


def _fnorm(x):
    return np.exp(-0.5*x*x)/np.sqrt(2*np.pi)

def _myerf(x): # --- Normal distribution integral (half range [0,inf]) with u=0, sigma=1
    return 0.5*special.erf(x/np.sqrt(2)) 

def _arcerf(y): # --- Inverse error function of normal distribution (Quantile function)
    return np.sqrt(2)*special.erfinv(2*y)

def _bari(y1, y2):
    x1 = _arcerf(y1)
    x2 = _arcerf(y2)
    bari = np.abs(_fnorm(x2)-_fnorm(x1))/(y2-y1)
    return bari

def _qslice(n):
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
        spos.append(_bari(y1,y2))
        y1 = y2
        y2 = y2 + scharge
        charge.append(scharge)
    x = _arcerf(y1)
    # spos.append(np.exp(-0.5*x*x)/scharge/ractwopi)
    spos.append(_fnorm(x)/scharge)
    charge.append(scharge)

    df = pd.DataFrame()
    df['spos'] = spos
    df['charge'] = charge
    return df

def qslice(qtot, sigma, nslices):
    if nslices > 1 : 
        qslice = 1.0 / float(nslices)           # --- slice charge
        qsint = np.arange(1, nslices) * qslice  # --- integrated slice charge
        si = normzp(qsint, 0.0, sigma)          # --- s-position per slice
        spos = []
        spos.append(-sigma**2*fnorm(si[0], 0.0, sigma)/qslice)
        [spos.append(bari(si[i], si[i+1], 0.0, sigma, qslice)) for i in np.arange(len(si)-1)]
        spos.append(sigma**2*fnorm(si[-1], 0.0, sigma)/qslice)
        df = pd.DataFrame()
        df['spos'] = spos
        df['charge'] = qslice
    elif nslices == 1 :
        df = pd.DataFrame({'spos':1.0e-9,'charge':qtot})
    elif nslices == 0 :
        df = pd.DataFrame()
    else:
        raise ValueError(' qslice2 : wrong input value.')
    return df