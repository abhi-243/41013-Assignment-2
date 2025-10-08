import swift
import spatialgeometry as sg
import spatialmath as sm
import os
import numpy as np

# Path to your directory containing .stl files
mesh_dir = r"C:\Users\abhin\OneDrive\Documents\UTS\Spring Semester 2025\41013 Industrial Robotics\Assignments\A2\41013-Assignment-2\Environment Meshes\Bricks"

# Initialize Swift environment
env = swift.Swift()
env.launch(realtime=True)

# Example color map: you can define a color for each specific file
color_map = {
    "scaled_9551.stl"          : (0.9569,  0.9569,  0.9569),   #WHITE 
    "scaled_241223(1).stl"     : (0,       0.2235,  0.3686),   #EARTH BLUE
    "scaled_241223(2).stl"     : (0,       0.2235,  0.3686),   #EARTH BLUE
    "scaled_303701.stl"        : (0.9569,  0.9569,  0.9569),   #WHITE 
    "scaled_4211065.stl"       : (0.0824,  0.0824,  0.0824),   #BLACK 
    "scaled_4548180.stl"       : (0.0824,  0.0824,  0.0824),   #BLACK 
    "scaled_4632100(1).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_4632100(2).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_4632100(3).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6029208(1).stl"    : (0.0824,  0.0824,  0.0824),   #BLACK 
    "scaled_6029208(2).stl"    : (0.0824,  0.0824,  0.0824),   #BLACK 
    "scaled_6029208(3).stl"    : (0.0824,  0.0824,  0.0824),   #BLACK 
    "scaled_6029208(4).stl"    : (0.0824,  0.0824,  0.0824),   #BLACK 
    "scaled_6058966.stl"       : (0.0824,  0.0824,  0.0824),   #BLACK 
    "scaled_6061047(1).stl"    : (0.9569,  0.9569,  0.9569),   #WHITE 
    "scaled_6061047(2).stl"    : (0.9569,  0.9569,  0.9569),   #WHITE 
    "scaled_6170524.stl"       : (0.9569,  0.9569,  0.9569),   #WHITE 
    "scaled_6186974.stl"       : (0,       0.2235,  0.3686),   #EARTH BLUE
    "scaled_6218226(1).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6218226(2).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6218226(3).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6218226(4).stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6248833.stl"       : (0.9686,  0.8196,  0.0706),   #TR. YELLOW
    "scaled_6251290.stl"       : (0.4980,  0.0745,  0.1059),   #NEW DARK RED  
    "scaled_6285534.stl"       : (0.0824,  0.0824,  0.0824),   #BLACK 
    "scaled_6329585.stl"       : (0.9569,  0.9569,  0.9569),   #WHITE 
    "scaled_6365907(1).stl"    : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE 
    "scaled_6365907(2).stl"    : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE 
    "scaled_6365908.stl"       : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE 
    "scaled_6370526.stl"       : (0.9608,  0.4902,  0.1255)    #BRIGHT ORANGE 
}

position_map = {
    "scaled_9551.stl"          : (0.04, 0.08, 0.),
    "scaled_241223(1).stl"     : (0.28, 0.08, 0.),
    "scaled_241223(2).stl"     : (0.44, 0.08, 0.064),
    "scaled_303701.stl"        : (0.32, 0.08, 0.032),
    "scaled_4211065.stl"       : (0.48, 0.08, 0.096),
    "scaled_4548180.stl"       : (-0.12, 0.08, 0.128),
    "scaled_4632100(1).stl"    : (0.34627, 0.08, 0.13027),
    "scaled_4632100(2).stl"    : (0.42627, 0.08, 0.13027),
    "scaled_4632100(3).stl"    : (0.50627, 0.08, 0.13027),
    "scaled_6029208(1).stl"    : (-0.16, -0.131, -0.015),
    "scaled_6029208(2).stl"    : (0.48, -0.131, -0.015),
    "scaled_6029208(3).stl"    : (-0.16, 0.291, -0.015),
    "scaled_6029208(4).stl"    : (0.48, 0.291, -0.015),
    "scaled_6058966.stl"       : (0.6, 0.08, 0.216),
    "scaled_6061047(1).stl"    : (0.08, 0.2, 0.032),
    "scaled_6061047(2).stl"    : (0.08, -0.4, 0.032),
    "scaled_6170524.stl"       : (-0.4, 0.08, 0.),
    "scaled_6186974.stl"       : (0.44, 0.08, 0.128),
    "scaled_6218226(1).stl"    : (-0.16, -0.131, 0.015),
    "scaled_6218226(2).stl"    : (-0.16, 0.291, 0.015),
    "scaled_6218226(3).stl"    : (0.48, -0.131, 0.015),
    "scaled_6218226(4).stl"    : (0.48, 0.291, 0.015),
    "scaled_6248833.stl"       : (0.48, 0.08, 0.032),
    "scaled_6251290.stl"       : (0.56, 0.08, 0.064),
    "scaled_6285534.stl"       : (0.16, 0.08, 0.),
    "scaled_6329585.stl"       : (-0.04, 0.08, 0.128),
    "scaled_6365907(1).stl"    : (0.16, -0.12, 0.032),
    "scaled_6365907(2).stl"    : (0.16, 0.28, 0.032),
    "scaled_6365908.stl"       : (-0.08, 0.08, 0.032),
    "scaled_6370526.stl"       : (0.6, 0.08, 0.224)
}

