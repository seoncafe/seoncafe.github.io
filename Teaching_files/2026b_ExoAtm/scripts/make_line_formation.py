"""Toy model of thermal line formation (Seager 2010, Sec. 6.3): figs/line_formation.pdf.

A plane-parallel LTE atmosphere without scattering, gridded in pressure.
The continuum optical depth is tau_c = p / p0 and an absorption line adds
a Gaussian opacity profile, tau_nu = tau_c [1 + A exp(-x^2)], where x is
the frequency offset from line center in Doppler widths. The emergent flux
is F = 2 pi int B(T(tau_nu)) E_2(tau_nu) d tau_nu, and it is shown as a
brightness temperature, F = pi B(T_b), at 15 micron. Three temperature
profiles: decreasing outward, isothermal, and a temperature inversion.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expn

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 14

h, c, k = 6.626e-34, 2.998e8, 1.381e-23
lam = 15e-6


def planck(T):
    return 2 * h * c**2 / lam**5 / np.expm1(h * c / (lam * k * T))


def tbright(B):
    return h * c / (lam * k) / np.log1p(2 * h * c**2 / (lam**5 * B))


p = np.logspace(-6, 2, 4000)        # bar
p0 = 1.0                            # continuum tau = 1 at 1 bar
logp = np.log10(p)
profiles = {
    'decreasing outward': 200 + 100 * (logp + 6) / 8,
    'isothermal': np.full_like(p, 250.0),
    'inversion': 300 - 100 * (logp + 6) / 8,
}
colors = {'decreasing outward': 'tab:blue', 'isothermal': 'tab:gray', 'inversion': 'tab:red'}

x = np.linspace(-4, 4, 161)
A = 1e4
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={'width_ratios': [1, 1.35]})
for name, T in profiles.items():
    B = planck(T)
    tb = []
    for xx in x:
        # prepend the top of the atmosphere (tau = 0) at the uppermost temperature
        tau = np.concatenate([[0.0], p / p0 * (1 + A * np.exp(-xx**2))])
        BB = np.concatenate([[B[0]], B])
        F = 2 * np.pi * np.trapezoid(BB * expn(2, tau), tau)
        tb.append(tbright(F / np.pi))
    ax1.plot(T, p, color=colors[name], lw=2, label=name)
    ax2.plot(x, tb, color=colors[name], lw=2, label=name)

# pressures where tau = 2/3 in the continuum and at line center
for pp, lab in [(2 / 3 * p0, r'continuum $\tau=2/3$'),
                (2 / 3 * p0 / (1 + A), r'line core $\tau=2/3$')]:
    ax1.axhline(pp, color='k', ls=':', lw=1)
    ax1.text(308, pp, lab, va='bottom', ha='right', fontsize=11,
             bbox=dict(facecolor='white', edgecolor='none', pad=1))
ax1.set_yscale('log')
ax1.invert_yaxis()
ax1.set_xlim(190, 310)
ax1.set_xlabel(r'Temperature (K)')
ax1.set_ylabel(r'Pressure (bar)')
ax1.set_title(r'(a) temperature profiles', fontsize=14)

ax2.set_xlabel(r'Frequency offset from line center $x$ (Doppler widths)')
ax2.set_ylabel(r'Brightness temperature $T_{\rm b}$ (K)')
ax2.set_title(r'(b) emergent spectrum at $15\,\mu$m', fontsize=14)
ax2.legend(loc='upper right', fontsize=11, frameon=False)
ax2.set_ylim(190, 310)
fig.tight_layout()
fig.savefig('figs/line_formation.pdf')
print('wrote figs/line_formation.pdf')
