
from __future__ import annotations
import functools
from itertools import chain

import tkinter as tk
from tkinter import ttk
import os
from typing import Callable

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib

import numpy as np

from json_interface import load_lattice
import central_equation

import potentials
from density import plot_densities

# tell matplotlib to use TkAgg so we can show plots on tkinter windows
matplotlib.use("TkAgg")


#####################################################################################################
# set up whole window

root = tk.Tk()
root.title("Lattice Bands")

mainframe = ttk.Frame(root, padding = "12")
mainframe.grid(column = 0, row = 0, sticky = "NESW")
root.columnconfigure(0, weight = 2)
# root.columnconfigure(1, weight = 1)
root.rowconfigure(0, weight = 1)

interfaceframe = ttk.Frame(mainframe, padding = 10)
interfaceframe.grid(column = 1, row = 0, sticky = "NESW")
# interfaceframe.rowconfigure(0, weight = 1)
# interfaceframe.rowconfigure(1, weight = 1)
interfaceframe.rowconfigure(2, weight = 2)



#####################################################################################################
# lattice selector

lattice_label = ttk.Label(interfaceframe, text = "Select lattice to use:")
lattice_label.grid(column = 0, row = 0, sticky = "S")

files: list[str] = os.listdir("lattices")
json_files = []

# TODO: add a name field to the json and load from that?
for filename in files:
    if filename.endswith(".json"):
        json_files.append(filename[:-5])

lattice = tk.StringVar()
lattice.set("2d_square")
file_menu = ttk.OptionMenu(interfaceframe, lattice, lattice.get(), *json_files)
file_menu.grid(column = 0, row = 1, sticky = "N")




#####################################################################################################
# define number entry boxes

def _validate_num(text: str):
    return text.isdigit() or text == ""

