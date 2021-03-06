#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 08:59:09 2018

@author: ilikecarbs

%%%%%%%%%%%%%%%%%%%%%%%%%%
   PhD_chapter_Concepts
%%%%%%%%%%%%%%%%%%%%%%%%%%

**Conceptual figures for thesis**

.. note::
        To-Do:
            -
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm
from scipy.optimize import curve_fit
import matplotlib.image as mpimg
from scipy.signal import savgol_filter

import ARPES_header as ARPES
import ARPES_utils as utils


# Set standard fonts
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.serif'] = ['Computer Modern Roman']
plt.rc('font', **{'family': 'serif', 'serif': ['STIXGeneral']})

# Dictionaries
font = {'family': 'serif',
        'style': 'normal',
        'color': 'black',
        'weight': 'ultralight',
        'size': 12,
        }

kwargs_ex = {'cmap': cm.ocean_r}  # Experimental plots
kwargs_th = {'cmap': cm.bone_r}  # Theory plots
kwargs_ticks = {'bottom': True,
                'top': True,
                'left': True,
                'right': True,
                'direction': 'in',
                'length': 1.5,
                'width': .5,
                'colors': 'black'}
kwargs_cut = {'linestyle': '-.',
              'color': 'turquoise',
              'lw': .5}
kwargs_ef = {'linestyle': ':',
             'color': 'k',
             'lw': 1}

# Directory paths
save_dir = '/Users/denyssutter/Documents/2_physics/PhD/PhD_Denys/Figs/'
data_dir = '/Users/denyssutter/Documents/2_physics/PhD/data/'
home_dir = '/Users/denyssutter/Documents/3_library/Python/ARPES'


