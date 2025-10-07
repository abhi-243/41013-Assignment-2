import swift
import spatialgeometry as sg
import os

# Path to your directory containing .stl files
mesh_dir = r"C:\Users\abhin\OneDrive\Documents\UTS\Spring Semester 2025\41013 Industrial Robotics\Assignments\A2\41013-Assignment-2\Environment Meshes\Bricks"

# Initialize Swift environment
env = swift.Swift()
env.launch(realtime=True)

# Example color map: you can define a color for each specific file
color_map = {
    "scaled_9327.stl"       : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_9551.stl"       : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_241223.stl"     : (0,       0.2235,  0.3686),   #EARTH BLUE
    "scaled_303701.stl"     : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_408324.stl"     : (0.9686,  0.8196,  0.0706),   #TR. YELLOW
    "scaled_452226.stl"     : (0.0824,  0.0824,  0.0824),   #BLACK
    "scaled_4211065.stl"    : (0.0824,  0.0824,  0.0824),   #BLACK
    "scaled_4298609.stl"    : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_4548180.stl"    : (0.0824,  0.0824,  0.0824),   #BLACK
    "scaled_4632100.stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6029208.stl"    : (0.0824,  0.0824,  0.0824),   #BLACK
    "scaled_6058966.stl"    : (0.0824,  0.0824,  0.0824),   #BLACK
    "scaled_6061047.stl"    : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_6125731.stl"    : (0,       0.5725,  0.2784),   #DARK GREEN
    "scaled_6126046.stl"    : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_6153335.stl"    : (0.9686,  0.8196,  0.0706),   #TR. YELLOW
    "scaled_6167576.stl"    : (0.3922,  0.4039,  0.3961),   #DARK STONE GREY
    "scaled_6170524.stl"    : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_6176636.stl"    : (0.9686,  0.8196,  0.0706),   #TR. YELLOW
    "scaled_6181575.stl"    : (0.8235,  0.8235,  0.8235),   #WARM GOLD DRUM LACQUERED
    "scaled_6186974.stl"    : (0,       0.2235,  0.3686),   #EARTH BLUE
    "scaled_6218226.stl"    : (0.4667,  0.4667,  0.4745),   #COOL SILVER DRUM LACQUERED
    "scaled_6223056.stl"    : (0.2314,  0.2314,  0.0510),   #DARK BROWN
    "scaled_6244785.stl"    : (0.9882,  0.7647,  0.6196),   #LIGHT NOUGAT
    "scaled_6248833.stl"    : (0.9686,  0.8196,  0.0706),   #TR. YELLOW
    "scaled_6251290.stl"    : (0.4980,  0.0745,  0.1059),   #NEW DARK RED
    "scaled_6278396.stl"    : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_6285534.stl"    : (0.0824,  0.0824,  0.0824),   #BLACK
    "scaled_6329585.stl"    : (0.9569,  0.9569,  0.9569),   #WHITE
    "scaled_6365907.stl"    : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE
    "scaled_6365908.stl"    : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE
    "scaled_6370526.stl"    : (0.9608,  0.4902,  0.1255),   #BRIGHT ORANGE
    "scaled_6371360.stl"    : (0,       0.5725,  0.2784)    #DARK GREEN
}

# Loop through all files in directory
for file in os.listdir(mesh_dir):
    if file.endswith(".stl") and file.startswith("scaled_"):
        full_path = os.path.join(mesh_dir, file)
        try:
            mesh = sg.Mesh(filename=full_path)
            
            # Assign color based on filename, default to white if not in color_map
            mesh.color = color_map.get(file, (1, 1, 1))  # RGB values between 0 and 1
            
            env.add(mesh)
            print(f"Loaded {file} with color {mesh.color}")
        except Exception as e:
            print(f"Failed to load {file}: {e}")

print("All STL models loaded into Swift environment.")
input("Press Enter to close...")
