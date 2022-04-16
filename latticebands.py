
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
from matplotlib.colors import to_rgba
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
file_menu.grid(column = 0, row = 1, sticky = "N", pady = (0, 20))




#####################################################################################################
# define number entry boxes

# fails for negative values
def _validate_int(text: str):
    return text.isdigit() or text == ""

class IntString(tk.StringVar):
    """
    Wrapper for tk.StringVar for use with int_entry.
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

class int_entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validator = self.register(_validate_int)
        # this is the incantaion I found to make text validation work
        self.config(validate = "key", validatecommand = (validator, '%P'))


def _validate_float(text: str):
    # try to split at a decimal point
    match text.split("."):
        # if there isn't a decimal point, it should be an integer
        case [integer]:
            return _validate_int(integer)
        # if there is, both before and after the decimal point should "look like" integers
        case [integer, fraction]:
            return _validate_int(integer) and _validate_int(fraction)
        # otherwise (more than one '.'), fail
        case _:
            return False
            
class FloatString(tk.StringVar):
    """
    Wrapper for tk.StringVar for use with float_entry.
    Allows entry of a string but ensures a float value.
    """
    def __init__(self, *args, default: float = 1, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = default

    def get(self) -> float:
        tempval = super().get()
        if tempval == "":
            return self._default
        else:
            return float(tempval)

class float_entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validator = self.register(_validate_float)
        # this is the incantaion I found to make text validation work
        self.config(validate = "key", validatecommand = (validator, '%P'))

#####################################################################################################
# potential selector

potential_frame = ttk.Frame(interfaceframe)
potential_frame.grid(column = 0, row = 2, sticky = "N")

potentials_to_plot: list[potential_entry] = []

def add_potential():
    new_pot = potential_entry(potential_frame)
    new_pot.pack(pady = (0, 10))
    potentials_to_plot.append(new_pot)

add_potential_buton = ttk.Button(potential_frame, text = "Add potential to plot", command = add_potential)
add_potential_buton.pack(anchor = "n", pady = (0, 10))

potential_map = \
{
    "Empty lattice": potentials.empty_v,
    "Simple": potentials.simple_v,
    "Quadratic": potentials.typical_v,
}
_max_pot_width = max(len(k) for k in potential_map.keys())

line_styles_map = \
{
    "Solid": "-",
    "Dashed": "--",
    "Dotted": ":",
    "Dash-dot": "-."
}
_max_line_width = max(len(k) for k in line_styles_map.keys())

colors = \
[
    "red",
    "blue",
    "green",
    "black",
    "grey",
    "darkred",
    "darkblue",
    "darkgreen",
    "darkgray",
    "rainbow",
]
_max_color_width = max(len(k) for k in colors)

class potential_entry(ttk.Frame):
    """GUI element for displaying and editing parameters of 
    potenitals being plotted, as well as plotting styles.
    """
    # TODO list:
    # Add labels for most elements to explain what they do
    # Maybe check to make sure the delete button doesn't have a memory leak
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.separator = ttk.Separator(self, orient = "horizontal")
        self.separator.grid(row = 0, column = 0, columnspan = 100, sticky = "EW", pady = (0, 5))

        self.approximation_label = ttk.Label(self, text = "Select approximation:")
        self.approximation_label.grid(row = 1, column = 0, columnspan = 2, sticky = "W")

        self.potential_name = tk.StringVar(value = "Empty lattice")
        self.potential_selector = ttk.Combobox(self, textvariable = self.potential_name, state = "readonly", values = list(potential_map.keys()), width = _max_pot_width)
        self.potential_selector.current(0)
        self.potential_selector.grid(row = 1, column = 2, columnspan = 3, padx = 5, sticky = "W")

        # self.scale_label = ttk.Label(self, text = "Strength:")
        # self.scale_label.grid(row = 1, column = 2, columnspan = 2, sticky = "E", padx = (5, 0))

        self.scale_var = FloatString(value = "1", default = 1)
        # self.scale_entry = num_entry(self, textvariable = self.scale_var, width = 4)
        # self.scale_entry.grid(row = 1, column = 4, columnspan = 2, sticky = "W", padx = (0, 5))

        self.del_btn = ttk.Button(self, command = self.remove, text = "Remove", width = 8)
        self.del_btn.grid(row = 1, column = 10, sticky = "E")

        self.style_label = ttk.Label(self, text = "Line style:")
        self.style_label.grid(row = 2, column = 0, sticky = "W")

        self.linestyle = tk.StringVar(value = "Solid")
        self.style_selector = ttk.Combobox(self, textvariable = self.linestyle, state = "readonly", values = list(line_styles_map.keys()), width = _max_line_width)
        self.style_selector.grid(row = 3, column = 0, sticky = "W")

        self.color_label = ttk.Label(self, text = "Color:")
        self.color_label.grid(row = 2, column = 1, sticky = "W", columnspan = 2)

        self.linecolor = tk.StringVar(value = "black")
        self.color_selector = ttk.Combobox(self, textvariable = self.linecolor, state = "readonly", values = colors, width = _max_color_width)
        self.color_selector.grid(row = 3, column = 1, columnspan = 2, sticky = "W")

        self.alpha_label = ttk.Label(self, text = "Opacity:")
        self.alpha_label.grid(row = 2, column = 4, sticky = "W")

        # use a 0-255 range to leverage existing code for integer handling, but convert to 0-1 later
        self.linealpha = FloatString(value = "1", default = 1)
        self.alpha_entry = float_entry(self, textvariable = self.linealpha, width = 4)
        self.alpha_entry.grid(row = 3, column = 4, sticky = "W")

        self.density_label = ttk.Label(self, text = "Check to make density of states plot:")
        self.density_label.grid(row = 4, column = 0, columnspan = 4)

        self.is_density_checked = tk.BooleanVar(value = False)
        self.density_check = ttk.Checkbutton(self, variable = self.is_density_checked, command = self.density_callback)
        self.density_check.grid(row = 4, column = 10)

    def density_callback(self):
        for entry in potentials_to_plot:
            if entry is not self:
                entry.is_density_checked.set(False)

    def get_potential(self):
        return functools.partial(potential_map[self.potential_name.get()], scale = self.scale_var.get())

    def get_line_style(self):
        return line_styles_map[self.linestyle.get()]

    def get_line_color(self):
        return self.linecolor.get()

    def get_line_alpha(self):
        return self.linealpha.get()

    def remove(self):
        self.pack_forget()
        potentials_to_plot.remove(self)

# have something be plotted by default at least
add_potential()
potentials_to_plot[0].is_density_checked.set(True)

#####################################################################################################
# plot parameters - resolution and range

range_label = ttk.Label(interfaceframe, text = "Number of bands to plot:")
range_label.grid(column = 0, row = 7)

range_var = IntString(value = "9", default = 9)
range_entry = int_entry(interfaceframe, textvariable = range_var)
range_entry.grid(column = 0, row = 8)

resolution_label = ttk.Label(interfaceframe, text = "Resolution of plot (sample rate between symmetry points):", wraplength = 150)
resolution_label.grid(column = 0, row = 9)

resolution_var = IntString(value = "50", default = 50)
resolution_entry = int_entry(interfaceframe, textvariable = resolution_var)
resolution_entry.grid(column = 0, row = 10)


#####################################################################################################
# setting up the go button and plotting function
# TODO: look into moving some of these algorithm details to their own function or maybe even module

def plot_bands():
    band_axes.clear()
    density_axes.clear()

    lattice_filepath = f"lattices/{lattice.get()}.json"
    lat = load_lattice(lattice_filepath)

    for point in lat.vertical_lines:
        band_axes.axvline(point, linestyle = "--", color = (.5, .5, .5, .5))

    band_count = range_var.get()
    resolution = resolution_var.get()

    band_paths = lat.get_paths(resolution)
    plot_ranges = []
    for i in range(len(band_paths)):
        plot_ranges.append(np.linspace(i, i+1, resolution))
    
    path = np.array(list(chain.from_iterable(band_paths)))
    plot_space = np.array(list(chain.from_iterable(plot_ranges)))

    density_energies = None

    for entry in potentials_to_plot:
        potential = entry.get_potential()
    
        style_params = {}
        style_params.update(linestyle = entry.get_line_style())
        if entry.get_line_color() != "rainbow":
            style_params.update(color = to_rgba(entry.get_line_color(), entry.get_line_alpha()))

        energy_bands = central_equation.get_bands(path, potential, band_count)
        for band in energy_bands:
            band_axes.plot(plot_space, band, **style_params)

        if entry.is_density_checked.get():
            density_energies = energy_bands

    band_axes.set_xlabel("High Symmetry Points")
    band_axes.set_xticks(list(range(len(lat.points))))
    band_axes.set_xticklabels(lat.point_names)
    band_axes.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")

    band_axes.relim()
    band_axes.autoscale()

    if density_energies is not None:
        plot_densities(density_energies, density_axes)

    density_axes.set_xlabel("Density")
    density_axes.set_xlim(left = 0)

    canvas.draw()

go_button = ttk.Button(interfaceframe, text = "Plot bands", command = plot_bands)
go_button.grid(column = 0, row = 20)




#####################################################################################################
# setting up the matplotlib canvas

# TODO: see if the density subplot can be hidden/resummoned at will

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
