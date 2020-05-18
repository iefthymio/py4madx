#
# -- slice a normal distribution to equal area (charge) slices
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

def qslice(qtot, sigma, nslices):
    assert nslices%2 == 1, 'Nslices must be 1 or odd number'
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
        df['id'] = np.arange(-np.int(nslices/2), np.int(nslices/2)+1)
        df.at[df.index[df['id'] == 0],'spos'] = 1.0e-9
        df['charge'] = qslice
    elif nslices == 1 :
        df = pd.DataFrame({'spos':1.0e-9,'charge':qtot,'id':0})
    else:
        raise ValueError(' qslice2 : wrong input value.')
    return df

if __name__ in '__main__':
   
    df = qslice(1.1e11, 3.0, 15)
    df.head()