def fig1(print_fig=True):
    """figure 1

    %%%%%%%%%%%%%%%%%%%%%%%%%%%
    Photoemission principle DOS
    %%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig1'

    fig = plt.figure(figname, figsize=(8, 8), clear=True)

    ax = fig.add_axes([.2, .2, .6, .6])

    xx = np.linspace(0, 1.5, 100)
    xx_fill = np.linspace(0, np.sqrt(2), 100)
    yy = xx ** 2
    yy_fill = xx_fill ** 2

    x_off = 3.5
    y_off = 4.5
    yy_2 = yy + y_off
    yy_2_fill = yy_fill + y_off
    xx_2 = xx * utils.FDsl(yy_2, *[.05, 2+y_off, 1, 0, 0]) + x_off
    xx_2_fill = xx_fill * utils.FDsl(yy_2, *[.05, 2.2+y_off, 1, 0, 0]) + x_off

    core_1 = utils.lor(yy_2, *[.7+y_off, .03, .12, 0, 0, 0]) + x_off
    core_2 = utils.lor(yy_2, *[1.2+y_off, .03, .1, 0, 0, 0]) + x_off

    # plot DOS solid
    ax.plot(xx, yy + 2, 'k')
    ax.plot(xx_fill, 4*np.ones(len(xx_fill)), 'k-', lw=.5)
    ax.plot([0, 1.2], [.7, .7], 'k-', alpha=.5, lw=2)
    ax.plot([0, 1], [1.2, 1.2], 'k-', alpha=.5, lw=2)
    ax.fill_between(xx_fill, yy_fill + 2, 4, alpha=.1, color='k')

    # plot spectrum
    ax.plot(xx_2, yy_2 + 2, 'k')
    ax.plot(xx_2_fill, (4+y_off)*np.ones(len(xx_2_fill)), 'k-', lw=.5)
    ax.plot(core_1, yy_2, 'k')
    ax.plot(core_2, yy_2, 'k')
    ax.fill_between(xx_2_fill, yy_2_fill + 2, 4 + y_off, alpha=.5, color='C8')
    ax.fill_between(core_1, yy_2, 4 + y_off, alpha=.5, color='C8')
    ax.fill_between(core_2, yy_2, 4 + y_off, alpha=.5, color='C8')

    # plot arrow and excitation
    x_arr_1 = np.linspace(.88, 1.5, 50)
    y_arr_1 = np.sin(x_arr_1*50)/10 + x_arr_1*.7 + .9
    ax.plot(x_arr_1, y_arr_1, 'c-')
    ax.arrow(x_arr_1[0], y_arr_1[0], -.1, -.09,
             head_width=0.1, head_length=0.1,
             ec='c', fc='c', lw=2)
    ax.text(1.55, 2, r'$h\nu$')
    ax.plot([0, x_off], [y_off, y_off], **kwargs_ef)
    ax.plot(.5, 1.2, 'o', mec='k', mfc='w')
    ax.plot(.5, 1.2+y_off, 'ko')
    ax.plot([.5, x_off], [1.2+y_off, 1.2+y_off], **kwargs_ef)
    ax.arrow(.5, 1.2, 0, y_off-.2, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    x_arr_2 = np.linspace(.88, 1.5, 50) + .5
    y_arr_2 = np.sin(x_arr_2*50)/10 + x_arr_2*.7 + 3.3
    ax.plot(x_arr_2, y_arr_2, 'c-')
    ax.arrow(x_arr_2[0], y_arr_2[0], -.1, -.09,
             head_width=0.1, head_length=0.1,
             ec='c', fc='c', lw=2)
    ax.plot(1, 3.8, 'o', mec='k', mfc='w')
    ax.plot(1, 3.8+y_off, 'ko')
    ax.plot([1, x_off], [3.8+y_off, 3.8+y_off], **kwargs_ef)
    ax.arrow(1, 3.8, 0, y_off-.2, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.text(2.05, 4.75, r'$h\nu$')

    # plot helper lines
    ax.plot([4.5, 9.], [1.2+y_off, 1.2+y_off], **kwargs_ef)
    ax.plot([7.7, 8.4], [y_off, y_off], **kwargs_ef)
    ax.plot([1, 9.], [1.2, 1.2], **kwargs_ef)
    ax.plot([np.sqrt(2), 8.4], [4, 4], **kwargs_ef)
    ax.arrow(8, 5, 0, .58, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.arrow(8, 5, 0, -.4, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.text(8.1, 5, r'$E_\mathrm{kin}$')
    ax.arrow(8, 4.25, 0, .15, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.arrow(8, 4.25, 0, -.15, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.text(8.1, 4.13, r'$\Phi$')
    ax.arrow(8, 3, 0, .88, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.arrow(8, 3, 0, -1.7, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.text(8.1, 2.5, r'$E_\mathrm{B}$')
    ax.arrow(8.8, 3, 0, 2.58, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.arrow(8.8, 3, 0, -1.7, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.text(8.9, 3.5, r'$h\nu$')

    # plot axis
    ax.arrow(0, 0, 0, 5, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=1.5)
    ax.arrow(0, 0, 2.5, 0, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=1.5)
    ax.arrow(0+x_off, 0+y_off, 0, 5, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=1.5)
    ax.arrow(0+x_off, 0+y_off, 2.5, 0, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=1.5)
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    plt.axis('off')

    # add text
    ax.text(4.5, 5.8, 'core levels')
    ax.text(4.7, 7.5, 'valence band')
    ax.text(-.7, 3.9, r'$E_\mathrm{F}$')
    ax.text(-.7, 4.4, r'$E_\mathrm{vac}$')
    ax.text(.4, 5.9, r'$e^-$')
    ax.text(.9, 8.5, r'$e^-$')
    ax.text(-.8, 6.5, r'SAMPLE', fontdict=font)
    ax.text(4, 9, r'SPECTRUM', fontdict=font)
    ax.text(2.7, -.1, r'DOS$(\omega)$', fontdict=font)
    ax.text(2.7+x_off, -.1+y_off, r'DOS$(\omega)$', fontdict=font)
    ax.text(-.12, 5.2, r'$\omega$', fontdict=font)
    ax.text(-.12+x_off, 5.2+y_off, r'$\omega$', fontdict=font)
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig2(print_fig=True):
    """figure 2

    %%%%%%%%%%%%%%%%%%%%%
    Electron transmission
    %%%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig2'

    fig = plt.figure(figname, figsize=(8, 8), clear=True)

    ax = fig.add_axes([.2, .2, .6, .6])

    # Create a sphere
    k_i = 2.5
    k_f = 2

    k_th = np.pi/3
    off = 4
    th = np.linspace(0, np.pi, 100)
    x_i = k_i * np.cos(th)
    y_i = k_i * np.sin(th)
    x_f = k_f * np.cos(th)
    y_f = k_f * np.sin(th)
    kx_i = k_i * np.cos(k_th)
    ky_i = k_i * np.sin(k_th)
    ky_f = np.sqrt(k_f ** 2 - kx_i ** 2)

    kxs_i = np.linspace(-k_f, k_f, 100)
    kys_i = np.sqrt(k_i ** 2 - kxs_i ** 2)

    kx_p = np.linspace(0, k_f, 50)
    kx_n = np.linspace(0, -k_f, 50)
    ky_p = kx_p * (kys_i[-1] / k_f)
    ky_n = kx_n * -(kys_i[0] / k_f)

    ax.arrow(0, 0, kx_i-.1, ky_i-.15, head_width=0.1, head_length=0.1,
             fc='r', ec='r', lw=1.5)
    ax.arrow(0, 0, 0, ky_i-.1, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.arrow(0, 0, kx_i-.06, 0, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)

    ax.arrow(0, off, kx_i-.1, ky_f-.15, head_width=0.1, head_length=0.1,
             fc='r', ec='r', lw=1.5)
    ax.arrow(0, off, 0, ky_f-.1, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.arrow(0, off, kx_i-.06, 0, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)

    ax.plot(kxs_i, kys_i, 'C8-', lw=3)
    ax.plot([kxs_i[-1], kxs_i[-1]], [kys_i[-1], off], 'k--', lw=.5)
    ax.plot([kxs_i[0], kxs_i[0]], [kys_i[0], off], 'k--', lw=.5)
    ax.plot(kx_p, ky_p, 'k--', lw=.5)
    ax.plot(kx_n, ky_n, 'k--', lw=.5)
    ax.fill_between(kx_p, ky_p, kys_i[50:], facecolor='C8', alpha=.1,
                    edgecolor='w')
    ax.fill_between(kx_n, ky_n, kys_i[50:], facecolor='C8', alpha=.1,
                    edgecolor='w')
    ax.plot([kx_i, kx_i], [0, off+ky_f], **kwargs_ef)
    ax.plot(x_i, y_i, 'k-')
    ax.plot(x_f, y_f+off, 'C8-')
    ax.fill_between([-3, 3], [3.6, 3.6], [4, 4], color='C8', alpha=.2)
    ax.fill_between([-3, 3], [-.4, -.4], [0, 0], color='k', alpha=.2)
    ax.set_xlim(-3.25, 3.25)
    ax.set_ylim(-.4, 6.1)

    ax.arrow(-k_f, 1, 0, .35, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)
    ax.arrow(-k_f, 1, 0, -.9, head_width=0.1, head_length=0.1,
             fc='k', ec='k', lw=.5)

    ax.plot(kx_i, ky_i, 'o', mec='k', mfc='w')
    ax.plot(kx_i, ky_f+off, 'o', mec='k', mfc='k')
    plt.axis('off')

    # add text
    ax.text(-2, .35, r'$\sqrt{\frac{2m V_0}{\hbar^2}}$', fontdict=font)
    ax.text(1.3, 5.7, r'$e^-$', fontdict=font)
    ax.text(.03, .7, r'$\theta_\mathrm{int}$')
    ax.text(.1, 4.4, r'$\theta$')
    ax.text(.65, 1.8, r'$\mathbf{K}_f$', color='r')
    ax.text(.7, 5.3, r'$\mathbf{k}_f$', color='r')
    ax.text(-.4, 1.8, r'$\mathbf{K}_f^\perp$')
    ax.text(-.4, 5.2, r'$\mathbf{k}_f^\perp$')
    ax.text(.8, -.3, r'$\mathbf{K}_f^\parallel$')
    ax.text(.8, 3.7, r'$\mathbf{k}_f^\parallel$')
    ax.text(-1.8, 3.73, 'Surface')
    ax.text(-1.8, 4.27, 'Vacuum')
    ax.text(-1.8, -.27, 'Bulk')
    ax.text(-.1, -.27, r'$\Gamma$')
    x1, y1 = 0, 1  # for angle text
    x2, y2 = 0.45, 0.8  # for angle text

    # angle text
    ax.annotate("",
                xy=(x1, y1), xycoords='data',
                xytext=(x2, y2), textcoords='data',
                arrowprops=dict(arrowstyle="-",
                                color="k",
                                shrinkA=0, shrinkB=0,
                                patchA=None,
                                patchB=None,
                                connectionstyle="arc3,rad=.25"
                                ))
    x1, y1 = 0, .7+off
    x2, y2 = 0.4, 0.5+off
    ax.annotate("",
                xy=(x1, y1), xycoords='data',
                xytext=(x2, y2), textcoords='data',
                arrowprops=dict(arrowstyle="-",
                                color="k",
                                shrinkA=0, shrinkB=0,
                                patchA=None,
                                patchB=None,
                                connectionstyle="arc3,rad=.25"
                                ))
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig3(print_fig=True):
    """figure 3

    %%%%%%%
    EDC/MDC
    %%%%%%%
    """

    figname = 'CONfig3'

    fig = plt.figure(figname, figsize=(8, 8), clear=True)

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_position([.1, .5, .3, .4])
    ax1.tick_params(**kwargs_ticks)
    T = 48

    a = 3.885
    t1 = -0.23
    t2 = 0.087
    mu = -0.272
    W = 0.2
    gamma = 0.02
    A = 4
    kB = 8.617e-5

    w = np.linspace(0.05, -0.5, int(1e3))
    k = np.linspace(-1, 1, int(1e3))

    def sig(gamma, A, W, w):
        return (- complex(0, 1) * (gamma + A * w ** 2) / (1 + (w / W) ** 4)
                + 1 / np.sqrt(2) * w / W * (gamma * (1 + (w / W) ** 2)
                - A * W ** 2 * (1 - (w / W) ** 2)) / (1 + (w / W) ** 4))

    def Ximod(t1, t2, a, mu, k):
        return (2 * t1 * (np.cos(1 / np.sqrt(2) * k * a) +
                          np.cos(1 / np.sqrt(2) * k * a)) +
                4 * t2 * np.cos(1 / np.sqrt(2) * k * a) *
                np.cos(1 / np.sqrt(2) * k * a) - mu)

    def G(k, w, t1, t2, a, mu, gamma, A, W):
        return 1 / (w - Ximod(t1, t2, a, mu, k) - sig(gamma, A, W, w))

    ek = 1.2 * Ximod(t1, t2, a, mu, k)
    [K, E] = np.meshgrid(k, w)

    model = (-1 / np.pi * np.imag(G(K, E, t1, t2, a, mu, gamma, A, W)) *
             utils.FDsl(E, *[T*kB, 0, 1, 0, 0]))

    max_pts = np.ones((w.size))

    # extract eigenenergies in the DFT plot
    for i in range(w.size):
        max_pts[i] = model[i, :].argmax()
    ini = 93  # range where to search for
    fin = 580  # 580
    max_pts = max_pts[ini:fin]
    max_k = np.abs(k[max_pts.astype(int)])
    max_en = w[ini:fin]

    w_ek = np.zeros(fin-ini)
    for i in range(fin-ini):
        dummy, k_idx = utils.find(k, max_k[i])
        w_ek[i] = ek[k_idx]

    # build MDC / EDC
    mdc_val, mdc_idx = utils.find(w, -.1)
    mdc = model[mdc_idx]
    edc_val, edc_idx = utils.find(k, .4)
    edc = model[:, edc_idx]

    # initial guess
    p_mdc_i = np.array([-.3, .3,
                        .05, .05,
                        .3, .3,
                        .1, 0, 0])

    # fit boundaries
    bounds_bot = np.concatenate((p_mdc_i[0:-3] - np.inf,
                                 p_mdc_i[-3:] - np.inf))
    bounds_top = np.concatenate((p_mdc_i[0:-3] + np.inf,
                                 p_mdc_i[-3:] + np.inf))
    p_mdc_bounds = (bounds_bot, bounds_top)

    # fit MDC
    p_mdc, cov_mdc = curve_fit(
            utils.lor_2, k, mdc, p_mdc_i, bounds=p_mdc_bounds)

    # fit and background
    f_mdc = utils.lor_2(k, *p_mdc)

    # coherent / incoheren weight EDC
    p_edc_coh = np.array([-.05, 2e-2, 6.6e-1, 0, 0, 0])
    p_edc_inc = np.array([-.15, 1.1e-1, 5.5e-1, 0, 0, 0])
    f_coh = utils.lor(w, *p_edc_coh) * utils.FDsl(w, *[T*kB*2, 0, 1, 0, 0])
    f_coh[0] = 0
    f_coh[-1] = 0
    f_inc = utils.lor(w, *p_edc_inc) * utils.FDsl(w, *[T*kB*2, 0, 1, 0, 0])
    f_inc[0] = 0
    f_inc[-1] = 0

    c0 = ax1.pcolormesh(k, w, model, cmap=cm.bone_r, zorder=.1)
    ax1.set_rasterization_zorder(.2)
    ax1.plot(k, ek, 'C4--')
    ax1.plot(max_k, max_en, 'k-', lw=1)
    ax1.plot([k[0], k[-1]], [0, 0], **kwargs_ef)
    ax1.plot([k[0], k[-1]], [mdc_val, mdc_val], ls='-.', color='r', lw=.5)
    ax1.plot([edc_val, edc_val], [w[0], w[-1]], ls='-.', color='r', lw=.5)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_position([.1, .29, .3, .2])
    ax2.tick_params(**kwargs_ticks)
    ax2.plot(k, mdc, 'ko-', lw=1, ms=1)
    ax2.plot(k, f_mdc, 'C8--')
    # ax2.plot([p_mdc[1]-p_mdc[2], p_mdc[1] + p_mdc[2]],
    #          [np.max(mdc)/2, np.max(mdc)/2])

    ax2.arrow(-.02, np.max(mdc)/2, .2, 0, head_width=0.3,
              head_length=0.1, fc='C0', ec='C0')
    ax2.arrow(.4+.33, np.max(mdc)/2, -.2, 0, head_width=0.3,
              head_length=0.1, fc='C0', ec='C0')
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_position([.41, .5, .2, .4])
    ax3.tick_params(**kwargs_ticks)
    ax3.plot([0, 100], [0, 0], **kwargs_ef)
    ax3.plot(edc, w, 'ko-', lw=1, ms=1)
    ax3.fill(f_coh, w, alpha=.5, color='b', zorder=.1)
    ax3.fill(f_inc, w, alpha=.5, color='C0', zorder=.1)
    ax3.set_rasterization_zorder(.2)

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_position([.7, .5, .25, .25])
    ax4.tick_params(**kwargs_ticks)
    ReS = savgol_filter(max_en - w_ek, 51, 3)
    ax4.plot(-w[ini:fin]*1e3, -np.imag(sig(gamma, A, W, w))[ini:fin]*1e3/1.2,
             'C0', lw=2)
    ax4.plot(np.abs(max_en)*1e3, ReS*1e3, 'g', lw=2)
#    ax4.plot(np.abs(max_en)*1e3, utils.poly_2(np.abs(max_en),
#                                              .02, 0, 1.5)*1e3, 'C0-', lw=2)
    ax4.set_rasterization_zorder(.2)

    # decorate axes
    ax1.set_xticklabels([])
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-.5, .05)
    ax1.set_ylabel(r'$\omega$ (eV)', fontdict=font)
    ax2.set_yticks([])
    ax2.set_xlim(-1, 1)
    ax2.set_ylim(0, 1.1 * np.max(mdc))
    ax2.set_xlabel(r'$k$ $(\pi/a)$', fontdict=font)
    ax2.set_ylabel('MDC intensity', fontdict=font)
    ax3.set_yticklabels([])
    ax3.set_xticks([])
    ax3.set_xlim(0, 1.1 * np.max(edc))
    ax3.set_ylim(-.5, .05)
    ax3.set_xlabel('EDC intensity', fontdict=font)
    ax4.set_ylabel('Arb. units', fontdict=font)
    ax4.set_yticks([])
    ax4.set_xlabel(r'$\omega$ (meV)', fontdict=font)
    ax4.set_xticks(np.arange(0, 300, 100))
    ax4.set_xticklabels(['0', '-100', '-200'])
    ax4.set_ylim(0, 85)
    ax4.set_xlim(0, 268)

    # add text
    ax1.text(-.95, .02, r'(a)', fontdict=font)
    ax1.text(-.85, -.09, 'MDC', color='r', fontsize=12)
    ax1.text(.27, -.4, 'EDC', rotation=90, color='r', fontsize=12)
    ax1.text(.05, -.3, r'$\epsilon_\mathbf{k}^b$', color='C4', fontsize=12)
    ax1.text(.05, -.2, r'$\epsilon_\mathbf{k}^\mathrm{exp}$', color='k',
             fontsize=12)
    ax2.text(-.95, 5.5, r'(b)', fontdict=font)
    ax2.text(.5, 3.2, r'$2\,\Gamma$', color='C0', fontsize=12)
    ax3.text(.5, .02, r'(c)', fontdict=font)
    ax3.text(4, -.11, r'$\mathcal{A}_\mathrm{coh}\,(k, \omega)$',
             fontsize=12, color='b')
    ax3.text(2, -.2, r'$\mathcal{A}_\mathrm{inc}\,(k, \omega)$',
             fontsize=12, color='C0')
    ax4.text(200, 56, r'$2\,\Gamma (\omega)$', color='C0', fontsize=12)
    ax4.text(200, 30, r'$\Re \Sigma (\omega)$', color='g', fontsize=12)
    ax4.text(5, 78, '(d)', fontdict=font)

    # colorbar
    pos = ax3.get_position()
    cax = plt.axes([pos.x0+pos.width + 0.01,
                    pos.y0, 0.01, pos.height])
    cbar = plt.colorbar(c0, cax=cax, ticks=None)
    cbar.set_ticks([])

    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig4(print_fig=True):
    """figure 4

    %%%%%%%%%%%%%%%%%%
    Experimental Setup
    %%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig4'

    fig = plt.figure(figname, figsize=(8, 8), clear=True)

    ax = fig.add_axes([.1, .1, .8, .8], projection='3d')

    ax.tick_params(**kwargs_ticks)

    # Create a sphere
    k_i = 3

    k_phi = np.pi/3
    k_th = np.pi/3

#    phi, theta = np.mgrid[0.0:0.5*np.pi:180j, 0.0:2.0*np.pi:720j]
#    x_i = k_i * np.sin(phi) * np.cos(theta)
#    y_i = k_i * np.sin(phi) * np.sin(theta)
#    z_i = k_i * np.cos(phi)

    x_phi = 1.1 * np.cos(np.linspace(0, k_phi, 100))
    y_phi = 1.1 * np.sin(np.linspace(0, k_phi, 100))
    z_phi = np.zeros(100)

    x_th = 1 * np.sin(np.linspace(0, k_th, 100)) * np.cos(k_phi)
    y_th = 1 * np.sin(np.linspace(0, k_th, 100)) * np.sin(k_phi)
    z_th = 1 * np.cos(np.linspace(0, k_th, 100))

    y_hv = np.linspace(-2, -.25, 100)
    x_hv = .2*np.sin(y_hv*50)
    z_hv = -y_hv

    kx_i = k_i * np.sin(k_th) * np.cos(k_phi)
    ky_i = k_i * np.sin(k_th) * np.sin(k_phi)
    kz_i = k_i * np.cos(k_th)

    ax.quiver(0, 0, 0, 0, 0, 2.5, arrow_length_ratio=.08,
              color='k', zorder=.1)
    ax.quiver(0, 0, 0, 0, 2.5, 0, arrow_length_ratio=.06,
              color='k', zorder=.1)
    ax.quiver(0, 0, 0, 2.5, 0, 0, arrow_length_ratio=.08,
              color='k', zorder=.1)
    ax.quiver(0, 0, 0, kx_i-.1, ky_i-.1, kz_i-.1, arrow_length_ratio=.08, lw=2,
              color='r', zorder=.1)
    ax.quiver(x_hv[-1], y_hv[-1], z_hv[-1], .1, .3, -.2,
              arrow_length_ratio=.6, color='c', zorder=.1)

    ax.plot([0, 0], [0, 0], [0, 0], 'o', mec='k', mfc='w', ms=5)
    ax.plot([kx_i, kx_i], [ky_i, ky_i], [kz_i, kz_i],
            'o', mec='k', mfc='k', ms=5)
    ax.plot([kx_i, kx_i], [ky_i, ky_i], [0, kz_i], **kwargs_ef)
    ax.plot([0, kx_i], [0, ky_i], [kz_i, kz_i], **kwargs_ef)
    ax.plot([0, kx_i], [0, ky_i], [0, 0], **kwargs_ef)
    ax.plot([kx_i, kx_i], [0, ky_i], [0, 0], **kwargs_ef)
    ax.plot([0, kx_i], [ky_i, ky_i], [0, 0], **kwargs_ef)
    ax.plot([0, kx_i], [ky_i, ky_i], [0, 0], **kwargs_ef)
    ax.plot(x_phi, y_phi, z_phi, 'C0')
    ax.plot(x_th, y_th, z_th, 'C0')
    ax.plot(x_hv, y_hv, z_hv, 'c')
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-2, 4])
    ax.set_aspect("equal")
    # ax.plot_surface(x_i, y_i, z_i, color="r", alpha=.05)

    # add text
    ax.text(0, -2.2, 2, r'$hv$', fontdict=font)
    ax.text(0, 1.65, 1., r'$e^-$', fontdict=font)
    ax.text(0, .1, .35, r'$\theta$', fontdict=font)
    ax.text(.75, .3, 0, r'$\phi$', fontdict=font)
    ax.text(2.9, 0, 0, r'$x$', fontdict=font)
    ax.text(0, 2.6, 0, r'$y$', fontdict=font)
    ax.text(0, -.1, 2.6, r'$z$', fontdict=font)
    ax.text(3.5, 1.5, -0.25, 'SAMPLE', fontdict=font)

    kwargs_cyl = {'alpha': .05, 'color': 'k'}  # keywords cylinder

    # Cylinder
    r = 3
    x_cyl = np.linspace(-r, r, 100)
    z_cyl = np.linspace(-1, 0, 100)
    X_cyl, Z_cyl = np.meshgrid(x_cyl, z_cyl)
    Y_cyl = np.sqrt(r**2 - X_cyl**2)

    x_cir = r * np.cos(np.linspace(0, 2*np.pi, 360))
    y_cir = r * np.sin(np.linspace(0, 2*np.pi, 360))

    R, Phi = np.meshgrid(np.linspace(0, r, 100), np.linspace(0, 2*np.pi, 100))

    X_cir = R * np.cos(Phi)
    Y_cir = R * np.sin(Phi)
    Z_ceil = np.zeros((100, 100))
    Z_floor = -np.ones((100, 100))

    # draw cylinder
    ax.plot_surface(X_cyl, Y_cyl, Z_cyl, **kwargs_cyl, zorder=.1)
    ax.plot_surface(X_cyl, -Y_cyl, Z_cyl, **kwargs_cyl, zorder=.1)
    ax.plot_surface(X_cir, Y_cir, Z_floor, **kwargs_cyl, zorder=.1)
    ax.plot_surface(X_cir, Y_cir, Z_ceil, **kwargs_cyl, zorder=.1)
    ax.set_rasterization_zorder(.2)
    ax.plot(x_cir, y_cir, 'k-', alpha=.1)
    ax.plot(x_cir, y_cir, -1, 'k--', alpha=.1, lw=.5)
    plt.axis('off')
    ax.view_init(elev=20, azim=30)

    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=200,
                    bbox_inches="tight")


def fig5(print_fig=True):
    """figure 5

    %%%%%%%%%%%%%%%%
    eg, t2g orbitals
    %%%%%%%%%%%%%%%%
    """

    figname = 'CONfig5'

    # create figure
    fig = plt.figure(figname, figsize=(8, 8), clear=True)
    ax = fig.add_axes([.1, .1, .8, .8], projection='3d')

    theta_1d = np.linspace(0, np.pi, 300)
    phi_1d = np.linspace(0, 2*np.pi, 300)

    theta_2d, phi_2d = np.meshgrid(theta_1d, phi_1d)
    xyz_2d = np.array([np.sin(theta_2d) * np.sin(phi_2d),
                      np.sin(theta_2d) * np.cos(phi_2d),
                      np.cos(theta_2d)])

    colormap = cm.ScalarMappable(cmap=plt.get_cmap("PRGn"))
    colormap.set_clim(-.45, .45)

    l_ = 2  # angular momentum

    # build orbitals
    dz2 = sph_harm(0, l_, phi_2d, theta_2d)

    dxz = ((sph_harm(-1, l_, phi_2d, theta_2d)
           - sph_harm(1, l_, phi_2d, theta_2d))
           / np.sqrt(2))

    dyz = (1j * (sph_harm(-1, l_, phi_2d, theta_2d)
           + sph_harm(1, l_, phi_2d, theta_2d))
           / np.sqrt(2))

    dxy = (1j * (sph_harm(-2, l_, phi_2d, theta_2d)
           - sph_harm(2, l_, phi_2d, theta_2d))
           / np.sqrt(2))

    dx2y2 = ((sph_harm(-2, l_, phi_2d, theta_2d)
             + sph_harm(2, l_, phi_2d, theta_2d))
             / np.sqrt(2))

    dz2_r = np.abs(dz2.real)*xyz_2d
    dxz_r = np.abs(dxz.real)*xyz_2d
    dyz_r = np.abs(dyz.real)*xyz_2d
    dxy_r = np.abs(dxy.real)*xyz_2d
    dx2y2_r = np.abs(dx2y2.real)*xyz_2d

    orbitals_r = (dxy_r, dxz_r, dyz_r, dz2_r, dx2y2_r)
    orbitals = (dxy, dxz, dyz, dz2, dx2y2)

    # locations
    x = [0, 0, 0, 0, 0]
    y = [1.1, 2.6, 4.1, 1.85, 3.35]
    z = [1, 1, 1, 2.65, 2.65]

    # plot orbitals
    for i in range(5):
        ax.plot_surface(orbitals_r[i][0]+x[i], orbitals_r[i][1]+y[i],
                        orbitals_r[i][2]+z[i],
                        facecolors=colormap.to_rgba(orbitals[i].real),
                        rstride=2, cstride=2, zorder=.1)

    # surfaces
    X_t2g = np.zeros((2, 2))
    z_t2g = [.2, 1.9]
    y_t2g = [.2, 4.9]
    Y_t2g, Z_t2g = np.meshgrid(y_t2g, z_t2g)

    X_eg = np.zeros((2, 2))
    z_eg = [1.9, 3.6]
    y_eg = [.2, 4.9]
    Y_eg, Z_eg = np.meshgrid(y_eg, z_eg)

    # plot surfaces
    ax.plot_surface(X_t2g, Y_t2g, Z_t2g, alpha=.2, color='b', zorder=.1)
    ax.plot_surface(X_eg, Y_eg, Z_eg, alpha=.2, color='C0', zorder=.1)
    ax.quiver(0, 0, 0, 0, 0, 1, arrow_length_ratio=.08,
              color='k')
    ax.quiver(0, 0, 0, 0, 1, 0, arrow_length_ratio=.06,
              color='k')
    ax.quiver(0, 0, 0, 1, 0, 0, arrow_length_ratio=.08,
              color='k')
    ax.set_xlim(1, 4)
    ax.set_ylim(2.5, 5.5)
    ax.set_zlim(1, 4)
    plt.axis('off')
    ax.view_init(elev=20, azim=30)

    # add text
    ax.text(1.25, 0, 0, '$x$', fontdict=font)
    ax.text(0, 1.1, -.05, '$y$', fontdict=font)
    ax.text(0, -.05, 1.1, '$z$', fontdict=font)

    ax.text(0, 1.05, 1.45, r'$d_{xy}$', fontdict=font)
    ax.text(0, 2.5, 1.5, r'$d_{yz}$', fontdict=font)
    ax.text(0, 3.85, 1.5, r'$d_{xz}$', fontdict=font)
    ax.text(0, 1.75, 3.35, r'$d_{z^2}$', fontdict=font)
    ax.text(0, 3.1, 3.05, r'$d_{x^2-y^2}$', fontdict=font)

    ax.text(0, .3, 3.3, r'$e_{g}$', fontsize=15, color='k')
    ax.text(0, .3, 1.6, r'$t_{2g}$', fontsize=15, color='k')
    ax.set_rasterization_zorder(.2)
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=300,
                    bbox_inches="tight")


def fig6(print_fig=True):
    """figure 6

    %%%%%%%%%%%%%%%%%%
    Manipulator angles
    %%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig6'

    fig = plt.figure(figname, figsize=(8, 8), clear=True)

    ax = fig.add_axes([.1, .1, .8, .8], projection='3d')

    k_i = 3
    phi, theta = np.mgrid[0.0:0.5*np.pi:180j, 0.0:2.0*np.pi:720j]
    x_i = k_i * np.sin(phi) * np.cos(theta)
    y_i = k_i * np.sin(phi) * np.sin(theta)
    z_i = k_i * np.cos(phi)

    # draw hemisphere
    ax.plot_surface(x_i, y_i, z_i, color='C8', alpha=.1)

    # detector angles
    angdg = np.linspace(-20, 20, 100)
    thdg = 10
    tidg = 20
    phidg = 0

    # angle x-axis
    phi = np.pi/8

    # angle indicators
    k = utils.det_angle(k_i, angdg, thdg, tidg, phidg)
    k_ti = utils.det_angle(2.2, np.linspace(0, thdg, 30), thdg, tidg, phidg)
    k_0 = utils.det_angle(k_i, 0, 0, tidg, phidg)
#    k_m = det_angle(.6, angdg, thdg, tidg, phidg)
    k_full = utils.det_angle(k_i, np.linspace(-90, 90, 200), 0, tidg, phidg)

    # angle indicator
    x_th_m = np.zeros(50)
    y_th_m = 1.5 * np.sin(np.linspace(0, tidg*np.pi/180, 50))
    z_th_m = 1.5 * np.cos(np.linspace(0, tidg*np.pi/180, 50))

    x_phi_m = 1.7 * np.sin(np.linspace(0, phi, 50))
    y_phi_m = 1.7 * np.cos(np.linspace(0, phi, 50))
    z_phi_m = np.zeros(50)

    # lines
    ax.quiver(0, 0, 0, 0, 0, k_i, color='k', arrow_length_ratio=.06, lw=2)
    ax.quiver(0, 0, 0, k_i*np.sin(phi), k_i*np.cos(phi), 0,
              color='k', arrow_length_ratio=.06, lw=2)
    ax.quiver(0, 0, 0, k_i*np.sin(phi-np.pi/2), k_i*np.cos(phi-np.pi/2), 0,
              color='k', arrow_length_ratio=.06, lw=2)
    ax.plot([0, 0], [0, k_i], [0, 0], 'k--', lw=1)
    ax.plot([0, k[0, 50]], [0, k[1, 50]], [0, k[2, 50]], 'k--', lw=1)
    ax.plot([0, k_0[0]], [0, k_0[1]], [0, k_0[2]], 'k--', lw=1)

    ax.plot(k_full[0], k_full[1], k_full[2], **kwargs_ef)
    ax.plot([0, k[0, -1]], [0, k[1, -1]], [0, k[2, -1]], **kwargs_ef)
    ax.plot([0, k[0, 0]], [0, k[1, 0]], [0, k[2, 0]], **kwargs_ef)
    ax.plot(k[0], k[1], k[2], 'r-', lw=3)
    ax.plot(k_ti[0], k_ti[1], k_ti[2], 'C0-')
    ax.plot(x_th_m, y_th_m, z_th_m, 'C0-')
    ax.plot(x_phi_m, y_phi_m, z_phi_m, 'C0-')

    # Cylinder
    kwargs_cyl = {'alpha': .05, 'color': 'k'}  # keywords cylinder
    r = 3
    x_cyl = np.linspace(-r, r, 100)
    z_cyl = np.linspace(-1, 0, 100)
    X_cyl, Z_cyl = np.meshgrid(x_cyl, z_cyl)
    Y_cyl = np.sqrt(r**2 - X_cyl**2)

    x_cir = r * np.cos(np.linspace(0, 2*np.pi, 360))
    y_cir = r * np.sin(np.linspace(0, 2*np.pi, 360))

    R, Phi = np.meshgrid(np.linspace(0, r, 100), np.linspace(0, 2*np.pi, 100))

    X_cir = R * np.cos(Phi)
    Y_cir = R * np.sin(Phi)
    Z_ceil = np.zeros((100, 100))
    Z_floor = -np.ones((100, 100))

    # draw cylinder
    ax.plot_surface(X_cyl, Y_cyl, Z_cyl, **kwargs_cyl)
    ax.plot_surface(X_cyl, -Y_cyl, Z_cyl, **kwargs_cyl)
    ax.plot_surface(X_cir, Y_cir, Z_floor, **kwargs_cyl)
    ax.plot_surface(X_cir, Y_cir, Z_ceil, **kwargs_cyl)
    ax.plot(x_cir, y_cir, 'k-', alpha=.1)
    ax.plot(x_cir, y_cir, -1, 'k--', alpha=.1, lw=.5)

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-1, 3])

    plt.axis('off')
    ax.view_init(elev=20, azim=50)

    # add text
    ax.text(-.2, .2, 2.8, r'Detector angles  $\alpha$', fontsize=15, color='r')
    ax.text(1.5, 3.2, 0, '$x$', fontsize=15, color='k')
    ax.text(-2.9, 1.2, 0, '$y$', fontsize=15, color='k')
    ax.text(0, -.1, 3.1, '$z$', fontsize=15, color='k')
    ax.text(-.2, -.2, 1, r'$\Theta$', fontsize=15, color='k')
    ax.text(-.2, .53, 1.8, r'$\chi$', fontsize=15, color='k')
    ax.text(.48, 1.32, 0, r'$\Phi$', fontsize=15, color='k')
    ax.text(3., 3, 0, 'SAMPLE', fontsize=15, color='k')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=200,
                    bbox_inches="tight")


