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

<<<<<<< Updated upstream
gui = RobotControlUI([IRB120_Abhi,UR3_Given,myCobot320m5,XI1305_Hamish], names=["IRB120", "UR3", "myCobot320", "XI1305"])
gui.render()

# === Load in bricks (start pos) ===
=======
brick_meshes = {}  # Dictionary to store meshes

>>>>>>> Stashed changes
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
            pos = brick["pos_start"]
            rpy = brick["rot_start"]
            mesh.T = sm.SE3(*pos) * sm.SE3.RPY(*rpy, order='xyz')
            
            env.add(mesh)
            env.step(0.01) 
            brick_meshes[file] = mesh
            
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

#ee pose
def fk_pose(robot):
    T = robot.fkine(robot.q)
    pos = np.array(T.t).flatten()
    rpy = np.array(sm.base.tr2rpy(T.R))
    return np.hstack((pos, rpy))


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
Kp = 1
dt = 0.1
max_steps = 200
vel_limit = 0.4

robots = [IRB120_Abhi, UR3_Given, myCobot320m5, XI1305_Hamish]

# Example assignment of bricks to robots
robot_stls = {
    "IRB120": ["20.stl", "7.stl", "15.stl", "17.stl", "18.stl", "19.stl", "26.stl", "30.stl"],           # STLs for IRB120
    "UR3": ["2.stl", "3.stl", "4.stl", "5.stl", "6.stl", "16.stl","25.stl", "29.stl"],     # STLs for UR3
    "myCobot": ["9.stl", "12.stl", "13.stl", "21.stl", "22.stl", "24.stl", "28.stl"],        # STLs for myCobot
    "XI1305": ["8.stl", "10.stl", "11.stl", "14.stl", "23.stl", "27.stl"]          # STLs for XI1305
}
targets = [
    # IRB120 targets
    [
        [0.85733, 0.57601, 0.15, 0, pi, 0],             
        [0.4408, 0.0008, 0.275, 0, pi, 0],           #20
        [0.74013, 0.7584, 0.05, 0, 0, 0],             
        [0.1608, 0.0008, 0.107, 0, 0, 0],           #7
        [0.57912, 0.19498, 0.05, 0, 0, 0],            
        [0.2808, 0.0008, 0.203, 0, 0, 0],           #15
        [0.49374, 0.82848, 0.05, 0, 0, 0],           
        [0.26707, 0.0008, 0.20527, 0, 0, 0],           # 17
        [0.29378, 0.77646, 0.05, 0, 0, 0], 
        [0.34707, 0.0008, 0.20527, 0, 0, 0],           # 18
        [0.67258, 0.39539, 0.05, 0, 0, 0],  
        [0.4408, 0.0008, 0.266, 0, 0, 0],           #19
        [0.30067, 0.34492, 0.05, 0, 0, 0],         
        [0.3208, 0.2118, 0.08, 0, 0, 0],           #26
        [0.24255, -0.6451, 0.05, 0, 0, 0], 
        [0.3208, 0.2118, 0.05, 0, 0, 0],          #30
    ],

    # UR3 targets
    [
        [0.75995, -0.5573, 0.08, 0, pi, 0],
        [0.3208, 0.0008, 0.107, 0, pi, 0], #2
        [0.74537, -0.77453, 0.05, 0, 0, 0],
        [0.4008, 0.0008, 0.139, 0, 0, 0],#3
        [0.55536, -0.25309, 0.05, 0, 0, 0],
        [0.1208, 0.0008, 0.075, 0, 0, 0],#4
        [0.24783, -0.46479, 0.05, 0, 0, 0],
        [0.2808, 0.0008, 0.139, 0, 0, 0],#5
        [0.33452, -0.8627, 0.05, 0, 0, 0],
        [0.3208, 0.0008, 0.171, 0, 0, 0],#6
        [0.80295, -0.30272, 0.05, 0, 0, 0],
        [0.18707, 0.0008, 0.20527, 0, 0, 0],#16
        [0.58453, -0.84006, 0.05, 0, 0, 0],
        [0.3208, -0.2102, 0.08, 0, 0, 0], #25
        [0.2417, 0.52362, 0.05, 0, 0, 0],
        [-0.3192, 0.2118, 0.05, 0, 0, 0],#29
    ],

    # myCobot targets
    [
        [-0.19349, 0.56355, 0.0, 0, 0, 0],
        [-0.0792, 0.1208, 0.107, 0, 0, 0], #9
        [-0.2432, 0.70297, 0.05, 0, 0, 0],
        [0.0008, 0.2008, 0.107, 0, 0, 0], #12
        [-0.5469, 0.74508, 0.05, 0, 0, 0],
        [-0.2392, 0.0008, 0.107, 0, 0, 0], #13
        [-0.48085, 0.26724, 0.05, 0, 0, 0],
        [-0.2792, 0.0008, 0.203, 0, 0, 0], #21
        [-0.66261, 0.30192, 0.05, 0, 0, 0],
        [-0.1992, 0.0008, 0.203, 0, 0, 0], #22
        [-0.74034, 0.45166, 0.05, 0, 0, 0],
        [-0.3192, 0.2118, 0.08, 0, 0, 0], #24
        [-0.76188, 0.65304, 0.05, 0, 0, 0],
        [0.3208, -0.2102, 0.05, 0, 0, 0], #28
    ],

    # XI1305 targets "XI1305": ["8.stl", "10.stl", "11.stl", "14.stl", "23.stl", "27.stl"]    
    [
        [-0.7277, -0.69698, 0.05, 0, pi, 0],
        [-0.1192, 0.0008, 0.075, 0, pi, 0], #8
        [-0.21167, -0.59785, 0.05, 0, 0, 0],
        [-0.0792, -0.11895, 0.107, 0, 0, 0], #10
        [-0.21111, -0.43383, 0.05, 0, 0, 0],
        [0.0008, -0.1992, 0.107, 0, 0, 0], #11
        [-0.46877, -0.75245, 0.05, 0, 0, 0],
        [-0.5592, 0.0008, 0.075, 0, 0, 0], #14
        [-0.7384, -0.46326, 0.05, 0, 0, 0],
        [-0.3192, -0.2102, 0.08, 0, 0, 0], #23
        [-0.68106, -0.25906, 0.05, 0, 0, 0],
        [-0.3192, -0.2102, 0.05, 0, 0, 0], #27
    ]
]
 