#rotation_map = {
#    "scaled_9551.stl"          : (0, 0, -np.pi/2),
#    "scaled_241223(1).stl"     : (0, 0, np.pi/2),
#    "scaled_241223(2).stl"     : (0, 0, np.pi/2),
#    "scaled_303701.stl"        : (0, 0, -np.pi/2),
#    "scaled_4211065.stl"       : (0, 0, np.pi/2),
#    "scaled_4548180.stl"       : (0, 0, -np.pi/2),
#    "scaled_4632100(1).stl"    : (0, 0, np.pi/2),
#    "scaled_4632100(2).stl"    : (0, 0, np.pi/2),
#    "scaled_4632100(3).stl"    : (0, 0, np.pi/2),
#    "scaled_6029208(1).stl"    : (0, 0, -np.pi/2),
#    "scaled_6029208(2).stl"    : (0, 0, -np.pi/2),
#    "scaled_6029208(3).stl"    : (0, 0, np.pi/2),
#    "scaled_6029208(4).stl"    : (0, 0, np.pi/2),
#    "scaled_6058966.stl"       : (0, 0, np.pi/2),
#    "scaled_6061047(1).stl"    : (0, 0, 0),
#    "scaled_6061047(2).stl"    : (0, 0, np.pi),
#    "scaled_6170524.stl"       : (0, 0, -np.pi/2),
#    "scaled_6186974.stl"       : (0, 0, 0),
#    "scaled_6218226(1).stl"    : (0, 0, np.pi/2),
#    "scaled_6218226(2).stl"    : (0, 0, -np.pi/2),
#    "scaled_6218226(3).stl"    : (0, 0, np.pi/2),
#    "scaled_6218226(4).stl"    : (0, 0, -np.pi/2),
#    "scaled_6248833.stl"       : (0, 0, np.pi/2),
#    "scaled_6251290.stl"       : (np.pi/2, 0, np.pi/2),
#    "scaled_6285534.stl"       : (0, 0, np.pi/2),
#    "scaled_6329585.stl"       : (0, 0, np.pi/2),
#    "scaled_6365907(1).stl"    : (0, 0, 0),
#    "scaled_6365907(2).stl"    : (0, 0, np.pi),
#    "scaled_6365908.stl"       : (0, 0, -np.pi/2),
#    "scaled_6370526.stl"       : (0, 0, np.pi/2)
#}

rotation_map = {
    "scaled_9551.stl"          : (0, 0, 0),
    "scaled_241223(1).stl"     : (np.pi/2, 0, 0),
    "scaled_241223(2).stl"     : (np.pi/2, 0, 0),
    "scaled_303701.stl"        : (-np.pi/2, 0, 0),
    "scaled_4211065.stl"       : (np.pi/2, 0, 0),
    "scaled_4548180.stl"       : (-np.pi/2, 0, 0),
    "scaled_4632100(1).stl"    : (np.pi/2, 0, 0),
    "scaled_4632100(2).stl"    : (np.pi/2, 0, 0),
    "scaled_4632100(3).stl"    : (np.pi/2, 0, 0),
    "scaled_6029208(1).stl"    : (-np.pi/2, 0, 0),
    "scaled_6029208(2).stl"    : (-np.pi/2, 0, 0),
    "scaled_6029208(3).stl"    : (np.pi/2, 0, 0),
    "scaled_6029208(4).stl"    : (np.pi/2, 0, 0),
    "scaled_6058966.stl"       : (np.pi/2, 0, 0),
    "scaled_6061047(1).stl"    : (0, 0, 0),
    "scaled_6061047(2).stl"    : (np.pi/2, 0, 0),
    "scaled_6170524.stl"       : (-np.pi/2, 0, 0),
    "scaled_6186974.stl"       : (0, 0, 0),
    "scaled_6218226(1).stl"    : (np.pi/2, 0, 0),
    "scaled_6218226(2).stl"    : (-np.pi/2, 0, 0),
    "scaled_6218226(3).stl"    : (np.pi/2, 0, 0),
    "scaled_6218226(4).stl"    : (-np.pi/2, 0, 0),
    "scaled_6248833.stl"       : (np.pi/2, 0, 0),
    "scaled_6251290.stl"       : (np.pi/2, 0, np.pi/2),
    "scaled_6285534.stl"       : (np.pi/2, 0, 0),
    "scaled_6329585.stl"       : (np.pi/2, 0, 0),
    "scaled_6365907(1).stl"    : (0, 0, 0),
    "scaled_6365907(2).stl"    : (np.pi, 0, 0),
    "scaled_6365908.stl"       : (-np.pi/2, 0, 0),
    "scaled_6370526.stl"       : (0, 0, 0)
}

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
            pos = position_map.get(file, (0, 0, 0))
            rpy = rotation_map.get(file, (0, 0, 0))

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