class IntString(tk.StringVar):
    """
    Wrapper for tk.StringVar for use with num_entry.
    Allows entry as a string but ensures and integer value.
    """
    def __init__(self, *args, default: int = 0, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = default

    def get(self) -> int:
        tempval = super().get()
        if tempval == "":
            return self._default
        else:
            return int(tempval)

class num_entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validator = self.register(_validate_num)
        # this is the incantaion I found to make text validation work
        self.config(validate = "key", validatecommand = (validator, '%P'))


#####################################################################################################
# potential selector

potential_frame = ttk.Frame(interfaceframe)
potential_frame.grid(column = 0, row = 2, sticky = "N")

potentials_to_plot = []

def add_potential():
    new_pot = potential_entry(potential_frame)
    new_pot.pack()
    potentials_to_plot.append(new_pot)

add_potential_buton = ttk.Button(potential_frame, text = "Add potential to plot", command = add_potential)
add_potential_buton.pack(anchor = "n")

potential_map = \
{
    "Empty": potentials.empty_v,
    "Simple": potentials.simple_v,
    "Quadratic": potentials.typical_v,
}
_max_width = max(len(k) for k in potential_map.keys())

class potential_entry(ttk.Frame):
    """GUI element for displaying and editing parameters of 
    potenitals being plotted, as well as plotting styles.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.potential_name = tk.StringVar(value = "Empty")
        self.potential_selector = ttk.Combobox(self, textvariable = self.potential_name, state = "readonly", values = list(potential_map.keys()), width = _max_width)
        self.potential_selector.current(0)
        self.potential_selector.grid(row =0, column = 0)

        self.scale_label = ttk.Label(self, text = "Strength:")
        self.scale_label.grid(row = 0, column = 1, sticky = "E", padx = (5, 0))

        self.scale_var = IntString(value = "1", default = 1)
        self.scale_entry = num_entry(self, textvariable = self.scale_var, width = 4)
        self.scale_entry.grid(row = 0, column = 2, sticky = "W", padx = (0, 5))

        self.del_btn = ttk.Button(self, command = self.remove, text = "Remove", width = 8)
        self.del_btn.grid(row = 0, column = 5, sticky = "E")

    def get_potential(self):
        return functools.partial(potential_map[self.potential_name.get()], scale = self.scale_var.get())

    def remove(self):
        self.pack_forget()
        potentials_to_plot.remove(self)

#####################################################################################################
# plot parameters - resolution and range

range_label = ttk.Label(interfaceframe, text = "Nearest neigbors to visit:")
range_label.grid(column = 0, row = 7)

range_var = IntString(value = "1", default = 1)
range_entry = num_entry(interfaceframe, textvariable = range_var)
range_entry.grid(column = 0, row = 8)

resolution_label = ttk.Label(interfaceframe, text = "Resolution of plot (higher is better but slower):", wraplength = 150)
resolution_label.grid(column = 0, row = 9)

resolution_var = IntString(value = "50", default = 50)
resolution_entry = num_entry(interfaceframe, textvariable = resolution_var)
resolution_entry.grid(column = 0, row = 10)



#####################################################################################################
# add density of states checkbox
# TODO: decide whether or not to even use this

# density_label = ttk.Label(interfaceframe, text = "Make density of states diagram (doesn't work yet):", wraplength = 150)
# density_label.grid(column = 0, row = 14)

# make_density_plot = tk.BooleanVar(value = False)
# density_plot_checkbox = ttk.Checkbutton(interfaceframe, variable = make_density_plot)
# density_plot_checkbox.grid(column = 0, row = 15)



#####################################################################################################
# setting up the go button and plotting function
# TODO: move some of these algorithm details to their own function or maybe even module

def plot_bands():
    band_axes.clear()
    density_axes.clear()

    lattice_filepath = f"lattices/{lattice.get()}.json"
    lat = load_lattice(lattice_filepath)

    for point in lat.vertical_lines:
        band_axes.axvline(point, linestyle = "--", color = (.5, .5, .5, .5))

    reciprocal_range = range_var.get()
    resolution = resolution_var.get()

    band_paths = lat.get_paths(resolution)
    plot_ranges = []
    for i in range(len(band_paths)):
        plot_ranges.append(np.linspace(i, i+1, resolution))
    
    path = np.array(list(chain.from_iterable(band_paths)))
    plot_space = np.array(list(chain.from_iterable(plot_ranges)))

    band_count = (2*reciprocal_range + 1)**2

    V = functools.partial(potentials.typical_v, scale = 2)

    # TODO: allow selecting the potential to use
    energy_bands = central_equation.get_bands(path, V, band_count)
    for band in energy_bands:
        band_axes.plot(plot_space, band)

    band_axes.set_xlabel("High Symmetry Points")
    band_axes.set_xticks(list(range(len(lat.points))))
    band_axes.set_xticklabels(lat.point_names)
    band_axes.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")

    plot_densities(energy_bands, density_axes)

    density_axes.set_xlabel("Density")
    density_axes.set_xlim(left = 0)
    # density_axes.axvline(0, color = "k", linewidth = .75)

    canvas.draw()

go_button = ttk.Button(interfaceframe, text = "Plot bands", command = plot_bands)
go_button.grid(column = 0, row = 20)




#####################################################################################################
# setting up the matplotlib canvas

fig = Figure()

band_axes: Axes
density_axes: Axes

# define a gridspec for the displayed subplots, giving more room to the bands than the density plot
grid_spec = \
{
    "width_ratios": (3, 1),
    "wspace": .0,
}
sub_opts = \
{
    "xticklabels": [],
}
band_axes, density_axes = fig.subplots(1, 2, sharey = True, gridspec_kw = grid_spec, subplot_kw = sub_opts)

canvas = FigureCanvasTkAgg(fig, master = mainframe)
canvas.get_tk_widget().grid(column = 0, row = 0, sticky = "NESW")
# make the canvas resize with the window
mainframe.rowconfigure(0, weight = 1)
mainframe.columnconfigure(0, weight = 1)

root.mainloop()
