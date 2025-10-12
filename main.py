from IRB120.IRB120 import IRB120
from Environment_Meshes.brick_data import color_map, position_map_end, position_map_start, rotation_map_end, rotation_map_start
from ir_support import UR3
import swift
import spatialgeometry as sg
import spatialmath as sm
import roboticstoolbox as rtb
import numpy as np
import os
from math import pi

env_mesh_path = r"Assignments\A2\41013-Assignment-2\Environment_Meshes\Environment\City_Street_Set.dae"
car_mesh_path = r"Assignments\A2\41013-Assignment-2\Environment_Meshes\Race_Car_correct.dae"
bricks_mesh_path = r"Assignments\A2\41013-Assignment-2\Environment_Meshes\Bricks"

# === Launch Swift ===
env = swift.Swift()
env.launch(realtime=True)
env.step(0.1)

# === Initialize robots ===
robot1 = IRB120()
robot2 = UR3()

# === Set base poses instead of passing `pose=` to env.add() ===
robot1.base = sm.SE3(0.0, 0.5, 0.05) * sm.SE3.RPY(0, 0, 0, order='xyz')
robot2.base = sm.SE3(0.0, 2.0, 0.05) * sm.SE3.RPY(0, 0, 0, order='xyz')

# === Add robots to Swift ===
robot1.add_to_env(env)
robot2.add_to_env(env)

# === Load environment mesh ===
env_mesh = sg.Mesh(filename=env_mesh_path)
env_mesh.color = (0.6, 0.6, 0.6)
env_mesh.T = sm.SE3(0, 0, 0)
env.add(env_mesh)

for file in os.listdir(bricks_mesh_path):
    if file.endswith(".stl") and file.startswith("scaled_"):
        full_path = os.path.join(bricks_mesh_path, file)
        try:
            mesh = sg.Mesh(filename=full_path)
            mesh.color = color_map.get(file, (1, 1, 1))
            pos = position_map_end.get(file, (0, 0, 0))
            rpy = rotation_map_end.get(file, (0, 0, 0))
            mesh.T = sm.SE3(*pos) * sm.SE3.RPY(*rpy, order='xyz')
            
            env.add(mesh)
            env.step(0.01)  # Step after each addition
            print(f"Loaded {file} → Pos: {pos}, Rot: {rpy}, Color: {mesh.color}")
        except Exception as e:
            print(f"Failed to load {file}: {e}")

# === Simple motion demo ===
q_start = np.zeros(robot1.n)
q_goal  = q_start + np.array([pi/6, -pi/4, pi/3, 0, pi/6, 0])
traj = rtb.jtraj(q_start, q_goal, 50).q

robot1.q = q_start
robot2.q = q_start
env.step(0.01)

input("Run motion test")
print("Running motion...")
for q in traj:
    robot1.q = q
    robot2.q = q
    env.step(0.02)

print(f"Loaded environment: {os.path.basename(env_mesh_path)}")
input("Press Enter to exit...")