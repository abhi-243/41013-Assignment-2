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
from GUI import RobotControlUI
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

gui = RobotControlUI([IRB120_Abhi,UR3_Given,myCobot320m5,XI1305_Hamish], names=["IRB120", "UR3", "myCobot320", "XI1305"])
gui.render()

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


# Start all robots from zero
q_zero = np.zeros(IRB120_Abhi.n)
IRB120_Abhi.q = q_zero
UR3_Given.q = q_zero
myCobot320m5.q = q_zero
XI1305_Hamish.q = q_zero
env.step(0.1)

##RMRC helper functions
#ee position
def fk_position(robot):
    T = robot.fkine(robot.q)
    return np.array(T.t).flatten()

#jacobian matrix
def linear_jacobian(robot, q):
    J_full = robot.jacob0(q)
    return np.array(J_full[0:3, :], dtype=float)

#joint angle limits
def clip_to_qlim(robot, q):
    try:
        qmin, qmax = robot.qlim
        q_clipped = np.minimum(np.maximum(q, qmin), qmax)
        return q_clipped
    except Exception:
        return q
    
#Variables for rmrc
Kp = 2.0
dt = 0.05
max_steps = 200
vel_limit = 0.2

input("Press Enter to start RMRC demo...")

robots = [IRB120_Abhi, UR3_Given, myCobot320m5, XI1305_Hamish]

#Target positions
targets = [
    [   # IRB120
        np.array([0.1608,  0.0008, 0.107]),   # Position 1
        np.array([0,  0.8, 0.5])    # Position 2
    ],
    [   # UR3
        np.array([0.18707, 0.0008, 0.20527]),   # Position 1
        np.array([0.3, -0.3, 0.5])    # Position 2
    ],
    [   # myCobot
        np.array([-0.5592, 0.0008, 0.075]),  # Position 1
        np.array([-0.5,  0.5, 0.5])   # Position 2
    ],
    [   # XI1305
        np.array([-0.0792, -0.11895, 0.107]),  # Position 1
        np.array([-0.5, -0.5, 0.5])   # Position 2
    ]
]

#target postion loop
for phase in range(2):
    print(f"Moving to target set {phase + 1}")
    p_des_all = [targets[i][phase] for i in range(len(robots))]

    for step in range(max_steps):
        all_reached = True

        for i, robot in enumerate(robots):
            q = robot.q.copy()
            p_cur = fk_position(robot)
            p_des = p_des_all[i]

            error = p_des - p_cur
            err_norm = np.linalg.norm(error)

            #check error within tolerance
            if err_norm < 5e-3:
                continue
            all_reached = False

            v_des = Kp * error
            v_norm = np.linalg.norm(v_des)
            if v_norm > vel_limit:
                v_des = (v_des / v_norm) * vel_limit

            Jv = linear_jacobian(robot, q)
            dq = np.linalg.pinv(Jv).dot(v_des)
            q_next = clip_to_qlim(robot, q + dq * dt)
            robot.q = q_next

        env.step(dt)
        gui.render()
        time.sleep(dt)

        if all_reached:
            break

print("\n✅ RMRC demo complete.")
input("Press Enter to exit...")