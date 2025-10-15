from IRB120.IRB120 import IRB120
from myCobot320m5.milan import myCobot
from XI1305_module.XI1305_robot import XI1305
from Environment_Meshes.test import stl_data
from teach_pendant import TeachPendant
from ir_support import UR3
import swift
import spatialgeometry as sg
import spatialmath as sm
import roboticstoolbox as rtb
import numpy as np
import os
from math import pi
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env_mesh_path = os.path.join(BASE_DIR, "Environment_Meshes", "Environment", "City_Street_Set-test.dae")
car_mesh_path = os.path.join(BASE_DIR, "Environment_Meshes", "Race_Car_correct.dae")
bricks_mesh_path = os.path.join(BASE_DIR, "Environment_Meshes", "Bricks")

# === Set working directory to project root ===
os.chdir(BASE_DIR)
print("Working directory set to:", os.getcwd())

# === Launch Swift ===
env = swift.Swift()
env.launch(realtime=True)
env.step(0.1)

# === Initialize robots ===
IRB120_Abhi = IRB120()
UR3_Given = UR3()
myCobot320m5 = myCobot()
XI1305_Hamish = XI1305()

# # === Initialize Teach Pendant ===
# robots = {
#     "IRB120": IRB120_Abhi,
#     "UR3": UR3_Given,
#     "myCobot320": myCobot320m5,
#     "XI1305": XI1305_Hamish
# }
# 
# pendant = TeachPendant(env, robots)

# === Set base poses instead of passing `pose=` to env.add() ===
IRB120_Abhi.base = sm.SE3(0.5, 0.5, 0.05) * sm.SE3.RPY(-np.pi/2, 0, 0, order='xyz')
UR3_Given.base = sm.SE3(0.5, -.5, 0.05) * sm.SE3.RPY(np.pi, 0, 0, order='xyz')
myCobot320m5.base = sm.SE3(-0.5, 0.5, 0.05) * sm.SE3.RPY(np.pi, 0, 0, order='xyz')
XI1305_Hamish.base = sm.SE3(-0.5, -.5, 0.05) * sm.SE3.RPY(np.pi, 0, 0, order='xyz')

# === Add robots to Swift ===
IRB120_Abhi.add_to_env(env)
UR3_Given.add_to_env(env)
myCobot320m5.add_to_env(env)
XI1305_Hamish.add_to_env(env)

# === Load environment mesh ===
env_mesh = sg.Mesh(filename=env_mesh_path)
env_mesh.color = (0.6, 0.6, 0.6)
env_mesh.T = sm.SE3(0, 0, 0)
env.add(env_mesh)

# === Load in bricks (start pos) ===
for file in os.listdir(bricks_mesh_path):
    if file.endswith(".stl"):
        full_path = os.path.join(bricks_mesh_path, file)
        try:
            mesh = sg.Mesh(filename=full_path)
            
            # Fetch all properties from stl_data
            brick = stl_data.get(file, None)
            if brick is None:
                print(f"No data found for {file}, skipping...")
                continue

            mesh.color = brick["color"]
            pos = brick["pos_end"]
            rpy = brick["rot_end"]
            mesh.T = sm.SE3(*pos) * sm.SE3.RPY(*rpy, order='xyz')
            
            env.add(mesh)
            env.step(0.01)  # Step after each addition
            print(f"Loaded {file} → Pos: {pos}, Rot: {rpy}, Color: {mesh.color}")
        except Exception as e:
            print(f"Failed to load {file}: {e}")

# Function to generate a random joint angle within robot limits if available
def random_joint_angles(robot):
    try:
        q_min, q_max = robot.qlim
        return np.random.uniform(q_min, q_max)
    except AttributeError:
        # Default fallback if no limits are defined
        return np.random.uniform(-np.pi, np.pi, robot.n)

# Start all robots from zero
q_zero = np.zeros(IRB120_Abhi.n)
IRB120_Abhi.q = q_zero
UR3_Given.q = q_zero
myCobot320m5.q = q_zero
XI1305_Hamish.q = q_zero
env.step(0.1)

input("Press Enter to start random motion demo...")

# Perform 10 random moves for each robot
for move_idx in range(10):
    print(f"\n=== Random Move {move_idx + 1}/10 ===")

    # Generate random targets for each robot
    q_rand_IRB120 = random_joint_angles(IRB120_Abhi)
    q_rand_UR3 = random_joint_angles(UR3_Given)
    q_rand_myCobot = random_joint_angles(myCobot320m5)
    q_rand_XI1305 = random_joint_angles(XI1305_Hamish)

    # Create smooth joint-space trajectories
    traj_IRB120 = rtb.jtraj(IRB120_Abhi.q, q_rand_IRB120, 50).q
    traj_UR3 = rtb.jtraj(UR3_Given.q, q_rand_UR3, 50).q
    traj_myCobot = rtb.jtraj(myCobot320m5.q, q_rand_myCobot, 50).q
    traj_XI1305 = rtb.jtraj(XI1305_Hamish.q, q_rand_XI1305, 50).q

    # Animate trajectories simultaneously
    for i in range(50):
        IRB120_Abhi.q = traj_IRB120[i]
        UR3_Given.q = traj_UR3[i]
        myCobot320m5.q = traj_myCobot[i]
        XI1305_Hamish.q = traj_XI1305[i]
        env.step(0.03)

print("All 10 random motions completed.")
input("Press Enter to exit...")

#pendant.run()