max_phases = max(len(robot_targets) for robot_targets in targets)
approach_offset = 0.05
# ---------- Attach/place helpers (drop-in) ----------
def attach_mesh_to_ee(robot, mesh, rot_offset=None, height_offset=0.0):
    try:
        robot.env.remove(mesh)
    except Exception:
        pass

    if rot_offset is None:
        rot_offset = sm.SE3()


    z_offset = sm.SE3(0, 0, height_offset)
    flip_rot = sm.SE3.Rx(np.pi)
    mesh.T = flip_rot * rot_offset * z_offset

    ee_link = robot.links[-1]
    ee_link._children.append(mesh)

    print(f"Attached {os.path.basename(mesh.filename)} to {robot.name} (flipped & offset applied)")
    return mesh.T


def place_brick_at_pose(brick_mesh, pose):
    pose = np.array(pose, dtype=float)
    if pose.size < 6:
        pose = np.hstack((pose, np.zeros(6 - pose.size)))
    T_world = sm.SE3(*pose[:3]) * sm.SE3.RPY(*pose[3:], order='xyz')
    brick_mesh.T = T_world
    return T_world

def detach_mesh_from_ee(env, robot, mesh, height_offset=-0.03):

    ee_link = robot.links[-1]
    if mesh in ee_link._children:
        ee_link._children.remove(mesh)
        print(f"Detached {mesh.filename} from {robot.name}")
    
    mesh.T = robot.fkine(robot.q) * sm.SE3(0, 0, height_offset)
    env.add(mesh)


# ---------- State ----------
attached_meshes = [None] * len(robots)      
placing_scheduled = [False] * len(robots)  
place_pose_next = [None] * len(robots)

# offsets
rot_offset = sm.SE3.Rx(np.pi)             
height_offset = -0.019                     
tol_pos = 5e-3   # 5 mm tolerance

# ---------- RMRC LOOP with alternating pick & place ----------
attached_meshes = [None] * len(robots) 

for phase in range(max_phases):
    print(f"\n--- Phase {phase + 1} ---")

    # desired pose
    p_des_all = [
        targets[i][phase] if phase < len(targets[i]) else targets[i][-1]
        for i in range(len(robots))
    ]

    for step in range(max_steps):
        all_reached = True

        for i, robot in enumerate(robots):
            q = robot.q.copy()
            pose_cur = fk_pose(robot)
            pose_des = np.array(p_des_all[i], dtype=float)

            if pose_des.size < 6:
                pose_des = np.hstack((pose_des, np.zeros(6 - pose_des.size)))

            p_cur, rpy_cur = pose_cur[:3], pose_cur[3:]
            p_des, rpy_des = pose_des[:3], pose_des[3:]

            pos_error = p_des - p_cur
            R_cur = sm.base.rpy2r(*rpy_cur)
            R_des = sm.base.rpy2r(*rpy_des)
            rot_error = np.array(sm.base.tr2rpy(R_des @ R_cur.T))

            if np.linalg.norm(pos_error) < 5e-3:
                #pick/place func
                if phase % 2 == 0:
                    if attached_meshes[i] is None:
                        robot_name = robot.name.replace("320m5", "")
                        stl_list = robot_stls.get(robot_name, [])
                        if phase // 2 < len(stl_list):
                            stl_name = stl_list[phase // 2]
                            stl_mesh = brick_meshes.get(stl_name)
                            if stl_mesh:
                                # Attach STL to EE
                                T_rel = attach_mesh_to_ee(robot, stl_mesh, height_offset=-0.03)
                                attached_meshes[i] = {"mesh": stl_mesh, "T_rel": T_rel, "name": stl_name}
                                print(f"{robot.name} picked up {stl_name}")

                else:  #odd phase place
                    if attached_meshes[i] is not None:
                        entry = attached_meshes[i]
                        mesh = entry["mesh"]
                        detach_mesh_from_ee(env, robot, mesh)
                        attached_meshes[i] = None
                        print(f"{robot.name} placed {mesh.filename}")

                continue

            all_reached = False

            # RMRC velocity control
            v_des = Kp * np.hstack((pos_error, rot_error))
            v_norm = np.linalg.norm(v_des[:3])
            if v_norm > vel_limit:
                v_des[:3] = (v_des[:3] / v_norm) * vel_limit

            J_full = np.array(robot.jacob0(q), dtype=float)
            λ = 0.1
            dq = J_full.T @ np.linalg.inv(J_full @ J_full.T + λ**2 * np.eye(6)) @ v_des
            q_next = clip_to_qlim(robot, q + dq * dt)
            robot.q = q_next

            # Update attached mesh position
            if attached_meshes[i] is not None:
                entry = attached_meshes[i]
                entry["mesh"].T = robot.fkine(robot.q) * entry["T_rel"]

        env.step(dt)
        gui.render()
        time.sleep(dt)

        if all_reached:
            break