def fig7(print_fig=True):
    """figure 7

    %%%%%%%%%%%%
    Mirror plane
    %%%%%%%%%%%%
    """

    figname = 'CONfig7'

    fig = plt.figure(figname, figsize=(8, 8), clear=True)
    ax = fig.add_axes([.1, .1, .8, .8], projection='3d')
    ax.tick_params(**kwargs_ticks)

    # Create a sphere
    k_i = 3

    k_phi = np.pi/2
    k_th = np.pi/4

    theta_1d = np.linspace(0, np.pi, 300)
    phi_1d = np.linspace(0, 2*np.pi, 300)

    theta_2d, phi_2d = np.meshgrid(theta_1d, phi_1d)
    xyz_2d = np.array([np.sin(theta_2d) * np.sin(phi_2d),
                      np.sin(theta_2d) * np.cos(phi_2d),
                      np.cos(theta_2d)])

    colormap = cm.ScalarMappable(cmap=plt.get_cmap("PRGn"))
    colormap.set_clim(-.45, .45)

    l_ = 2
    dxy = (1j * (sph_harm(-2, l_, phi_2d, theta_2d)
           - sph_harm(2, l_, phi_2d, theta_2d))
           / np.sqrt(2))
    dxy_r = np.abs(dxy.real)*xyz_2d

    ax.plot_surface(dxy_r[0]*3, dxy_r[1]*3,
                    dxy_r[2]*.0, alpha=.1,
                    facecolors=colormap.to_rgba(dxy.real),
                    rstride=2, cstride=2)

    X = np.zeros((2, 2))
    z = [0, 3.5]
    y = [-3, 3]
    Y, Z = np.meshgrid(y, z)
    ax.plot_surface(X, Y, Z, alpha=.2, color='C8')

    angdg = np.linspace(-15, 15, 100)
    tidg = 0
    k_1 = utils.det_angle(4, angdg, -40, tidg, 90)
    # k_2 = utils.det_angle(4, angdg, 0, 40, 0)
    y_hv = np.linspace(-2, -.25, 100)
    x_hv = .2*np.sin(y_hv*50)
    z_hv = -y_hv

    kx_i = k_i * np.sin(k_th) * np.cos(k_phi)
    ky_i = k_i * np.sin(k_th) * np.sin(k_phi)
    kz_i = k_i * np.cos(k_th)

    ax.quiver(0, 0, 0, 0, 0, 2.5, arrow_length_ratio=.08,
              color='k')
    ax.quiver(0, 0, 0, 0, 2.5, 0, arrow_length_ratio=.06,
              color='k')
    ax.quiver(0, 0, 0, 2.5, 0, 0, arrow_length_ratio=.08,
              color='k')
    ax.quiver(0, 0, 0, kx_i-.1, ky_i-.1, kz_i-.1, arrow_length_ratio=.08, lw=2,
              color='r')
    ax.quiver(x_hv[-1], y_hv[-1], z_hv[-1], .1, .3, -.2,
              arrow_length_ratio=.6, color='c')

    ax.quiver(0, -1.5, 1.5, 0, .7, .7, arrow_length_ratio=.2,
              color='b', lw=2)
    ax.quiver(0, -1.5, 1.5, .8, 0, 0, arrow_length_ratio=.2,
              color='b', lw=2)
    ax.plot([0, 0], [0, 0], [0, 0], 'o', mec='k', mfc='w', ms=5)
    ax.plot([kx_i, kx_i], [ky_i, ky_i], [kz_i, kz_i],
            'o', mec='k', mfc='k', ms=5)
    ax.plot([0, k_1[0, 0]], [0, k_1[1, 0]], [0, k_1[2, 0]], **kwargs_ef)
    ax.plot([0, k_1[0, -1]], [0, k_1[1, -1]], [0, k_1[2, -1]], **kwargs_ef)
    ax.plot(k_1[0], k_1[1], k_1[2], 'r-', lw=3)
    # ax.plot(k_2[0], k_2[1], k_2[2], 'r-', lw=3, alpha=.1)
    ax.plot(x_hv, y_hv, z_hv, 'c', lw=2)
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-2, 4])
    ax.set_aspect("equal")
    # ax.plot_surface(x_i, y_i, z_i, color="r", alpha=.05)

    # add text
    ax.text(0, -2.2, 2, r'$hv$', fontdict=font)
    ax.text(0, 2.3, 2., r'$e^-$', fontdict=font)
    ax.text(2.9, 0, 0, r'$x$', fontdict=font)
    ax.text(0, 2.6, 0, r'$y$', fontdict=font)
    ax.text(0, -.1, 2.6, r'$z$', fontdict=font)
    ax.text(2.8, 2.5, -0.25, 'SAMPLE', fontdict=font)
    ax.text(2., 1.3, 0, r'$d_{xy}$', fontdict=font)
    ax.text(0, -2.6, 2.6, 'Mirror plane', fontdict=font)
    ax.text(1.9, 0, 1.85, r'$\bar{\sigma}$', fontdict=font)
    ax.text(.8, 0, 2.15, r'$\bar{\pi}$', fontdict=font)
    ax.text(0, 2.2, 3.5, r'Detector', fontdict=font)
    kwargs_cyl = {'alpha': .05, 'color': 'k'}  # keywords cylinder

    # Cylinder
    r = 3
    x_cyl = np.linspace(-r, r, 100)
    z_cyl = np.linspace(-1, 0, 100)
    X_cyl, Z_cyl = np.meshgrid(x_cyl, z_cyl)
    Y_cyl = np.sqrt(r**2 - X_cyl**2)

    x_cir = r * np.cos(np.linspace(0, 2*np.pi, 360))
    y_cir = r * np.sin(np.linspace(0, 2*np.pi, 360))

    R, Phi = np.meshgrid(np.linspace(0, r, 100), np.linspace(0, 2*np.pi, 100))

    X_cir = R * np.cos(Phi)
    Y_cir = R * np.sin(Phi)
    Z_ceil = np.zeros((100, 100))
    Z_floor = -np.ones((100, 100))

    # draw cylinder
    ax.plot_surface(X_cyl, Y_cyl, Z_cyl, **kwargs_cyl)
    ax.plot_surface(X_cyl, -Y_cyl, Z_cyl, **kwargs_cyl)
    ax.plot_surface(X_cir, Y_cir, Z_floor, **kwargs_cyl)
    ax.plot_surface(X_cir, Y_cir, Z_ceil, **kwargs_cyl)
    ax.plot(x_cir, y_cir, 'k-', alpha=.1)
    ax.plot(x_cir, y_cir, -1, 'k--', alpha=.1, lw=.5)
    plt.axis('off')
    ax.view_init(elev=20, azim=50)

    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=300,
                    bbox_inches="tight")


