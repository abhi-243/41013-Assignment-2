import swift
import spatialgeometry as sg
import spatialmath as sm
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

mesh_path = os.path.join(BASE_DIR, "Environment", "City_Street_Set.dae")

# === Launch Swift environment ===
env = swift.Swift()
env.launch(realtime=True)

# === Load and configure mesh ===
mesh = sg.Mesh(filename=mesh_path)
mesh.color = (0.8, 0.2, 0.2)  # RGB (red)
mesh.T = sm.SE3(0.1, 0.0, 0.0) * sm.SE3.RPY(0, 0, 0, order='xyz')

# === Add to Swift ===
env.add(mesh)

print(f"Loaded model: {os.path.basename(mesh_path)}")
input("Press Enter to exit...")