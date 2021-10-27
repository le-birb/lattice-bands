
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
pi_x_kx = np.linspace(0, b[0]/2, num = resolution)
pi_x_ky = np.zeros(resolution)

x_m_kx  = np.zeros(resolution) + b[0]/2
x_m_ky  = np.linspace(0, b[1]/2, num = resolution)

m_pi_kx = np.linspace(b[0]/2, 0, num = resolution)
m_pi_ky = np.linspace(b[1]/2, 0, num = resolution)


pi_x_plot_range = np.linspace(0, 2)
x_m_plot_range  = np.linspace(2, 4)
m_pi_plot_range = np.linspace(4, 6)


fig = p.figure()
ax  = fig.add_subplot()

# add lines to separate the paths and make reading the plot easier
for point in [0, 2, 4, 6]:
    p.axvline(point, linestyle = "--", color = (0, 0, 0, .5))

# define the g offsets to iterate over
g_x = range(-g_range, g_range + 1)
g_y = range(-g_range, g_range + 1)

g_offsets = product(g_x, g_y)

for offset in g_offsets:
    pi_x_energies = energy(pi_x_kx + offset[0]*b[0], pi_x_ky + offset[1]*b[1])
    x_m_energies = energy(x_m_kx + offset[0]*b[0], x_m_ky + offset[1]*b[1])
    m_pi_energies = energy(m_pi_kx + offset[0]*b[0], m_pi_ky + offset[1]*b[1])

    ax.plot(pi_x_plot_range, pi_x_energies)
    ax.plot(x_m_plot_range, x_m_energies)
    ax.plot(m_pi_plot_range, m_pi_energies)

ax.set_xlabel("High Symmetry Points")
ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
ax.set_xticklabels([r"$\Pi$", r"$\Delta$", r"X", r"Z", r"M", r"$\Sigma$"])
ax.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")
p.show()