def fig8(print_fig=True):
    """figure 8

    %%%%%%%%%%%%%%%%%%
    Data normalization
    %%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig8'

    mat = 'CSRO20'
    year = '2017'
    sample = 'S6'
    gold = '62091'

    D = ARPES.DLS(gold, mat, year, sample)
    D.norm(gold=gold)

    fig = plt.figure(figname, figsize=(8, 8), clear=True)
    ax1 = fig.add_subplot(321)
    ax1.set_position([.1, .5, .35, .35])
    ax1.tick_params(**kwargs_ticks)

    # plot data
    c0 = ax1.contourf(D.ang, D.en, np.transpose(D.int), 200, **kwargs_ex,
                      zorder=.1)
    ax1.set_rasterization_zorder(.2)

    # decorate axes
    ax1.set_xticklabels([])
    ax1.set_ylabel(r'$E_\mathrm{kin}$ (eV)', fontdict=font)

    ax2 = fig.add_subplot(322)
    ax2.set_position([.1, .14, .35, .35])
    ax2.tick_params(**kwargs_ticks)

    # plot data
    ax2.contourf(D.angs, D.en_norm, D.int_norm, 200, **kwargs_ex, zorder=.1)
    ax2.set_rasterization_zorder(.2)
    ax2.plot([D.ang[0], D.ang[-1]], [0, 0], **kwargs_ef)

    # decorate axes
    ax2.set_ylabel(r'$\omega$ (eV)', fontdict=font)
    ax2.set_xlabel(r'Detector angles', fontdict=font)

    # add text
    ax1.text(-15, 17.652, '(a)', fontdict=font)
    ax2.text(-15, 0.02, '(b)', fontdict=font)

    # colorbar
    pos = ax1.get_position()
    cax = plt.axes([pos.x0, pos.y0+pos.height+.01,
                    pos.width, .01])
    cbar = plt.colorbar(c0, cax=cax, ticks=None, orientation='horizontal')
    cbar.set_ticks([])

    # some constant
    Ef_ini = 17.645
    T_ini = 6
    bnd = 1
    ch = 300

    kB = 8.6173303e-5  # Boltzmann constant

    # create figure
    ax3 = fig.add_subplot(323)
    ax3.set_position([.55, .63, .35, .22])
    enval, inden = utils.find(D.en, Ef_ini-0.12)  # energy window

    # plot data
    ax3.plot(D.en[inden:], D.int[ch, inden:], 'bo', ms=2)

    # initial guess
    p_ini_FDsl = [T_ini * kB, Ef_ini, np.max(D.int[ch, :]), 20, 0]

    # Placeholders
    T_fit = np.zeros(len(D.ang))
    Res = np.zeros(len(D.ang))
    Ef = np.zeros(len(D.ang))
    norm = np.zeros(len(D.ang))

    # Fit loop
    for i in range(len(D.ang)):
        try:
            p_FDsl, c_FDsl = curve_fit(utils.FDsl, D.en[inden:],
                                       D.int[i, inden:], p_ini_FDsl)
        except RuntimeError:
            print("Error - convergence not reached")

        # Plots data at this particular channel
        if i == ch:
            ax3.plot(D.en[inden:], utils.FDsl(D.en[inden:],
                     *p_FDsl), 'r-')

        T_fit[i] = p_FDsl[0] / kB
        Res[i] = np.sqrt(T_fit[i] ** 2 - T_ini ** 2) * 4 * kB
        Ef[i] = p_FDsl[1]  # Fit parameter

    # Fit Fermi level fits with a polynomial
    p_ini_poly2 = [Ef[ch], 0, 0, 0]
    p_poly2, c_poly2 = curve_fit(utils.poly_2, D.ang[bnd:-bnd],
                                 Ef[bnd:-bnd], p_ini_poly2)
    Ef_fit = utils.poly_2(D.ang, *p_poly2)

    # boundaries if strong curvature in Fermi level
    mx = np.max(D.en) - np.max(Ef_fit)
    mn = np.min(Ef_fit) - np.min(D.en)
    for i in range(len(D.ang)):
        mx_val, mx_idx = utils.find(D.en, Ef_fit[i] + mx)
        mn_val, mn_idx = utils.find(D.en, Ef_fit[i] - mn)
        norm[i] = np.sum(D.int[i, mn_idx:mx_idx])  # normalization

    # Plot data
    ax4 = fig.add_subplot(324)
    ax4.set_position([.55, .14, .35, .22])
    ax4.plot(D.ang, Res * 1e3, 'bo', ms=3)
    print("Resolution ~" + str(np.mean(Res)) + "eV")
    ax5 = fig.add_subplot(325)
    ax5.set_position([.55, .37, .35, .22])
    ax5.plot(D.ang, Ef, 'bo', ms=3)
    ax5.plot(D.ang[bnd], Ef[bnd], 'ro')
    ax5.plot(D.ang[-bnd], Ef[-bnd], 'ro')
    ax5.plot(D.ang, Ef_fit, 'r-')

    # decorate axes
    ax3.tick_params(**kwargs_ticks)
    ax3.set_ylim(0, 1400)
    ax4.tick_params(**kwargs_ticks)
    ax5.set_xticklabels([])
    ax3.xaxis.set_label_position('top')
    ax3.tick_params(labelbottom='off', labeltop='on')
    ax5.tick_params(**kwargs_ticks)
    ax3.set_xlabel(r'$\omega$', fontdict=font)
    ax3.set_ylabel('Intensity (a.u.)', fontdict=font)
    ax4.set_ylabel('Resolution (meV)', fontdict=font)
    ax4.set_xlabel('Detector angles', fontdict=font)
    ax5.set_ylabel(r'$\omega$ (eV)', fontdict=font)
    ax5.set_ylim(D.en[0], D.en[-1])

    # add text
    ax3.text(17.558, 1250, '(c)', fontdict=font)
    ax5.text(-17, 17.648, '(d)', fontdict=font)
    ax4.text(-17, 12.1, '(e)', fontdict=font)

    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig9(print_fig=True):
    """figure 9

    %%%%%%%%%%%%%%%%%
    Analyzer energies
    %%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig9'

    fig = plt.figure(figname, figsize=(8, 8), clear=True)

    ax = fig.add_axes([.2, .2, .6, .6])
    ax.tick_params(**kwargs_ticks)

    # plot lines
    ax.plot([.5, 1], [0, 0], **kwargs_ef)
    ax.plot([1, 1], [-1, 0], 'k-')
    ax.plot([1, 1.5], [0, 2], 'k-')
    ax.plot([1.5, 1.5], [2, 1], 'k-')
    ax.plot([1.5, 2], [2, 2], **kwargs_ef)
    ax.plot([.75, 1.8], [2.75, 2.75], **kwargs_ef)
    ax.plot([1, 2], [-.5, -.5], **kwargs_ef)
    ax.plot([.75, .9], [-.85, -.85], **kwargs_ef)
    ax.arrow(.75, -.85, 0, 3.45, head_width=0.02, head_length=0.1, fc='r',
             ec='r', lw=.2)
    ax.plot(.75, -.85, 'o', markeredgecolor='k', markerfacecolor='w')
    ax.plot(.75, 2.75, 'ko')
    xx = np.linspace(.45, .7, 100)
    yy = -.1*np.sin(xx*99) + 2 - xx
    ax.plot(xx, yy, 'c-')
    ax.arrow(.6, -.25, 0, .15, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(.6, -.25, 0, -.15, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(.85, -.65, 0, .05, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(.85, -.65, 0, -.1, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(.85, 0, 0, -.4, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(.85, 0, 0, 2.6, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(1.65, 0, 0, -.4, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(1.65, 0, 0, 1.4, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(1.65, 1.7, 0, -.1, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(1.65, 1.7, 0, .2, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(1.65, 2.3, 0, -.2, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(1.65, 2.3, 0, .35, head_width=0.02, head_length=0.1,
             fc='k', ec='k')
    ax.arrow(.702, 1.275, .02, -.03, head_width=0.03, head_length=0.03, lw=1.2,
             fc='c', ec='c')

    ax.plot([1.8, 1.85], [2.5, 2.5], 'k-')
    ax.plot([1.8, 1.85], [3, 3], 'k-')
    ax.plot([1.8, 1.8], [2.5, 3], 'k-')
    ax.plot([1.85, 1.85], [2.5, 3], 'k-')
    ax.fill_between([1.8, 1.85], [2.5, 2.5], [3, 3], color='m')
    ax.fill_between([1.5, 2], [1.5, 1.5], [1, 1], color='k', alpha=.3)
    ax.fill_between([.5, 1], [-1, -1], [-.5, -.5], color='C8', alpha=1)

    # add text
    ax.text(.62, -.3, r'$\Phi$', fontdict=font)
    ax.text(.88, -.7, r'$E_\mathrm{B}$', fontdict=font)
    ax.text(.88, 1, r'$E_\mathrm{kin}$', fontdict=font)
    ax.text(.4, -.05, r'$E_\mathrm{vac}$', fontdict=font)
    ax.text(.4, -.55, r'$E_\mathrm{F}$', fontdict=font)
    ax.text(2.01, 1.45, r'$E_\mathrm{F}$', fontdict=font)
    ax.text(2.01, 1.95, r'$E_\mathrm{vac}$', fontdict=font)
    ax.text(1.67, 2.3, r'$E_\mathrm{p}$', fontdict=font)
    ax.text(1.67, 1.7, r'$\Phi_\mathrm{A}$', fontdict=font)
    ax.text(1.67, .4, r'$eV_\mathrm{R}$', fontdict=font)
    ax.text(.53, -.72, 'Sample', fontdict=font)
    ax.text(1.7, 1.2, 'Analyzer', fontdict=font)
    ax.text(.55, 1.65, r'$h \nu$', fontdict=font)
    ax.text(1.88, 2.7, 'MCP', fontdict=font)
    ax.set_xlim(0.3, 2.2)
    ax.set_ylim(-1.2, 3.3)
    plt.axis('off')

    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig10(print_fig=True):
    """figure 10

    %%%%%%%%%%%%%%
    Analyzer setup
    %%%%%%%%%%%%%%
    """

    figname = 'CONfig10'

    fig = plt.figure(figname, figsize=(8, 8), clear=True)

    ax = fig.add_axes([.2, .2, .6, .6])
    ax.tick_params(**kwargs_ticks)

    r1 = 1.5
    r2 = 2
    r3 = 3

    r4 = 1.75
    r5 = 1.75

    phi = np.linspace(0, np.pi, 100)
    x1 = r1 * np.cos(phi)
    x2 = r2 * np.cos(phi)
    x3 = r3 * np.cos(phi)
    x4 = r4 * np.cos(phi)
    x5 = r5 * np.cos(phi)
    y1 = r1 * np.sin(phi) + 5
    y2 = r2 * np.sin(phi) + 5
    y3 = r3 * np.sin(phi) + 5
    y4 = r4 * np.sin(phi) + 4.9
    y5 = r5 * np.sin(phi) + 5.1
    phi_i1 = np.linspace(11/12*np.pi, 13/12*np.pi, 100)
    phi_i2 = np.linspace(-1/12*np.pi, 1/12*np.pi, 100)
    xi1 = 7.5 * np.cos(phi_i1) + 5.5
    yi1 = 7.5 * np.sin(phi_i1) + 3.15
    xi2 = 7.5 * np.cos(phi_i2) - 9
    yi2 = 7.5 * np.sin(phi_i2) + 3.15

    # round geometries
    ax.plot(x1, y1, 'k-', x2, y2, 'k-', x3, y3, 'k-')
    ax.plot(x4, y4, 'k--', x5, y5, 'k--')
    ax.plot(xi1, yi1, 'k--')
    ax.plot(xi2, yi2, 'k--')

    # herzog plate
    ax.plot([-r3, -r2], [5, 5], 'k-',
            [r2, r3], [5, 5], 'k-',
            [-r1, r1], [5, 5], 'k-')
    ax.plot([-r3, -r2], [4.9, 4.9], 'k-',
            [r2, r3], [4.9, 4.9], 'k-',
            [-r1, r1], [4.9, 4.9], 'k-')
    ax.plot([-r3, -r2], [4.8, 4.8], 'k-',
            [r2, r3], [4.8, 4.8], 'k-',
            [-r1, r1], [4.8, 4.8], 'k-')
    ax.plot([-r1, -r1], [4.8, 4.9], 'k-',
            [-r2, -r2], [4.8, 4.9], 'k-',
            [-r3, -r3], [4.8, 4.9], 'k-')
    ax.plot([r1, r1], [4.8, 4.9], 'k-',
            [r2, r2], [4.8, 4.9], 'k-',
            [r3, r3], [4.8, 4.9], 'k-')
    ax.fill_between([-r3, -r2], 4.8, 4.9, color='k', alpha=.3)
    ax.fill_between([r2, r3], 4.8, 4.9, color='k', alpha=.3)
    ax.fill_between([-r1, r1], 4.8, 4.9, color='k', alpha=.3)
    # MCP
    ax.plot([1.3, 2.2], [4.2, 4.2], 'k-',
            [1.3, 2.2], [4., 4.], 'k-',
            [1.3, 1.3], [4., 4.2], 'k-',
            [2.2, 2.2], [4., 4.2], 'k-')
    ax.fill_between([1.3, 2.2], [4, 4], [4.2, 4.2], color='m')

    # beam onto MCP
    ax.plot([1.75, 1.9], [5, 4.2], 'k--')
    ax.plot([1.75, 1.6], [5, 4.2], 'k--')

    # lenses
    ax.plot([-2.5, -2.2], [4.5, 4.5], 'k-',
            [-1.3, -1], [4.5, 4.5], 'k-',
            [-2.5, -2.2], [4., 4.], 'k-',
            [-1.3, -1], [4., 4.], 'k-')
    ax.plot([-2.5, -2.5], [4, 4.5], 'k-',
            [-2.2, -2.2], [4, 4.5], 'k-',
            [-1.3, -1.3], [4, 4.5], 'k-',
            [-1., -1.], [4, 4.5], 'k-')
    ax.plot([-2.5, -2.2], [3.5, 3.5], 'k-',
            [-1.3, -1], [3.5, 3.5], 'k-',
            [-2.5, -2.2], [3., 3.], 'k-',
            [-1.3, -1], [3., 3.], 'k-')
    ax.plot([-2.5, -2.5], [3, 3.5], 'k-',
            [-2.2, -2.2], [3, 3.5], 'k-',
            [-1.3, -1.3], [3, 3.5], 'k-',
            [-1., -1.], [3, 3.5], 'k-')
    ax.plot([-2.5, -2.2], [2.5, 2.5], 'k-',
            [-1.3, -1], [2.5, 2.5], 'k-',
            [-2.5, -2.2], [2., 2.], 'k-',
            [-1.3, -1], [2., 2.], 'k-')
    ax.plot([-2.5, -2.5], [2, 2.5], 'k-',
            [-2.2, -2.2], [2, 2.5], 'k-',
            [-1.3, -1.3], [2, 2.5], 'k-',
            [-1., -1.], [2, 2.5], 'k-')

    # grounding
    ax.plot([-2, -1.5], [.7, .7], 'k-',
            [-2, -1.5], [.6, .6], 'k-',
            [-2, -2], [.6, .7], 'k-',
            [-1.5, -1.5], [.6, .7], 'k-')
    ax.fill_between([-2, -1.5], .6, .7, color='C8')
    ax.plot([-1.75, -1.75], [.6, .3], 'k-')
    ax.plot([-1.95, -1.55], [.3, .3], 'k-')
    ax.plot([-1.9, -1.6], [.22, .22], 'k-')
    ax.plot([-1.85, -1.65], [.15, .15], 'k-')

    ax.plot([-r1, -r1], [5, 8.15], 'k-', lw=1)
    ax.plot([-r2, -r2], [5, 8.15], 'k-', lw=1)
    xx = np.linspace(-3.5, -2.2, 100)
    yy = -.1 * np.sin(xx * 30) - .3 - .5 * xx
    ax.plot(xx, yy, 'c-')
    ax.arrow(-2.2, .8, .08, -.06, head_width=0.12, head_length=0.12, lw=1.2,
             fc='c', ec='c')

    ax.arrow(-2, 3.1, 0, 0, head_width=0.2, head_length=0.2,
             fc='k', ec='k')
    ax.arrow(-1.5, 3.1, 0, 0, head_width=0.2, head_length=0.2,
             fc='k', ec='k')
    ax.arrow(-.1, 6.85, 0.001, 0, head_width=0.2, head_length=0.2,
             fc='k', ec='k')
    ax.arrow(-.1, 6.65, 0.001, 0, head_width=0.2, head_length=0.2,
             fc='k', ec='k')

    ax.arrow(0, 5, .9, .95, head_width=0.1, head_length=0.15,
             fc='k', ec='k')
    ax.arrow(0, 5, .8, 2.7, head_width=0.1, head_length=0.15,
             fc='k', ec='k')
    ax.arrow(-1.75, 8, -.1, 0, head_width=0.1, head_length=0.15,
             fc='k', ec='k')
    ax.arrow(-1.75, 8, .1, 0, head_width=0.1, head_length=0.15,
             fc='k', ec='k')
    ax.plot(-1.75, 1., 'ko', ms=7)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-.5, 8.5)

    # add text
    ax.text(1.4, 3.6, 'MCP', fontdict=font)
    ax.text(-.8, 3.2, 'Electrostatic', fontdict=font)
    ax.text(-.8, 2.85, 'lenses', fontdict=font)
    ax.text(-1.5, .9, r'$e^-$', fontdict=font)
    ax.text(-1.3, .4, 'Sample', fontdict=font)
    ax.text(-4, 1.5, r'$h\nu$', fontdict=font)
    ax.text(-1.9, 8.2, r'$w$', fontdict=font)
    ax.text(.55, 5.3, r'$r_1$', fontdict=font)
    ax.text(.8, 7.2, r'$r_2$', fontdict=font)
    plt.axis('off')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig11(print_fig=True):
    """figure 11

    %%%%%%%%%%%%%%
    Laue + Crystal
    %%%%%%%%%%%%%%
    """

    figname = 'CONfig11'

    fig = plt.figure(figname, figsize=(10, 4), clear=True)

    ax1 = fig.add_subplot(121)
    ax1.tick_params(**kwargs_ticks)
    ax1.set_position([.1, .29, .5, .5])
    ax1.set_xticks([])
    ax1.set_yticks([])
    laue = mpimg.imread(data_dir+'CON11a.jpg')
    laue = laue[:, 20:-20]
    phi = np.linspace(-np.pi/2, -np.pi/4*3+.05)
    x = 313 + 160 * np.cos(phi)
    y = 220 + 160 * np.sin(phi)

    ax1.imshow(laue, cmap='gray')
    ax1.plot([258, 225], [100, 30], 'k--', lw=.5)
    ax1.plot([224, 165], [120, 60], 'k--', lw=.5)
    ax1.plot([312, 313], [85, 35], 'k--', lw=.5)
    ax1.plot(x, y, 'k--', lw=.5)
    ax1.text(10, 35, '(a)', fontdict=font)
    ax1.text(270, 95, r'$\alpha_1$')
    ax1.text(222, 110, r'$\alpha_2$')
    ax1.text(258, 30, 'Ru-O-Ru')
    ax1.text(125, 55, 'Ru-Ru')

    ax2 = fig.add_subplot(122)
    ax2.tick_params(**kwargs_ticks)
    ax2.set_position([.4, .29, .5, .5])
    ax2.set_xticks([])
    ax2.set_yticks([])
    crystal = mpimg.imread(data_dir+'CON11b.jpg')
    crystal = crystal[70:1200, :, :]
    ax2.imshow(crystal)
    ax2.text(20, 90, '(b)', fontdict=font)

    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=300,
                    bbox_inches="tight")


def fig12(print_fig=True):
    """figure 12

    %%%%%%%%%%%%%%%%%%%%%%%%
    Inelastic mean free path
    %%%%%%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig12'

    # load data
    os.chdir(data_dir)
    data = np.genfromtxt('IMFP.csv', delimiter=',')
    E_kin = data[:, 0]
    IMFP = data[:, 1]
    xx = np.linspace(E_kin[0], E_kin[-1], 1000)
    lamb = 143 / xx ** 2 + .053 * np.sqrt(xx)

    # create figure
    fig = plt.figure(figname, figsize=(6, 6), clear=True)
    ax = fig.add_axes([.2, .2, .6, .6])
    ax.tick_params(**kwargs_ticks)

    # plot data
    ax.loglog(E_kin, IMFP, 'ko', ms=3)
    ax.loglog(xx, lamb, 'r--')
    ax.fill_between([10, 1e3], .1, 2, color='C0', alpha=.3)
    ax.fill_between([6, 10], .1, 12, color='c', alpha=.3)
    ax.fill_between([1e3, 5e3], .1, 10, color='b', alpha=.3)

    # decorate axes
    ax.set_xlabel('Electron energy (eV)', fontdict=font)
    ax.set_ylabel(r'$\lambda_\mathrm{IMFP}$ (nm)', fontdict=font)
    ax.set_ylim(.1, 1e3)

    # add text
    ax.text(5, 15, 'Laser', color='c')
    ax.text(30, 2.7, 'Conventional', color='C0')
    ax.text(1e3, 13, 'Soft X-ray', color='b')
    ax.text(1.5, 3e2,
            (r'$\lambda_\mathrm{IMFP} \simeq (143$' +
             r'$\cdot E\,\mathrm{[eV]}^{-2} + 0.054$' +
             r'$ \cdot \sqrt{E\,\mathrm{[eV]}})\,\mathrm{nm}$'),
            color='r')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig13(print_fig=True):
    """figure 13

    %%%%%%%%%%%%%
    Sr2RuO4 model
    %%%%%%%%%%%%%
    """

    figname = 'CONfig13'

    fig = plt.figure(figname, figsize=(5, 8), clear=True)

    ax = fig.add_axes([.1, .1, .8, .8], projection='3d')
    ax.tick_params(**kwargs_ticks)

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    X0 = .25 * np.outer(np.cos(u), np.sin(v))
    Y0 = .25 * np.outer(np.sin(u), np.sin(v))
    Z0 = .25 * np.outer(np.ones(np.size(u)), np.cos(v))
    X = .15 * np.outer(np.cos(u), np.sin(v))
    Y = .15 * np.outer(np.sin(u), np.sin(v))
    Z = .15 * np.outer(np.ones(np.size(u)), np.cos(v))
    Xs = .3 * np.outer(np.cos(u), np.sin(v))
    Ys = .3 * np.outer(np.sin(u), np.sin(v))
    Zs = .3 * np.outer(np.ones(np.size(u)), np.cos(v))

    def cc(arg):
        return mcolors.to_rgba(arg, alpha=.75)

    def triang(x0, y0, z0, x, y, z):
        X = [x0+x, 0+x, 0+x]
        Y = [0+y, 0+y, y0+y]
        Z = [0+z, z0+z, 0+z]
        verts = [list(zip(X, Y, Z))]
        return verts

    def octahedron(x, y, z):
        v1 = triang(-1, 1, 1, x, y, z)
        v2 = triang(-1, -1, 1, x, y, z)
        v3 = triang(-1, -1, -1, x, y, z)
        v4 = triang(-1, 1, -1, x, y, z)
        v5 = triang(1, 1, 1, x, y, z)
        v6 = triang(1, -1, 1, x, y, z)
        v7 = triang(1, -1, -1, x, y, z)
        v8 = triang(1, 1, -1, x, y, z)
        V = [v1, v2, v3, v4, v5, v6, v7, v8]
        for i in range(8):
            ax.add_collection3d(Poly3DCollection(V[i], facecolors=cc('w'),
                                                 edgecolor=cc('k')), zs='z')

        ax.plot_surface(X0 + x, Y0 + y, Z0 + z,  rstride=4,
                        cstride=4, color='r', lw=0)
        ax.plot_surface(X + x, Y + y, Z + z + 1,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y, Z + z - 1,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y + 1, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y - 1, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x + 1, Y + y, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x - 1, Y + y, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)

#    ax.plot([1, 1], [1, 1], [3, -3], 'k-')
#    ax.plot([-1, -1], [1, 1], [3, -3], 'k-')
#    ax.plot([1, 1], [-1, -1], [3, -3], 'k-')
#    ax.plot([-1, -1], [-1, -1], [3, -3], 'k-')
#    ax.plot([-1, 1], [-1, -1], [1, 1], 'k-')
#    ax.plot([-1, 1], [-1, -1], [-1, -1], 'k-')
#    ax.plot([-1, -1], [1, -1], [1, 1], 'k-')
#    ax.plot([-1, -1], [1, -1], [-1, -1], 'k-')
#    ax.plot([1, 1], [1, -1], [1, 1], 'k-')
#    ax.plot([1, 1], [1, -1], [-1, -1], 'k-')
#    ax.plot([-1, 1], [1, 1], [1, 1], 'k-')
#    ax.plot([-1, 1], [1, 1], [-1, -1], 'k-')
    ax.plot_surface(Xs + 1, Ys + 1, Zs + 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs + 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs + 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs + 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys + 1, Zs - 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs - 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs - 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs - 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs, Ys, Zs - 2, rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs, Ys, Zs + 2, rstride=4,
                    cstride=4, color='c', lw=0)

    octahedron(0, 0, 0)
    octahedron(1, 1, 3)
    octahedron(1, 1, -3)
    octahedron(1, -1, 3)
    octahedron(1, -1, -3)
    octahedron(-1, 1, 3)
    octahedron(-1, 1, -3)
    octahedron(-1, -1, 3)
    octahedron(-1, -1, -3)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-2.5, 2.5)
    ax.view_init(elev=7, azim=20)
    plt.axis('off')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=200,
                    bbox_inches="tight")


def fig14(print_fig=True):
    """figure 14

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Fermi liquid scattering scheme
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig14'

    fig = plt.figure(figname, figsize=(5, 2.5), clear=True)

    ax = fig.add_axes([0, 0, 1, 1])
    ax.tick_params(**kwargs_ticks)

    def circ(R):
        phi = np.linspace(0, 2*np.pi, 100)
        x = R * np.cos(phi)
        y = R * np.sin(phi)
        return x, y

    # coordinates
    x_a, y_a = circ(.5)
    x_a -= 1
    x_inner, y_inner = circ(.3)
    x_outer, y_outer = circ(.7)

    # plot data panel (a)
    ax.plot(x_a, y_a, color='k', lw=1)
    ax.plot(x_a+2, y_a, color='k', lw=1)
    ax.plot(-1.2, -.3, 'ko', markerfacecolor='w')
    ax.plot(-.5, .35, 'ko', markerfacecolor='w')
    ax.plot(-.9, .6, 'ko')
    ax.plot(-.8, -.55, 'ko')
    ax.arrow(-1.2, -.3, .275, .82, head_width=0.05, head_length=0.05,
             fc='k', ec='k', lw=.5)
    ax.arrow(-.5, .35, -.27, -.82, head_width=0.05, head_length=0.05,
             fc='k', ec='k', lw=.5)

    # plot data panel (b)
    ax.arrow(.4, 0, -.05, 0, head_width=0.05, head_length=0.05,
             fc='k', ec='k', lw=.5)
    ax.arrow(.4, 0, .05, 0, head_width=0.05, head_length=0.05,
             fc='k', ec='k', lw=.5)
    ax.arrow(1, -.4, 0, -.05, head_width=0.05, head_length=0.05,
             fc='k', ec='k', lw=.5)
    ax.arrow(1, -.4, 0, .05, head_width=0.05, head_length=0.05,
             fc='k', ec='k', lw=.5)
    ax.plot(x_outer+1, y_outer, 'k--')
    ax.fill_between(x_a, 0, y_a, color='C0')
    ax.fill_between(x_a+2, 0, y_a, color='C0')
    ax.fill_between(x_inner+1, 0, y_inner, color=(0, 0, .4))

    # add text
    ax.text(-1.6, .7, '(a)', fontdict=font)
    ax.text(.3, .7, '(b)', fontdict=font)
    ax.text(-1.33, -.28, r'$\mathbf{k}^\prime$', fontdict=font)
    ax.text(-.83, .57, r'$\mathbf{k}^\prime - \mathbf{q}$', fontdict=font)
    ax.text(-.43, .31, r'$\mathbf{k}$', fontdict=font)
    ax.text(-1.15, -.65, r'$\mathbf{k} + \mathbf{q}$', fontdict=font)
#    ax.text(.36, .08, r'$\epsilon_\mathbf{k}^q$', fontdict=font)
#    ax.text(1.05, -.42, r'$\epsilon_\mathbf{k}^q$', fontdict=font)
    ax.text(.36, .08, r'$\omega$', fontdict=font)
    ax.text(1.05, -.42, r'$\omega$', fontdict=font)

    # axes
    ax.set_ylim(-.9, .9)
    ax.set_xlim(-1.8, 1.8)
    plt.axis('off')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig15(print_fig=True):
    """figure 15

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Fermi liquid momentum distribution
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig15'

    k = np.linspace(-1.5, 1, 300)
    k_1 = np.linspace(-1.5, 0, 300)
    k_2 = np.linspace(0, 1, 300)

    kF = 0

    n_0 = utils.FDsl(k, 0, kF, 1, 0, 0)
    n_1 = utils.FDsl(k_1, .3, kF+.5, 1, 0, 0)
    n_2 = utils.FDsl(k_2, .3, kF-.5, 1, 0, 0)

    fig = plt.figure(figname, figsize=(6, 6), clear=True)

    ax1 = fig.add_axes([.18, .35, .3, .3])
    ax2 = fig.add_axes([.5, .35, .3, .3])
    ax1.tick_params(**kwargs_ticks)
    ax2.tick_params(**kwargs_ticks)

    ax1.plot(k, n_0, 'k-')
    ax1.plot([-2, 1], [0, 0], **kwargs_ef)
    ax2.plot([-2, 1], [0, 0], **kwargs_ef)
    ax2.plot(k_1, n_1, 'k-')
    ax2.plot(k_2, n_2, 'k-')
    ax2.plot([0, 0], [n_1[-1], n_2[0]], 'k-')
    ax2.arrow(.2, .5, 0, .27, head_width=0.05, head_length=0.05,
              fc='k', ec='k', zorder=3)
    ax2.arrow(.2, .5, 0, -.27, head_width=0.05, head_length=0.05,
              fc='k', ec='k', zorder=3)

    # decorate axes
    ax1.set_xlim(-1.5, 1)
    ax1.set_ylim(-.1, 1.2)
    ax1.set_xticks([0])
    ax2.set_xticks([0])
    ax1.set_xticklabels([r'$\mathbf{k}_\mathrm{F}$'], fontdict=font)
    ax2.set_xticklabels([r'$\mathbf{k}_\mathrm{F}$'], fontdict=font)
    ax1.set_yticks([0, 1])
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels([])
    ax2.set_xlim(-1.5, 1)
    ax2.set_ylim(-.1, 1.2)
    ax1.set_ylabel(r'$n_\mathbf{k}$', fontdict=font)

    ax2.text(.3, .48, '$Z$', fontdict=font)
    plt.show()
    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig16(print_fig=True):
    """figure 16

    %%%%%%%%%%%%%%%%%%%%
    Filling control Mott
    %%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig16'

    def Ellipse(R, w):
        # semi circle
        th = np.linspace(0, -np.pi, 200)
        r = R / np.sqrt(1 - (w * np.cos(th)) ** 2)
        x = r * np.cos(th)
        y = r * np.sin(th)
        return x, y

    x1, y1 = Ellipse(1.5, .95)
    x2, y2 = Ellipse(1.5, .88)
    x3, y3 = Ellipse(1.5, 0)

    fig = plt.figure(figname, figsize=(6, 6), clear=True)

    ax = fig.add_axes([.3, .3, .4, .4])
    ax.tick_params(**kwargs_ticks)
    ax.plot(x1, y1, 'C0--', x2, y2, 'b--', x3, y3, 'k--')
    ax.plot([0, 0], [-1.5, 0], 'r-', lw=5)
    ax.fill_between(x1, y1, 0, color='C0', alpha=.2)
    ax.fill_between(x2, y2, 0, color='b', alpha=.2)
    ax.fill_between(x3, y3, 0, color='k', alpha=.2)

    ax.arrow(0, -1.75, 0, .2, head_width=.3, head_length=.1, fc='k',
             ec='k', lw=1, zorder=2)

    ax.set_xlim(-6., 6)
    ax.set_ylim(-2, 0)
    ax.set_xticks([-6, 0, 6])
    ax.set_xticklabels((0, 1, 2))
    ax.set_yticks([])
    ax.set_yticklabels(['$U_c$'], fontdict=font)
    ax.set_xlabel('band filling $n$', fontdict=font)
    ax.set_ylabel('Coulomb $U$', fontdict=font)

    ax.text(-2.3, -1.85, 'Mott-insulator', fontdict=font)
    ax.text(.8, -.2, 'AF-I',  rotation='vertical',
            horizontalalignment='center', color='k')
    ax.text(2.4, -.2, 'AF-M',  rotation='vertical',
            horizontalalignment='center', color='b')
    ax.text(4., -.2, 'PM-M',  rotation='vertical',
            horizontalalignment='center', color='C0')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig17(print_fig=True):
    """figure 17

    %%%%%%%%%%%%%%
    Bi-layer model
    %%%%%%%%%%%%%%
    """

    figname = 'CONfig17'

    fig = plt.figure(figname, figsize=(5, 8), clear=True)

    ax = fig.add_axes([.1, .1, .8, .8], projection='3d')
    ax.tick_params(**kwargs_ticks)

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    X0 = .25 * np.outer(np.cos(u), np.sin(v))
    Y0 = .25 * np.outer(np.sin(u), np.sin(v))
    Z0 = .25 * np.outer(np.ones(np.size(u)), np.cos(v))
    X = .15 * np.outer(np.cos(u), np.sin(v))
    Y = .15 * np.outer(np.sin(u), np.sin(v))
    Z = .15 * np.outer(np.ones(np.size(u)), np.cos(v))
    Xs = .3 * np.outer(np.cos(u), np.sin(v))
    Ys = .3 * np.outer(np.sin(u), np.sin(v))
    Zs = .3 * np.outer(np.ones(np.size(u)), np.cos(v))

    def cc(arg):
        return mcolors.to_rgba(arg, alpha=.75)

    def triang(x0, y0, z0, x, y, z):
        X = [x0+x, 0+x, 0+x]
        Y = [0+y, 0+y, y0+y]
        Z = [0+z, z0+z, 0+z]
        verts = [list(zip(X, Y, Z))]
        return verts

    def octahedron(x, y, z):
        v1 = triang(-1, 1, 1, x, y, z)
        v2 = triang(-1, -1, 1, x, y, z)
        v3 = triang(-1, -1, -1, x, y, z)
        v4 = triang(-1, 1, -1, x, y, z)
        v5 = triang(1, 1, 1, x, y, z)
        v6 = triang(1, -1, 1, x, y, z)
        v7 = triang(1, -1, -1, x, y, z)
        v8 = triang(1, 1, -1, x, y, z)
        V = [v1, v2, v3, v4, v5, v6, v7, v8]
        for i in range(8):
            ax.add_collection3d(Poly3DCollection(V[i], facecolors=cc('w'),
                                                 edgecolor=cc('k')), zs='z')

        ax.plot_surface(X0 + x, Y0 + y, Z0 + z,  rstride=4,
                        cstride=4, color='r', lw=0)
        ax.plot_surface(X + x, Y + y, Z + z + 1,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y, Z + z - 1,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y + 1, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y - 1, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x + 1, Y + y, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x - 1, Y + y, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)

#    ax.plot([1, 1], [1, 1], [4, -4], 'k-')
#    ax.plot([-1, -1], [1, 1], [4, -4], 'k-')
#    ax.plot([1, 1], [-1, -1], [4, -4], 'k-')
#    ax.plot([-1, -1], [-1, -1], [4, -4], 'k-')
#    ax.plot([-1, 1], [-1, -1], [2, 2], 'k-')
#    ax.plot([-1, 1], [-1, -1], [-2, -2], 'k-')
#    ax.plot([-1, -1], [1, -1], [2, 2], 'k-')
#    ax.plot([-1, -1], [1, -1], [-2, -2], 'k-')
#    ax.plot([1, 1], [1, -1], [2, 2], 'k-')
#    ax.plot([1, 1], [1, -1], [-2, -2], 'k-')
#    ax.plot([-1, 1], [1, 1], [2, 2], 'k-')

    ax.plot_surface(Xs + 1, Ys + 1, Zs + 2,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs + 2,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs + 2,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs + 2,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys + 1, Zs,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys + 1, Zs - 2,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs - 2,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs - 2,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs - 2,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs, Ys, Zs - 3, rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs, Ys, Zs + 3, rstride=4,
                    cstride=4, color='c', lw=0)

    octahedron(0, 0, -1)
    octahedron(0, 0, 1)
    octahedron(1, 1, 4)
    octahedron(1, 1, -4)
    octahedron(1, -1, 4)
    octahedron(1, -1, -4)
    octahedron(-1, 1, 4)
    octahedron(-1, 1, -4)
    octahedron(-1, -1, 4)
    octahedron(-1, -1, -4)

    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.75, 1.75)
    ax.set_zlim(-3, 3)
    ax.view_init(elev=7, azim=20)
    plt.axis('off')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=200,
                    bbox_inches="tight")


def fig18(print_fig=True):
    """figure 18

    %%%%%%%%%%%%%%%
    Tri-layer model
    %%%%%%%%%%%%%%%
    """

    figname = 'CONfig18'

    fig = plt.figure(figname, figsize=(5, 8), clear=True)

    ax = fig.add_axes([.1, .1, .8, .8], projection='3d')
    ax.tick_params(**kwargs_ticks)

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    X0 = .25 * np.outer(np.cos(u), np.sin(v))
    Y0 = .25 * np.outer(np.sin(u), np.sin(v))
    Z0 = .25 * np.outer(np.ones(np.size(u)), np.cos(v))
    X = .15 * np.outer(np.cos(u), np.sin(v))
    Y = .15 * np.outer(np.sin(u), np.sin(v))
    Z = .15 * np.outer(np.ones(np.size(u)), np.cos(v))
    Xs = .3 * np.outer(np.cos(u), np.sin(v))
    Ys = .3 * np.outer(np.sin(u), np.sin(v))
    Zs = .3 * np.outer(np.ones(np.size(u)), np.cos(v))

    def cc(arg):
        return mcolors.to_rgba(arg, alpha=.75)

    def triang(x0, y0, z0, x, y, z):
        X = [x0+x, 0+x, 0+x]
        Y = [0+y, 0+y, y0+y]
        Z = [0+z, z0+z, 0+z]
        verts = [list(zip(X, Y, Z))]
        return verts

    def octahedron(x, y, z):
        v1 = triang(-1, 1, 1, x, y, z)
        v2 = triang(-1, -1, 1, x, y, z)
        v3 = triang(-1, -1, -1, x, y, z)
        v4 = triang(-1, 1, -1, x, y, z)
        v5 = triang(1, 1, 1, x, y, z)
        v6 = triang(1, -1, 1, x, y, z)
        v7 = triang(1, -1, -1, x, y, z)
        v8 = triang(1, 1, -1, x, y, z)
        V = [v1, v2, v3, v4, v5, v6, v7, v8]
        for i in range(8):
            ax.add_collection3d(Poly3DCollection(V[i], facecolors=cc('w'),
                                                 edgecolor=cc('k')), zs='z')

        ax.plot_surface(X0 + x, Y0 + y, Z0 + z,  rstride=4,
                        cstride=4, color='r', lw=0)
        ax.plot_surface(X + x, Y + y, Z + z + 1,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y, Z + z - 1,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y + 1, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y - 1, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x + 1, Y + y, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x - 1, Y + y, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)

    ax.plot_surface(Xs + 1, Ys + 1, Zs + 3,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs + 3,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs + 3,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs + 3,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys + 1, Zs + 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs + 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs + 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs + 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys + 1, Zs - 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs - 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs - 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs - 1,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys + 1, Zs - 3,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys - 1, Zs - 3,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs - 1, Ys + 1, Zs - 3,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs + 1, Ys - 1, Zs - 3,  rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs, Ys, Zs - 4, rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs, Ys, Zs + 4, rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs, Ys, Zs - 6, rstride=4,
                    cstride=4, color='c', lw=0)
    ax.plot_surface(Xs, Ys, Zs + 6, rstride=4,
                    cstride=4, color='c', lw=0)

    octahedron(0, 0, 0)
    octahedron(0, 0, -2)
    octahedron(0, 0, 2)
    octahedron(1, 1, 5)
    octahedron(1, 1, -5)
    octahedron(1, -1, 5)
    octahedron(1, -1, -5)
    octahedron(-1, 1, 5)
    octahedron(-1, 1, -5)
    octahedron(-1, -1, 5)
    octahedron(-1, -1, -5)
    octahedron(1, 1, 7)
    octahedron(1, 1, -7)
    octahedron(1, -1, 7)
    octahedron(1, -1, -7)
    octahedron(-1, 1, 7)
    octahedron(-1, 1, -7)
    octahedron(-1, -1, 7)
    octahedron(-1, -1, -7)

    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.7, 2.7)
    ax.set_zlim(-4.6, 4.6)
    ax.view_init(elev=7, azim=20)
    plt.axis('off')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=200,
                    bbox_inches="tight")


def fig19(print_fig=True):
    """figure 19

    %%%%%%%%%%%%%%%%%%%%
    Infinity-layer model
    %%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig19'

    fig = plt.figure(figname, figsize=(5, 8), clear=True)

    ax = fig.add_axes([.1, .1, .8, .8], projection='3d')
    ax.tick_params(**kwargs_ticks)

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    X0 = .25 * np.outer(np.cos(u), np.sin(v))
    Y0 = .25 * np.outer(np.sin(u), np.sin(v))
    Z0 = .25 * np.outer(np.ones(np.size(u)), np.cos(v))
    X = .15 * np.outer(np.cos(u), np.sin(v))
    Y = .15 * np.outer(np.sin(u), np.sin(v))
    Z = .15 * np.outer(np.ones(np.size(u)), np.cos(v))
    Xs = .3 * np.outer(np.cos(u), np.sin(v))
    Ys = .3 * np.outer(np.sin(u), np.sin(v))
    Zs = .3 * np.outer(np.ones(np.size(u)), np.cos(v))

    def cc(arg):
        return mcolors.to_rgba(arg, alpha=.75)

    def triang(x0, y0, z0, x, y, z):
        X = [x0+x, 0+x, 0+x]
        Y = [0+y, 0+y, y0+y]
        Z = [0+z, z0+z, 0+z]
        verts = [list(zip(X, Y, Z))]
        return verts

    def octahedron(x, y, z):
        v1 = triang(-1, 1, 1, x, y, z)
        v2 = triang(-1, -1, 1, x, y, z)
        v3 = triang(-1, -1, -1, x, y, z)
        v4 = triang(-1, 1, -1, x, y, z)
        v5 = triang(1, 1, 1, x, y, z)
        v6 = triang(1, -1, 1, x, y, z)
        v7 = triang(1, -1, -1, x, y, z)
        v8 = triang(1, 1, -1, x, y, z)
        V = [v1, v2, v3, v4, v5, v6, v7, v8]
        for i in range(8):
            ax.add_collection3d(Poly3DCollection(V[i], facecolors=cc('w'),
                                                 edgecolor=cc('k')), zs='z')

        ax.plot_surface(X0 + x, Y0 + y, Z0 + z,  rstride=4,
                        cstride=4, color='r', lw=0)
        ax.plot_surface(X + x, Y + y, Z + z + 1,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y, Z + z - 1,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y + 1, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x, Y + y - 1, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x + 1, Y + y, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)
        ax.plot_surface(X + x - 1, Y + y, Z + z,  rstride=4,
                        cstride=4, color='b', lw=0)

    ax.plot_surface(Xs, Ys, Zs, rstride=4,
                    cstride=4, color='c', lw=0)

    octahedron(1, 1, 1)
    octahedron(1, 1, -1)
    octahedron(1, -1, 1)
    octahedron(1, -1, -1)
    octahedron(-1, 1, 1)
    octahedron(-1, 1, -1)
    octahedron(-1, -1, 1)
    octahedron(-1, -1, -1)

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_zlim(-2.65, 2.65)
    ax.view_init(elev=7, azim=20)
    plt.axis('off')
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.png', dpi=200,
                    bbox_inches="tight")


def fig20(print_fig=True):
    """figure 20

    %%%%%%%%%%%%%%%%%%%%%%%
    Instrumental resolution
    %%%%%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig20'

    mat = 'CSRO20'
    year = '2017'
    sample = 'S6'
    # gold = '62091'
    gold = '62158'
    D = ARPES.DLS(gold, mat, year, sample)

    D.norm(gold=gold)
    D.norm_shift()

    # create figure
    fig = plt.figure(figname, figsize=(10, 10), clear=True)
    ax1 = fig.add_subplot(221)
    ax1.set_position([.41, .4, .25, .25])
    ax1.tick_params(**kwargs_ticks)
    ax2 = fig.add_subplot(222)
    ax2.set_position([.7, .4, .25, .25])
    ax2.tick_params(**kwargs_ticks)

    # plot panel (a)
    c0 = ax1.contourf(D.ang_shift, D.en_shift, D.int_shift, 100, **kwargs_ex,
                      zorder=.1)
    ax1.set_rasterization_zorder(.2)
    ax1.plot([D.ang[0], D.ang[-1]], [0, 0], **kwargs_ef)

    # decorate panel (a)
    ax1.set_ylabel(r'$\omega$ (eV)', fontdict=font)
    ax1.set_xlabel(r'Detector angles', fontdict=font)
    ax1.text(-15, 0.05, '(b)', fontdict=font)

    # colorbar
    pos = ax1.get_position()
    cax = plt.axes([pos.x0, pos.y0+pos.height+.01,
                    pos.width, .01])
    cbar = plt.colorbar(c0, cax=cax, ticks=None, orientation='horizontal')
    cbar.set_ticks([])

    # initial fit parameters
    Ef_ini = 0
    T_ini = 6  # measured temperature
    width = .007
    slope = -.02
    mx = 0.011

    # other parameters
    ch = 300  # channel
    xx = np.linspace(-0.2, 0.2, 1000)  # used for potting
    kB = 8.6173303e-5  # Boltzmann constant

    int_sum = np.sum(D.int_shift, 0) / D.ang.size  # average EDCs
#    ax2.plot(D.en_shift, D.int_shift, 'C0o', ms=2)  # plot all EDCs

    # reduce dataset for fit
    en = D.en_shift[ch, :]
    mx_val, mx_idx = utils.find(en, 0.02)
    mn_val, mn_idx = utils.find(en, -0.06)

    en = en[mn_idx:mx_idx]
    int_sum = int_sum[mn_idx:mx_idx]

    # plot averaged EDC
    ax2.plot(en, int_sum, 'bo', ms=5)

    # initial guess FD
    p_ini_FD = np.array([T_ini*kB, Ef_ini, mx,
                         np.min(int_sum), slope])

    # boundaries FD
    eps = 1e-9
    bnd_bot_FD = np.concatenate((p_ini_FD[:1] - eps,
                                 p_ini_FD[1:3] - np.inf,
                                 p_ini_FD[3:4] - eps,
                                 p_ini_FD[4:] - np.inf))
    bnd_top_FD = np.concatenate((p_ini_FD[:1] + eps,
                                 p_ini_FD[1:3] + np.inf,
                                 p_ini_FD[3:4] + eps,
                                 p_ini_FD[4:] + np.inf))
    bnd_FD = (bnd_bot_FD, bnd_top_FD)

    # fit FD
    p_FD, c_FD = curve_fit(utils.FDsl, en,
                           int_sum, p_ini_FD, bounds=bnd_FD)

    # initial guess FDG
    p_ini_FDG = np.array([T_ini*kB, p_FD[1], p_FD[2], width,
                          np.min(int_sum), 1, 0])

    # boundaries FDG
    bnd_bot_FDG = np.concatenate((p_ini_FDG[:1] - eps,
                                 p_ini_FDG[1:4] - np.inf,
                                 p_ini_FDG[4:] - np.inf))
    bnd_top_FDG = np.concatenate((p_ini_FDG[:1] + eps,
                                 p_ini_FDG[1:4] + np.inf,
                                 p_ini_FDG[4:] + np.inf))
    bnd_FDG = (bnd_bot_FDG, bnd_top_FDG)

    # fit FDG
    p_FDG, c_FDG = curve_fit(utils.FDconvGauss, en,
                             int_sum, p_ini_FDG, bounds=bnd_FDG)
    FWHM = p_FDG[3]
    err_FDG = np.sqrt(np.diag(c_FDG))
    err_FWHM = err_FDG[3] / 2
    print(err_FWHM)
    sig = FWHM/(2*np.sqrt(2*np.log(2)))

    # plot data
    ax2.plot(xx, utils.FDsl(xx, *p_FD), 'C1-')
    ax2.plot(xx, utils.gauss(xx, p_FDG[1], sig, np.max(int_sum), 0, 0, 0),
             'k-')
    ax2.plot(xx, utils.FDconvGauss(xx, *p_FDG), 'r-', lw=2)

#    ax2.text(-.035, .002, 'All EDCs', color='C0')
    ax2.text(-.035, .002, 'Averaged EDC',
             color='b', fontsize=12)
    ax2.text(-.035, .0016, r'$\widetilde{f}(\omega, T)$',
             color='C1', fontsize=12)
    ax2.text(-.035, .0012, r'$\mathcal{R}(\Delta \omega)$',
             color='k', fontsize=12)
    ax2.text(-.035, .0008,
             r'$\mathcal{R}(\Delta \omega) \otimes \widetilde{f}(\omega, T)$',
             color='r', fontsize=12)

    # decorate axes
    ax2.text(-.038, 0.00415, '(c)', fontdict=font)
    ax2.set_xlim(-.04, .02)
    ax2.set_ylim(0, 1.1*np.max(int_sum))
    ax2.set_yticks([])
    ax2.set_xlabel(r'$\omega$ (eV)', fontdict=font)
    ax2.set_ylabel('Intensity (arb.u.)', fontdict=font)

    # panel a)
    mat = 'EuLSCO21'
    year = '2015'
    sample = 'Eu21_1'
    files = np.array([25700, 25703, 25707, 25711, 25714, 25717])
    T = np.array([6.3, 8, 10.15, 12.1, 14.2, 16.2])
    T_fit = np.zeros(len(T))
    T_fit_err = np.zeros(len(T))

    n = 0
    for file in files:
        D = ARPES.DLS(file, mat, year, sample)
        D.gold(50.52)
        T_fit[n] = np.mean(D.T)
        T_fit_err[n] = np.std(D.T)
        n += 1

    kB = 8.617e-5  # Boltzmann constant

    en = 4*T_fit*kB*1e3
    en_err = 4*T_fit_err*kB*1e3/2
    print(en_err)
    ax3 = fig.add_subplot(223)
    ax3.set_position([.08, .4, .25, .25])
    ax3.tick_params(**kwargs_ticks)
    ax3.errorbar(T, en, yerr=en_err, lw=.5,
                 capsize=2, color='k', fmt='o', ms=5)
    p_ini_poly1 = [0, 0, 0]
    p_poly1, c_poly1 = curve_fit(utils.poly_1, T, en, p0=p_ini_poly1)
#    err_fit = np.sqrt(np.diag(c_poly1))

    xx = np.linspace(0, 20, 200)
    yy = utils.poly_1(xx, *p_poly1)

    ax3.plot(xx, yy, 'r--')
    ax3.plot([0, 5], [p_poly1[0], p_poly1[0]], **kwargs_ef)
    ax3.arrow(2, 4, 0, 4.2, head_width=0.4, head_length=0.5, fc='k', ec='k')
    ax3.arrow(2, 4, 0, -3.4, head_width=0.4, head_length=0.5, fc='k', ec='k')
    ax3.text(2.4, 5, 'Instrumental resolution')
    ax3.text(2.4, 3.5, (r'$\Delta \omega = $' +
                        str(np.round(p_poly1[0], 1)) +
                        r'$\,$meV'))
    ax3.text(.5, 13.9, '(a)', fontdict=font)
    ax3.set_xticks(np.arange(0, 20, 5))
    ax3.set_yticks(np.arange(0, 20, 5))
    ax3.set_xlim(0, 18)
    ax3.set_ylim(0, 15)
    ax3.set_xlabel(r'$T_\mathrm{sample}$ (K)')
    ax3.set_ylabel(r'$4\,k_\mathrm{B}\,T_\mathrm{fit}$ (meV)')
    ax3.grid(True, alpha=.2)

    plt.show()

    # Save figure
    if print_fig:
        fig.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig21(print_fig=True):
    """figure 21

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Instrumental resolution vs T
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    figname = 'CONfig21'

    mat = 'EuLSCO21'
    year = '2015'
    sample = 'Eu21_1'
    files = np.array([25700, 25703, 25707, 25711, 25714, 25717])
    T = np.array([6.3, 8, 10.15, 12.1, 14.2, 16.2])
    T_fit = np.zeros(len(T))
    T_fit_err = np.zeros(len(T))

    n = 0
    for file in files:
        D = ARPES.DLS(file, mat, year, sample)
        D.gold(50.52)
        T_fit[n] = np.mean(D.T)
        T_fit_err[n] = np.std(D.T)
        n += 1

    kB = 8.617e-5  # Boltzmann constant

    fig = plt.figure(figname, figsize=(6, 6), clear=True)
    ax1 = fig.add_subplot(131)
    ax1.set_position([.3, .3, .4, .4])
    ax1.tick_params(**kwargs_ticks)

    en = 4*T_fit*kB*1e3
    en_err = 4*T_fit_err*kB*1e3/2
    print(en_err)
    ax1.errorbar(T, en, yerr=en_err, lw=.5,
                 capsize=2, color='k', fmt='o', ms=5)
    p_ini_poly1 = [0, 0, 0]
    p_poly1, c_poly1 = curve_fit(utils.poly_1, T, en, p0=p_ini_poly1)
#    err_fit = np.sqrt(np.diag(c_poly1))

    xx = np.linspace(0, 20, 200)
    yy = utils.poly_1(xx, *p_poly1)

    ax1.plot(xx, yy, 'r--')
    ax1.plot([0, 5], [p_poly1[0], p_poly1[0]], **kwargs_ef)
    ax1.arrow(2, 4, 0, 4.2, head_width=0.4, head_length=0.5, fc='k', ec='k')
    ax1.arrow(2, 4, 0, -3.4, head_width=0.4, head_length=0.5, fc='k', ec='k')
    ax1.text(2.4, 5, 'Instrumental resolution')
    ax1.text(2.4, 3.5, (r'$\Delta \omega = $' +
                        str(np.round(p_poly1[0], 1)) +
                        r'$\,$meV'))
    ax1.set_xticks(np.arange(0, 20, 5))
    ax1.set_yticks(np.arange(0, 20, 5))
    ax1.set_xlim(0, 18)
    ax1.set_ylim(0, 15)
    ax1.set_xlabel(r'$T_\mathrm{sample}$ (K)')
    ax1.set_ylabel(r'$4\,k_\mathrm{B}\,T_\mathrm{fit}$ (meV)')
    ax1.grid(True, alpha=.2)
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)


def fig22(print_fig=True):
    """figure 22

    %%%%%%%%%%%%
    Tc over time
    %%%%%%%%%%%%
    """

    figname = 'CONfig22'

    os.chdir(data_dir)
    Tc1 = np.genfromtxt('Tc1.csv', delimiter=',')
    Tc2 = np.genfromtxt('Tc2.csv', delimiter=',')
    Tc3 = np.genfromtxt('Tc3.csv', delimiter=',')
    BCS1 = np.arange(0, 6, 1)
    BCS2 = np.arange(0, 4, 1)
    HF1 = np.arange(7, 8, 1)
    HF2 = np.arange(4, 10, 1)
    C = np.arange(10, 13, 1)
    Full = np.arange(13, 16, 1)
    Fe1 = np.arange(16, 18, 1)
    Fe2 = np.arange(1, 3, 1)
    Cu1 = np.arange(19, 21, 1)
    Cu2 = np.arange(3, 9, 1)

    t1 = Tc1[:, 0]
    T1 = Tc1[:, 1]
    t2 = Tc2[:, 0]
    T2 = Tc2[:, 1]
    t3 = Tc3[:, 0]
    T3 = Tc3[:, 1]

    fig = plt.figure(figname, figsize=(8, 8), clear=True)

    ax = fig.add_axes([.2, .2, .6, .6])
    ax.tick_params(**kwargs_ticks)
    axi = fig.add_axes([.27, .42, .32, .32])
    axi.tick_params(**kwargs_ticks)

    x_i = 1975
    x_f = 2016
    y_i = 0
    y_f = 50

    ax.plot([x_i, x_f], [y_i, y_i], 'k--')
    ax.plot([x_i, x_f], [y_f, y_f], 'k--')
    ax.plot([x_i, x_i], [y_i, y_f], 'k--')
    ax.plot([x_f, x_f], [y_i, y_f], 'k--')

#    ax.arrow(1978, 60, -2, 35, head_width=1.5, head_length=6, fc='k', ec='k')
    ax.annotate("", xytext=(1995, 55), xy=(1974, 105),
                arrowprops=dict(arrowstyle="->"))
    ax.plot([1900, 2020], [293.15, 293.15], **kwargs_ef)
    ax.plot([1900, 2020], [77, 77], **kwargs_ef)
    ax.plot([1900, 2020], [4, 4], **kwargs_ef)
    axi.plot([1986, 1986], [6, 29], '--', color='steelblue')
    axi.plot([1986, 1986], [40, 50], '--', color='steelblue')

    ax.plot(t1[BCS1], T1[BCS1], 'o', color='darkgreen')
    ax.plot(t2[BCS2], T2[BCS2], 'o', color='darkgreen')
    ax.plot(t3[0], T3[0], 'o', color='darkgreen')
    ax.plot(t1[HF1], T1[HF1], '*', color='c')
    ax.plot(t2[HF2], T2[HF2], '*', color='c')
    ax.plot(t2[C], T2[C], 'd', color='m')
    ax.plot(t2[Full], T2[Full], 'd', color='b')
    ax.plot(t2[Fe1], T2[Fe1], 's', color='C1')
    ax.plot(t3[Fe2], T3[Fe2], 's', color='C1')
    ax.plot(t2[Cu1], T2[Cu1], 'o', color='r')
    ax.plot(t3[Cu2], T3[Cu2], 'o', color='r')
    ax.plot(2018, 260, 'o', color='darkgreen')

    axi.plot(t2[BCS2], T2[BCS2], 'o', color='darkgreen')
    axi.plot(t1[HF1], T1[HF1], '*', color='c')
    axi.plot(t2[HF2], T2[HF2], '*', color='c')
    axi.plot(t2[C], T2[C], 'd', color='m')
    axi.plot(t2[Full], T2[Full], 'd', color='b')
    axi.plot(t2[Fe1], T2[Fe1], 's', color='C1')
    axi.plot(t3[Fe2], T3[Fe2], 's', color='C1')
    axi.plot(t2[Cu1], T2[Cu1], 'o', color='r')
    axi.plot(t3[Cu2], T3[Cu2], 'o', color='r')

    ax.text(1960, 283, r'$0^\circ$C', fontdict=font)
    ax.text(1960, 80, r'L$\,$N$_2$', fontdict=font)
    ax.text(1960, 7, r'L$\,^4$He', fontdict=font)
    axi.text(1983, 35, 'Discovery HTSC 1986', rotation=90, color='steelblue')

    ax.text(1908, 10, r'Hg', fontsize=8)
    ax.text(1913, 12, r'Pb', fontsize=8)
    ax.text(1931, 14, r'Nb', fontsize=8)
    ax.text(1939, 22, r'NbN', fontsize=8)
    ax.text(1948, 7, r'V$_3$Si', fontsize=8)
    ax.text(1950, 25, r'Nb$_3$Ge', fontsize=8)

    ax.text(1990, 106, r'YBaCuO', fontsize=8)
    ax.text(1985, 124, r'BiSrCaCuO', fontsize=8)
    ax.text(1981, 153, r'TlBaCaCuO', fontsize=8, rotation=45)
    ax.text(1993, 137, r'HgBaCaCuO', fontsize=8)
    ax.text(1983, 176, r'HgBaCaCuO @$30\,$GPa', fontsize=8)
    ax.text(1997, 147, r'HgTlBaCaCuO', fontsize=8)

    ax.text(2005, 70, r'SrFFeAs', fontsize=8)
    ax.text(2013, 105, r'FeSe', fontsize=8)

    ax.text(2005, 223, r'H$_2$S @$155\,$GPa', fontsize=8, rotation=45)
    ax.text(2002, 255, r'LaH$_{10}$ @$190\,$GPa', fontsize=8, rotation=45)

    axi.text(1976, 7.5, r'CeCu$_2$Si$_2$', rotation=45, fontsize=8)
    axi.text(1981, 5, r'UBe$_{13}$', rotation=45, fontsize=8)
    axi.text(1984.5, 4, r'UPt$_3$', rotation=45, fontsize=8)
    axi.text(1990, 8, r'UPd$_2$Al$_3$', rotation=45, fontsize=8)
    axi.text(1997, 5, r'CeCoIn$_5$', rotation=45, fontsize=8)
    axi.text(1999, 12, r'PuRhGa$_5$', rotation=45, fontsize=8)
    axi.text(1998.5, 23, r'PuCoGa$_5$', rotation=45, fontsize=8)

    axi.text(2002, .5, r'CNT', rotation=0, fontsize=8)
    axi.text(2005, 5.5, r'diamond', rotation=0, fontsize=8)
    axi.text(2007, 12, r'CNT', rotation=0, fontsize=8)

    axi.text(1989, 21, r'K$_3$C$_{60}$', rotation=0, fontsize=8)
    axi.text(1992.5, 33, r'RbCsC$_{60}$', rotation=0, fontsize=8)
    axi.text(1991, 43.5, r'Cs$_3$C$_{60}$ @$1.4\,$GPa', rotation=0, fontsize=8)

    axi.text(2007, 2.5, r'LaOFeP', rotation=0, fontsize=8)
    axi.text(2005, 26.5, r'LaOFFeAs', rotation=0, fontsize=8)

    axi.text(1986, 37.5, r'LaSrCuO', rotation=45, fontsize=8)
    axi.text(1985, 42.5, r'LaBaCuO', rotation=45, fontsize=8)

    axi.text(1989.5, 29.5, r'BKBO', rotation=0, fontsize=8)
    axi.text(1991, 25, r'YbPd$_2$B$_2$C', rotation=0, fontsize=8)
    axi.text(2003.5, 16, r'Li @$33\,$GPa', rotation=0, fontsize=8)
    axi.text(2002.5, 40.5, r'MgB$_2$', rotation=0, fontsize=8)

    ax.text(1981, 262, 'BCS', color='darkgreen', fontsize=12)
    ax.text(1981, 250, 'Heavy Fermions', color='c', fontsize=12)
    ax.text(1981, 238, 'Fullerene', color='b', fontsize=12)
    ax.text(1981, 226, 'Diamond', color='m', fontsize=12)
    ax.text(1981, 214, 'Cuprates', color='r', fontsize=12)
    ax.text(1981, 202, 'Iron-based', color='C1', fontsize=12)
    ax.set_xticks([1900, 1920, 1940, 1960, 1980, 2000, 2018])
    ax.set_ylim(0, 300)
    ax.set_xlim(1900, 2020)
    ax.set_xlabel('Year', fontdict=font)
    ax.set_ylabel('$T_c$ (K)', fontdict=font)
    axi.set_xlim(x_i, x_f)
    axi.set_ylim(y_i, y_f)
    plt.show()

    # Save figure
    if print_fig:
        plt.savefig(save_dir + figname + '.pdf', dpi=100,
                    bbox_inches="tight", rasterized=True)
