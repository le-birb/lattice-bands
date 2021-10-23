
import numpy as np
import matplotlib.pyplot as p

from math import pi

# a free electron's energy is equal to hb^2/(2m) * k^2, but I'm starting with just k^2 for simplicity
def energy(k: float) -> float:
    return k**2

# this'll be how many "G"s out to plot; won't work well for 2d or 3d but we'll cross those bridges when we get to them
n: int = 2

# our direct lattice spacing (starting easy, as normal)
a: float = 1

# reciprocal lattice spacing
b: float = 2*pi/a


fig = p.figure()
ax  = fig.add_subplot()

# m controls the G we're looking at, with G = mb
# we take values from -n to n inclusive (n+1 is excluded by range())
for m in range(-n, n+1):
    # everything is mapped back into a Brillouin zone,
    # which in 1d is an interval of width b centerd on 0
    # so our "x values" (k values) are all in this interval
    ks = np.linspace(-b/2, b/2, num = 50)
    energies = []
    
    for k in ks:
        # the energies are taken from the "true" position k + G
        energies.append(energy(k + m*b))

    ax.plot(ks, energies)

ax.set_xlabel("k")
ax.set_xticks([-np.pi, 0, np.pi])
ax.set_xticklabels([r"$-\frac{π}{a}$", "0", r"$\frac{π}{a}$"])
ax.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")
p.show()
