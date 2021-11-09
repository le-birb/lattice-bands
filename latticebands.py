
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

lattice_path = tk.StringVar(value = "")

filelbl = ttk.Label(interfaceframe, textvariable = lattice_path).grid(column = 0, row = 0, sticky = "S")
filebtn = ttk.Button(interfaceframe,text = "Select lattice file", command = get_lattice_file).grid(column = 0, row = 1, sticky = "N")


fig = Figure()

canvas = FigureCanvasTkAgg(fig, master = mainframe)
canvas.get_tk_widget().grid(column = 0, row = 0, sticky = "NESW")

root.mainloop()
