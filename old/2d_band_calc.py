
import numpy as np
import matplotlib.pyplot as p

from math import pi
from itertools import product

# this script will make a band plot for a 2-dimensional square lattice

def energy(kx: float, ky: float) -> float:
    return kx**2 + ky**2

g_range = 1
# a and b represent the physical and reciprocal basis vectors
# for more complex lattices, a better strategy should be found
a: np.array = np.array((1, 1))
b: np.array = 2*pi/a

# how many points to sample along each path
resolution = 50


# the paths along which the bands are plotted
# each path is split into a separate list of x and y coordinates
# so that they can be passed as arrays into the energy() function
# with no extra fuss
gamma_x_kx = np.linspace(0, b[0]/2, num = resolution)
gamma_x_ky = np.zeros(resolution)

x_m_kx  = np.zeros(resolution) + b[0]/2
x_m_ky  = np.linspace(0, b[1]/2, num = resolution)

m_gamma_kx = np.linspace(b[0]/2, 0, num = resolution)
m_gamma_ky = np.linspace(b[1]/2, 0, num = resolution)


gamma_x_plot_range = np.linspace(0, 2)
x_m_plot_range  = np.linspace(2, 4)
m_gamma_plot_range = np.linspace(4, 6)


fig = p.figure()
ax  = fig.add_subplot()

# add lines to separate the paths and make reading the plot easier
for point in [0, 2, 4, 6]:
    p.axvline(point, linestyle = "--", color = (0, 0, 0, .5))

# define the g offsets to iterate over
g_x = range(-g_range, g_range + 1)
g_y = range(-g_range, g_range + 1)

g_offsets = product(g_x, g_y)


# TODO: make sure there's a handler for if this ever runs out
# if that situation is hit, come up with a better solution
degeneracy_colors = ["black", "red", "blue", "green", "purple"]

seen_gamma_x_endpoints: set = set()
seen_x_m_endpoints: set = set()
seen_m_gamma_endpoints: set = set()

for offset in g_offsets:
    gamma_color_idx = 0
    x_color_idx = 0
    m_color_idx = 0

    gamma_x_energies = energy(gamma_x_kx + offset[0]*b[0], gamma_x_ky + offset[1]*b[1])
    x_m_energies = energy(x_m_kx + offset[0]*b[0], x_m_ky + offset[1]*b[1])
    m_gamma_energies = energy(m_gamma_kx + offset[0]*b[0], m_gamma_ky + offset[1]*b[1])

    # check endpoints for degeneracy
    gamma_x_endpoints = (gamma_x_energies[0], gamma_x_energies[-1])
    x_m_endpoints = (x_m_energies[0], x_m_energies[-1])
    m_gamma_endpoints = (m_gamma_energies[0], m_gamma_energies[-1])

    if gamma_x_endpoints in seen_gamma_x_endpoints:
        gamma_color_idx += 1
    else:
        seen_gamma_x_endpoints.add(gamma_x_endpoints)

    if x_m_endpoints in seen_x_m_endpoints:
        x_color_idx += 1
    else:
        seen_x_m_endpoints.add(x_m_endpoints)

    if m_gamma_endpoints in seen_m_gamma_endpoints:
        m_color_idx += 1
    else:
        seen_m_gamma_endpoints.add(m_gamma_endpoints)

    ax.plot(gamma_x_plot_range, gamma_x_energies, color = degeneracy_colors[gamma_color_idx])
    ax.plot(x_m_plot_range, x_m_energies, color = degeneracy_colors[x_color_idx])
    ax.plot(m_gamma_plot_range, m_gamma_energies, color = degeneracy_colors[m_color_idx])

ax.set_xlabel("High Symmetry Points")
ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
ax.set_xticklabels([r"$\Gamma$", r"$\Delta$", r"X", r"Z", r"M", r"$\Sigma$", r"$\Gamma$"])
ax.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")
p.show()