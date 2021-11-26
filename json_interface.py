
import json

from lattice import lattice

def load_lattice(file) -> lattice:
    with open(file, "r") as f:
        lattice_data: dict = json.load(f)
    return lattice(lattice_data["basis"], lattice_data["dimension"], lattice_data["points"], lattice_data["point_names"], lattice_data["line_points"])
