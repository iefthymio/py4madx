
#######################################################################################
# plotting functions
# taken from BBlumi web : 
#   http://bblumi.web.cern.ch/how-tos/ExamplesOfLattices/ExamplesOfLattices/#the-proton-synchrotron-booster
#######################################################################################

import numpy as np
import pandas as pd
import itertools

from . import pmadx
# import pmadx

import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.patches as patches

__version__ = '1.0 - (ie) 28.01.2022'


def plotLatticeSeries(ax,series, height=1., v_offset=0., color='r',alpha=0.5):
    aux=series
    ax.add_patch(
    patches.Rectangle(
        (aux.s-aux.l, v_offset-height/2.),   # (x,y)
        aux.l,          # width
        height,          # height
        color=color, alpha=alpha
    )
    )
    return;

def _plot_optip(dftwiss, bim, ip, title=''):
    ''' Plot optics around an LHC IP '''

    beamid = bim[-2:].lower()
    ipnum = ip[-1:]
    df_ip = dftwiss[dftwiss['beam']==bim].loc[f's.ds.l{ipnum}.{beamid}':f'e.ds.r{ipnum}.{beamid}']

    betx = df_ip[df_ip['beam']==bim].loc[ip].betx
    bety = df_ip[df_ip['beam']==bim].loc[ip].bety
    print(f'IP {ip} Beam {bim} beta values = {betx} {bety}')

    fig = plt.figure(figsize=(13,8))
    # set up subplot grid
    #gridspec.GridSpec(3,3)

    ax1=plt.subplot2grid((3,1), (0,0), colspan=1, rowspan=1)
    plt.plot(df_ip['s'],0*df_ip['s'],'k')

    DF=df_ip[(df_ip['keyword']=='quadrupole')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(plt.gca(), aux, height=aux.k1l, v_offset=aux.k1l/2, color='r')

    color = 'red'
    ax1.set_ylabel('1/f=K1L [m$^{-1}$]', color=color)  # we already handled the x-label with ax1
    ax1.tick_params(axis='y', labelcolor=color)
    plt.grid()
    plt.ylim(-.05,.05)
    # plt.title('CERN Large Hadron Collider, Beam 1, Injection Optics 2016, Q1='+format(madx.table.summ.Q1[0],'2.3f')+', Q2='+ format(madx.table.summ.Q2[0],'2.3f'))
    plt.title(title)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'blue'
    ax2.set_ylabel('$\\theta$=K0L [mrad]', color=color)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor=color)

    DF=df_ip[(df_ip['keyword']=='rbend')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(ax2, aux, height=aux.angle*1000, v_offset=aux.angle/2*1000, color='b')

    DF=df_ip[(df_ip['keyword']=='sbend')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(ax2, aux, height=aux.angle*1000, v_offset=aux.angle/2*1000, color='b')
    plt.ylim(-15,15)

    plt.axvline(df_ip.loc[ip].s, ls='--', color='black')
    
    # large subplot
    plt.subplot2grid((3,1), (1,0), colspan=1, rowspan=2,sharex=ax1)

    plt.plot(df_ip['s'],df_ip['betx'],'b', label='$\\beta_x$')
    plt.plot(df_ip['s'],df_ip['bety'],'r', label='$\\beta_y$')
    plt.legend(loc='best')
    plt.ylabel('$\\beta$-functions [m]')
    plt.xlabel('s [m]')

    ax3 = plt.gca().twinx()   # instantiate a second axes that shares the same x-axis
    
    pdx,pdy = plt.plot(df_ip['s'], df_ip['dx'], '-', df_ip['s'],df_ip['dy'], '--', color='brown')
    ax3.tick_params(axis='y', labelcolor='brown')
    ax3.set_ylabel('$D_{x,y}$ [m]', color='brown')  # we already handled the x-label with ax1
    plt.legend([pdx, pdy], ['$D_x$','$D_y$'], loc='upper left')
    plt.ylim(-1,3)
    plt.axvline(df_ip.loc[ip].s, ls='--', color='black')

    plt.grid()
    #fig.savefig('/cas/images/LHCB1OpticsRing.pdf')
    return fig


def plot_optip(dftwiss, bim, ip, title='', ymax=[], yticks=''):
    ''' Plot optics around an LHC IP '''

    beamid = bim[-2:].lower()
    ipnum = ip[-1:]
    df_ip = dftwiss[dftwiss['beam']==bim].loc[f's.ds.l{ipnum}.{beamid}':f'e.ds.r{ipnum}.{beamid}']

    betx = df_ip.loc[ip].betx
    bety = df_ip.loc[ip].bety
    # print(f'IP {ip} Beam {bim} beta values = {betx} {bety}')

    fig, axes = plt.subplots(nrows=2, ncols=1, sharex='col', 
                             gridspec_kw={'height_ratios': [1,4]},
                             figsize=(13,8))
    fig.set_tight_layout({'pad':0.1, 'h_pad':0.1})

    # -- head plot with lattice info
    ax1 = axes[0]
    ax1.plot(df_ip['s'],0*df_ip['s'],'k')
    ax1.text(0.8, 1.05, f'$\\beta_x$={betx:.2f}, $\\beta_y$={bety:.2f}',
             fontsize=12, transform=ax1.transAxes)

    DF=df_ip[(df_ip['keyword']=='quadrupole')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(ax1, aux, height=aux.k1l, v_offset=aux.k1l/2, color='r')

    color = 'red'
    ax1.set_ylabel('1/f=K1L [m$^{-1}$]', color=color)  # we already handled the x-label with ax1
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid()
    ax1.set_ylim(-.05,.05)
    # plt.title('CERN Large Hadron Collider, Beam 1, Injection Optics 2016, Q1='+format(madx.table.summ.Q1[0],'2.3f')+', Q2='+ format(madx.table.summ.Q2[0],'2.3f'))
    ax1.set_title(title)
    ax1.axvline(df_ip.loc[ip].s, ls='--', color='black')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'blue'
    ax2.set_ylabel('$\\theta$=K0L [mrad]', color=color)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor=color)

    DF=df_ip[(df_ip['keyword']=='rbend')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(ax2, aux, height=aux.angle*1000, v_offset=aux.angle/2*1000, color='b')

    DF=df_ip[(df_ip['keyword']=='sbend')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(ax2, aux, height=aux.angle*1000, v_offset=aux.angle/2*1000, color='b')
    ax2.set_ylim(-15,15)
    
    # bottom plot with optics data
    ax0 = axes[1]

    ax0.plot(df_ip['s'],df_ip['betx'],'b', label='$\\beta_x$')
    ax0.plot(df_ip['s'],df_ip['bety'],'r', label='$\\beta_y$')
    ax0.legend(loc='best')
    ax0.set_ylabel('$\\beta$-functions [m]')
    ax0.set_xlabel('s [m]')
    ax0.axvline(df_ip.loc[ip].s, ls='--', color='black')
            
    ax3 = ax0.twinx()   # instantiate a second axes that shares the same x-axis
    
    pdx,pdy = ax3.plot(df_ip['s'], df_ip['dx'], '-', df_ip['s'],df_ip['dy'], '--', color='orange')
    ax3.tick_params(axis='y', labelcolor='orange')
    ax3.set_ylabel('$D_{x,y}$ [m]', color='orange')  # we already handled the x-label with ax1
    ax3.legend([pdx, pdy], ['$D_x$','$D_y$'], loc='upper left')
    ax3.set_ylim(-1,3)

    ax0.grid()
    if ymax :
        ax0.set_ylim(ymax[0])
        ax3.set_ylim(ymax[1])

    if yticks:
        start, end = ax0.get_ylim()
        ax0.yaxis.set_ticks(np.arange(start, end, yticks))



    #fig.savefig('/cas/images/LHCB1OpticsRing.pdf')
    return fig

def plot_optics(twissdf, title='LHC Optics', fout='', fext='.pdf'):
    # fig = plot_optics(twissdf_ip, 'lhcb1', ip='ip1', title='VDM Optics 2016 - beam 1')
    for a, b in itertools.product(['lhcb1','lhcb2'], ['ip1', 'ip2','ip5','ip8']):
        fig = plot_optip(twissdf, bim=a, ip=b, title=f'{title} - {b.upper()} {a[-2:].upper()}')
        if fout : 
            fpdf = f'{fout}_{b.upper()}_{a[-2:].upper()}{fext}'
            fig.savefig(fpdf, dpi=200, bbox_inches='tight')
            print(f'>>>> figure saved to : {fpdf}')
 
def plot_optbeam(dftwiss, bim, title='', ymax=[], yticks='', ymaxdisp=[-1,3]):
    ''' Plot beam optics for the whole LHC ring'''

    beamid = bim[-2:].lower()
    df_beam = dftwiss[dftwiss['beam']==bim]

    # betx = df_ip.loc[ip].betx
    # bety = df_ip.loc[ip].bety
    # print(f'IP {ip} Beam {bim} beta values = {betx} {bety}')

    fig, axes = plt.subplots(nrows=2, ncols=1, sharex='col', 
                             gridspec_kw={'height_ratios': [1,4]},
                             figsize=(25,10))
    fig.set_tight_layout({'pad':0.1, 'h_pad':0.1})

    # -- head plot with lattice info
    ax1 = axes[0]
    ax1.plot(df_beam['s'],0*df_beam['s'],'k')
    fstring = ''
    for i in [1, 2, 5, 8]:
        betx = df_beam.loc[f'ip{i}'].betx
        bety = df_beam.loc[f'ip{i}'].bety
        fstring = fstring + f' IP{i}:$\\beta_x$={betx:.2f}, $\\beta_y$={bety:.2f}'
        
    ax1.text(0.6, 1.02, fstring, fontsize=12, transform=ax1.transAxes)

    DF=df_beam[(df_beam['keyword']=='quadrupole')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(ax1, aux, height=aux.k1l, v_offset=aux.k1l/2, color='r')

    color = 'red'
    ax1.set_ylabel('1/f=K1L [m$^{-1}$]', color=color)  # we already handled the x-label with ax1
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid()
    ax1.set_ylim(-.05,.05)
    # plt.title('CERN Large Hadron Collider, Beam 1, Injection Optics 2016, Q1='+format(madx.table.summ.Q1[0],'2.3f')+', Q2='+ format(madx.table.summ.Q2[0],'2.3f'))
    ax1.set_title(title, loc='left')
    # ax1.axvline(df_beam.loc[ip].s, ls='--', color='black')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'blue'
    ax2.set_ylabel('$\\theta$=K0L [mrad]', color=color)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor=color)

    DF=df_beam[(df_beam['keyword']=='rbend')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(ax2, aux, height=aux.angle*1000, v_offset=aux.angle/2*1000, color='b')

    DF=df_beam[(df_beam['keyword']=='sbend')]
    for i in range(len(DF)):
        aux=DF.iloc[i]
        plotLatticeSeries(ax2, aux, height=aux.angle*1000, v_offset=aux.angle/2*1000, color='b')
    ax2.set_ylim(-15,15)
    
    # -- bottom plot with optics data
    ax0 = axes[1]

    ax0.plot(df_beam['s'],df_beam['betx'],'b', label='$\\beta_x$')
    ax0.plot(df_beam['s'],df_beam['bety'],'r', label='$\\beta_y$')
    ax0.legend(loc='best')
    ax0.set_ylabel('$\\beta$-functions [m]')
    ax0.set_xlabel('s [m]')
    # ax0.axvline(df_beam.loc[ip].s, ls='--', color='black')
            
    ax3 = ax0.twinx()   # instantiate a second axes that shares the same x-axis
    
    pdx,pdy = ax3.plot(df_beam['s'], df_beam['dx'], '-', df_beam['s'],df_beam['dy'], '--', color='orange')
    ax3.tick_params(axis='y', labelcolor='orange')
    ax3.set_ylabel('$D_{x,y}$ [m]', color='orange')  # we already handled the x-label with ax1
    ax3.legend([pdx, pdy], ['$D_x$','$D_y$'], loc='upper left')
    ax3.set_ylim(ymaxdisp)

    ax0.grid()
    if ymax :
        ax0.set_ylim(ymax[0])
        ax3.set_ylim(ymax[1])

    if yticks:
        start, end = ax0.get_ylim()
        ax0.yaxis.set_ticks(np.arange(start, end, yticks))

    #fig.savefig('/cas/images/LHCB1OpticsRing.pdf')
    return fig

def plot_phaseadvance(df, bim, ips='', title='LHC Optics - Phase Advance', fout=''):
    dfsel = (df['name'].str.contains(r'^ip[1258]:1', regex=True)) & (df['beam']==bim)
    mudf = df[dfsel].sort_index()

    for ip in [1, 2, 5 ,8]:
        mudf[f'mux_ip{ip}'] = mudf['mux']-mudf['mux'].loc[f'ip{ip}']

    fig,ax = plt.subplots(figsize=(15,8))
    
    if isinstance(ips, int):
        ips = [ips]

    for ip in ips:
        mudf.plot(x=f'mux_ip{ip}', use_index=True, marker='o', ms=10, ax=ax)
    ax.grid()
    ax.set_title(f'{title} - B{bim[-1]}')
    ax.legend()
    return fig
