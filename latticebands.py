
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
from json_interface import load_lattice
import empty_lattice

# tell matplotlib to use TkAgg so we can show plots on tkinter windows
matplotlib.use("TkAgg")

root = tk.Tk()
root.title("Lattice Bands")

mainframe = ttk.Frame(root, padding = "12")
mainframe.grid(column = 0, row = 0, sticky = "NESW")
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

interfaceframe = ttk.Frame(mainframe)
interfaceframe.grid(column = 1, row = 0, sticky = "E")

def get_lattice_file():
    lattice_path.set(filedialog.askopenfilename(initialdir = "lattices"))

lattice_path = tk.StringVar(value = "No lattice selected")

filelbl = ttk.Label(interfaceframe, textvariable = lattice_path, wraplength = 150)
filelbl.grid(column = 0, row = 0, sticky = "S")
filebtn = ttk.Button(interfaceframe, text = "Select lattice file", command = get_lattice_file)
filebtn.grid(column = 0, row = 1, sticky = "N")

def plot_bands():
    band_axes.clear()

    lat = load_lattice(lattice_path.get())
    empty_lattice.plot_bands(lat, band_axes)

    band_axes.set_xlabel("High Symmetry Points")
    band_axes.set_xticks(list(range(len(lat.points))))
    band_axes.set_xticklabels(lat.point_names)
    band_axes.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")

    canvas.draw()




gobtn = ttk.Button(interfaceframe, text = "Plot bands", command = plot_bands)
gobtn.grid(column = 0, row = 2)

band_fig = Figure()

band_axes = band_fig.add_subplot()

canvas = FigureCanvasTkAgg(band_fig, master = mainframe)
canvas.get_tk_widget().grid(column = 0, row = 0, sticky = "NESW")

root.mainloop()
