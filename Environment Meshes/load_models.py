import swift
import spatialgeometry as sg
import spatialmath as sm
import os
from brick_data import color_map, position_map_end, position_map_start, rotation_map_end, rotation_map_start

# Path to your directory containing .stl files
mesh_dir = r"C:\Users\abhin\OneDrive\Documents\UTS\Spring Semester 2025\41013 Industrial Robotics\Assignments\A2\41013-Assignment-2\Environment Meshes\Bricks"

# Initialize Swift environment
env = swift.Swift()
env.launch(realtime=True)

# ===== MAIN LOOP =====
for file in os.listdir(mesh_dir):
    if file.endswith(".stl") and file.startswith("scaled_"):
        full_path = os.path.join(mesh_dir, file)
        try:
            # Load mesh
            mesh = sg.Mesh(filename=full_path)

            # Set color
            mesh.color = color_map.get(file, (1, 1, 1))

            # Get position & rotation
            pos = position_map_start.get(file, (0, 0, 0))
            rpy = rotation_map_start.get(file, (0, 0, 0))

            # Build SE3 transformation
            T = sm.SE3(*pos) * sm.SE3.RPY(*rpy, order='xyz')

            # Apply transform
            mesh.T = T

            # Add to environment
            env.add(mesh)
            print(f"Loaded {file} → Pos: {pos}, Rot (rpy): {rpy}, Color: {mesh.color}")

        except Exception as e:
            print(f"Failed to load {file}: {e}")

print("All STL models loaded with position and rotation.")
input("Press Enter to close...")