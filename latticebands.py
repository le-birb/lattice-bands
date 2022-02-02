
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, filedialog
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib

from json_interface import load_lattice
import empty_lattice
import central_equation

# tell matplotlib to use TkAgg so we can show plots on tkinter windows
matplotlib.use("TkAgg")

root = tk.Tk()
root.title("Lattice Bands")

mainframe = ttk.Frame(root, padding = "12")
mainframe.grid(column = 0, row = 0, sticky = "NESW")
root.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 1)
root.rowconfigure(0, weight = 1)

interfaceframe = ttk.Frame(mainframe, padding = 10)
interfaceframe.grid(column = 1, row = 0, sticky = "NESW")
interfaceframe.rowconfigure(0, weight = 1)
interfaceframe.rowconfigure(1, weight = 1)

lattice_label = ttk.Label(interfaceframe, text = "Select lattice to use:")
lattice_label.grid(column = 0, row = 0, sticky = "S")

files: list[str] = os.listdir("lattices")
json_files = []

for filename in files:
    if filename.endswith(".json"):
        json_files.append(filename[:-5])

lattice = tk.StringVar()
lattice.set("2d_square")
file_menu = ttk.OptionMenu(interfaceframe, lattice, lattice.get(), *json_files)
file_menu.grid(column = 0, row = 1, sticky = "N")

# TODO: add checks elsewhere to ensure empty inputs are handled gracefully
def _validate_num(text: str):
    return text.isdigit() or text == ""

class num_entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validator = self.register(_validate_num)
        self.config(validate = "key", validatecommand = (validator, '%P'))

range_label = ttk.Label(interfaceframe, text = "Nearest neigbors to visit:")
range_label.grid(column = 0, row = 7)

range_var = tk.StringVar(value = "1")
range_entry = num_entry(interfaceframe, textvariable = range_var)
range_entry.grid(column = 0, row = 8)

resolution_label = ttk.Label(interfaceframe, text = "Resolution of plot (higher is better but slower):", wraplength = 150)
resolution_label.grid(column = 0, row = 9)

resolution_var = tk.StringVar(value = "50")
resolution_entry = num_entry(interfaceframe, textvariable = resolution_var)
resolution_entry.grid(column = 0, row = 10)

density_label = ttk.Label(interfaceframe, text = "Make density of states diagram (doesn't work yet):", wraplength = 150)
density_label.grid(column = 0, row = 14)

make_density_plot = tk.BooleanVar(value = False)
density_plot_checkbox = ttk.Checkbutton(interfaceframe, variable = make_density_plot)
density_plot_checkbox.grid(column = 0, row = 15)


def plot_bands():
    band_axes.clear()

    lattice_path = f"lattices/{lattice.get()}.json"
    lat = load_lattice(lattice_path)
    empty_lattice.plot_bands(lat, band_axes, reciprocal_range = int(range_var.get()), resolution = int(resolution_var.get()))

    band_axes.set_xlabel("High Symmetry Points")
    band_axes.set_xticks(list(range(len(lat.points))))
    band_axes.set_xticklabels(lat.point_names)
    band_axes.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")

    canvas.draw()

go_button = ttk.Button(interfaceframe, text = "Plot bands", command = plot_bands)
go_button.grid(column = 0, row = 20)

fig = Figure()

band_axes = fig.add_subplot()

canvas = FigureCanvasTkAgg(fig, master = mainframe)
canvas.get_tk_widget().grid(column = 0, row = 0, sticky = "NESW")

root.mainloop()
