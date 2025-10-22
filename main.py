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
import serial
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
IRB120_Abhi.base = sm.SE3(0.4, 0.4, 0.05) * sm.SE3.RPY(-np.pi/2, 0, 0, order='xyz')
UR3_Given.base = sm.SE3(0.35, -.35, 0.05) * sm.SE3.RPY(np.pi, 0, 0, order='xyz')
myCobot320m5.base = sm.SE3(-0.5, 0.45, 0.05) * sm.SE3.RPY(0, 0, 0, order='xyz')
XI1305_Hamish.base = sm.SE3(-0.5, -0.5, 0.05) * sm.SE3.RPY(0, 0, 0, order='xyz')

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

# === Create UI Object and initialize serial com ===
gui = RobotControlUI([IRB120_Abhi,UR3_Given,myCobot320m5,XI1305_Hamish], names=["IRB120", "UR3", "myCobot320", "XI1305"])

ser = serial.Serial('COM9', 9600, timeout=1)

brick_meshes = {}  # Dictionary to store all loaded brick meshes

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
XI1305_Hamish.q = np.array([0, -pi/4, pi/2, 0, 0, 0])
myCobot320m5.tool = sm.SE3.Rx(np.pi/2)  # adjust if EE points sideways
XI1305_Hamish.tool = sm.SE3.Rx(np.pi)   # flip so z-axis points down
env.step(0.1)

##RMRC helper functions
def check_self_collision(robot):
    return False  # temporarily disable


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
Kp = 2
dt = 0.1
max_steps = 200
vel_limit = 0.8

robots = [IRB120_Abhi, UR3_Given, myCobot320m5, XI1305_Hamish]

robot_name_map = {
    IRB120_Abhi: "IRB120",
    UR3_Given: "UR3",
    myCobot320m5: "myCobot",
    XI1305_Hamish: "XI1305"
}


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
        [0.4408, 0.0008, 0.275, pi/2, 0, 0],           #20
        [0.44013, 0, 0.05, 0, pi, 0],             
        [0.258, 0.0008, 0.107, -pi/2, 0, 0],           #7
        [0.37912, 0.15498, 0.05, 0, pi, 0],            
        [0.2808, 0.0008, 0.203, 0, -pi, 0],           #15
        [0.59374, -0.1048, 0.05, 0, 0, 0],           
        [0.26707, 0.0008, 0.20527, -pi/2, 0, 0],           # 17
        [0.49378, 0.27646, 0.05, 0, pi, 0], 
        [0.34707, -0.0008, 0.20527, pi/2, 0, 0],           # 18
        [0.67258, 0.39539, 0.05, 0, pi, 0],  
        [0.4408, 0.0008, 0.266, pi, 2*pi, 0],           #19
        [0.30067, 0.34492, 0.05, 0, pi, 0],         
        [0.3208, 0.2118, 0.08, 0, 0, 0],           #26
        [0.24255, -0.6451, 0.05, 0, 0, 0], 
        [0.3208, 0.2118, 0.05, 0, 0, 0],          #30
    ],

    # UR3 targets
    [
        [0.75995, -0.5573, 0.08, 0, pi, 0],
        [0.3208, 0.0008, 0.107,-pi/2, pi, pi, ], #2
        [0.6, -0.57453, 0.05, 0, 0, 0],
        [0.39531263, -0.01938878, 0.14125708, 0, pi/2, pi/2],#3
        [0.55536, -0.25309, 0.05, 0, 0, 0],
        [0.1208, 0.0008, 0.075, 0, pi, 0],#4
        [0.14783, -0.46479, 0.05, 0, pi, 0],
        [0.2808, 0.0008, 0.1, pi/2, pi, 0],#5
        [0.23452, -0.4627, 0.05, 0, 0, 0],
        [0.3208, 0.0008, 0.171, 0, 0, 0],#6
        [0.80295, -0.30272, 0.05, 0, pi, 0],
        [0.18707, 0.0008, 0.20527, pi/2, 0, 0],#16
        [0.58453, -0.84006, 0.05, 0, 0, 0],
        [0.3208, -0.2102, 0.08, 0, 0, 0], #25
        [0.2417, 0.52362, 0.05, 0, 0, 0],
        [-0.3192, 0.2118, 0.05, 0, 0, 0],#29
    ],

    # myCobot targets
    [
        [-0.19349, 0.56355, 0.05, 0, 0, 0],
        [-0.0792, 0.2008, 0.107, 0, 0, 0], #9
        [-0.2432, 0.70297, 0.05, 0, 0, 0],
        [0.0008, 0.2008, 0.107, 0, 0, 0], #12
        [-0.5469, 0.74508, 0.05, 0, 0, 0],
        [-0.2392, 0.0008, 0.107, 0, 0, 0], #13
        [-0.48085, 0.26724, 0.05, 0, 0, 0],
        [-0.2792, 0.0008, 0.203, 0, 0, 0], #21
        [-0.66261, 0.10192, 0.05, 0, 0, 0],
        [-0.1992, 0.0008, 0.203, 0, 0, 0], #22
        [-0.74034, 0.45166, 0.05, 0, 0, 0],
        [-0.3192, 0.2118, 0.08, 0, 0, 0], #24
        [-0.76188, 0.65304, 0.05, 0, 0, 0],
        [0.3208, -0.2102, 0.05, 0, 0, 0], #28
    ],

    # XI1305 targets "XI1305": ["8.stl", "10.stl", "11.stl", "14.stl", "23.stl", "27.stl"]    
    [
        [-0.7277, 0.15, 0.05, 0, 0, 0],
        [-0.1192, 0.0008, 0.075, 0, 0, 0], #8
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
 
global_sequence = [
    (2, "pick", "9.stl"),     
    (2, "place", "9.stl"), 

    (2, "pick", "12.stl"),     
    (2, "place", "12.stl"), 

    (2, "pick", "13.stl"),     
    (2, "place", "13.stl"), 

    (3, "pick", "10.stl"),     
    (3, "place", "10.stl"), 

    (3, "pick", "8.stl"),     
    (3, "place", "8.stl"), 
   
    (3, "pick", "11.stl"),     
    (3, "place", "11.stl"), 

    (3, "pick", "14.stl"),     
    (3, "place", "14.stl"), 

    (1, "pick", "2.stl"),     
    (1, "place", "2.stl"), 
    
    (1, "pick", "3.stl"),     
    (1, "place", "3.stl"), 

    (1, "pick", "4.stl"),     
    (1, "place", "4.stl"), 

    (1, "pick", "5.stl"),     
    (1, "place", "5.stl"), 

    (0, "pick", "7.stl"),     
    (0, "place", "7.stl"), 

    (1, "pick", "6.stl"),     
    (1, "place", "6.stl"), 

    (0, "pick", "7.stl"),     
    (0, "place", "7.stl"), 
    
    (0, "pick", "15.stl"),     
    (0, "place", "15.stl"), 

    (1, "pick", "16.stl"),     
    (1, "place", "16.stl"), 

    (0, "pick", "17.stl"),     
    (0, "place", "17.stl"), 

    (0, "pick", "18.stl"),     
    (0, "place", "18.stl"), 

    (0, "pick", "19.stl"),     
    (0, "place", "19.stl"), 

    (0, "pick", "20.stl"),     
    (0, "place", "20.stl"), 
    
    

]

max_phases = max(len(robot_targets) for robot_targets in targets)
approach_offset = 0.05
# ---------- Attach/place helpers (drop-in) ----------
def attach_mesh_to_ee(robot, mesh, height_offset=-0.03):
    # Remove mesh from environment if it's already there
    try:
        robot.env.remove(mesh)
    except Exception:
        pass

    # Compute relative transform from EE to mesh
    T_ee = robot.fkine(robot.q)
    T_rel = T_ee.inv() * mesh.T * sm.SE3(0, 0, height_offset)

    # Register as a child of the end effector
    ee_link = robot.links[-1]
    ee_link._children.append(mesh)
    mesh._parent = ee_link

    print(f"Attached {os.path.basename(mesh.filename)} to {robot.name}")
    return T_rel


def detach_mesh_from_ee(env, robot, mesh, place_pose=None):

    ee_link = robot.links[-1]
    if mesh in ee_link._children:
        ee_link._children.remove(mesh)

    mesh._parent = None  # Clear parent link

    # If a specific place pose is given, use it; otherwise, use robot's current EE pose
    if place_pose is not None:
        mesh.T = sm.SE3(*place_pose[:3]) * sm.SE3.RPY(*place_pose[3:], order="xyz")
    else:
        mesh.T = robot.fkine(robot.q)

    env.add(mesh)
    print(f" Detached {os.path.basename(mesh.filename)} from {robot.name}")

def check_hardware_estop():
    global hardware_estop_triggered
    while ser.in_waiting:  # read all available lines
        line = ser.readline().decode().strip()
        if line == "PRESSED":
            hardware_estop_triggered = True
            print("HARDWARE E-STOP ACTIVATED!")
        elif line == "RELEASED":
            # Optionally ignore, or reset manually later
            pass
    return hardware_estop_triggered

# ---------- State ----------
attached_meshes = [None] * len(robots)      
placing_scheduled = [False] * len(robots)  
place_pose_next = [None] * len(robots)
hardware_estop_triggered = False

# offsets
rot_offset = sm.SE3.Rx(np.pi)             
height_offset = -0.019                     
tol_pos = 0.01


# ---------- RMRC LOOP with alternating pick & place ----------
attached_meshes = [None] * len(robots) 

# ---------- GLOBAL SEQUENCE EXECUTION ----------
attached_meshes = [None] * len(robots)

for step_idx, (robot_idx, action, stl_name) in enumerate(global_sequence):
    robot = robots[robot_idx]
    robot_name = robot_name_map[robot]
    robot_targets = robot_stls[robot_name]

    print(f"\n--- Step {step_idx + 1}: {robot_name} {action} {stl_name} ---")

    stl_mesh = brick_meshes.get(stl_name)
    if stl_mesh is None:
        print(f"STL {stl_name} not found, skipping...")
        continue

    # find the correct target for this STL and action
    target_list = targets[robot_idx]
    robot_targets = robot_stls[robot_name]
    try:
        stl_index = robot_targets.index(stl_name)
    except ValueError:
        print(f"{stl_name} not assigned to {robot_name}, skipping.")
        continue

    # even index = pick, odd index = place
    target_idx = stl_index * 2 + (1 if action == "place" else 0)
    if target_idx >= len(target_list):
        print(f"No valid pose for {stl_name}.")
        continue

    pose_des = np.array(target_list[target_idx], dtype=float)

    # ---- RMRC motion for this single robot ----
    for step in range(max_steps):
        gui.render()
        if gui.estop_triggered or check_hardware_estop():
            print("Emergency Stop!")
            break

        q = robot.q.copy()
        pose_cur = fk_pose(robot)
        p_cur, rpy_cur = pose_cur[:3], pose_cur[3:]
        p_des, rpy_des = pose_des[:3], pose_des[3:]
        pos_error = p_des - p_cur
        R_cur = sm.base.rpy2r(*rpy_cur)
        R_des = sm.base.rpy2r(rpy_des)

        # Current and desired rotation matrices
        R_cur = robot.fkine(robot.q).R
        R_des = sm.base.rpy2r(*rpy_des)

        # Compute 3D rotation error
        rot_error = 0.5 * (np.cross(R_cur[:,0], R_des[:,0]) +
                        np.cross(R_cur[:,1], R_des[:,1]) +
                        np.cross(R_cur[:,2], R_des[:,2]))

        if np.linalg.norm(pos_error) < tol_pos:
            if action == "pick":
                T_rel = attach_mesh_to_ee(robot, stl_mesh, height_offset=-0.03)
                attached_meshes[robot_idx] = {"mesh": stl_mesh, "T_rel": T_rel}
                print(f" {robot_name} picked {stl_name}")
            elif action == "place":
                if attached_meshes[robot_idx] is not None:
                    entry = attached_meshes[robot_idx]
                    mesh = entry["mesh"]
                    detach_mesh_from_ee(env, robot, mesh, pose_des)
                    attached_meshes[robot_idx] = None
                    print(f"{robot_name} placed {stl_name}")
            break
        if check_self_collision(robot):
            print(f" {robot_name} in self-collision, stopping motion!")
            break


        # RMRC control law
        v_des = Kp * np.hstack((pos_error, rot_error))
        v_norm = np.linalg.norm(v_des[:3])
        if v_norm > vel_limit:
            v_des[:3] = (v_des[:3] / v_norm) * vel_limit

        J_full = np.array(robot.jacob0(q), dtype=float)
        λ = 0.2
        dq = J_full.T @ np.linalg.inv(J_full @ J_full.T + λ**2 * np.eye(6)) @ v_des
        q_next = clip_to_qlim(robot, q + dq * dt)
        robot.q = q_next
        T = robot.fkine(robot.q)

        # update attached mesh if holding
        if attached_meshes[robot_idx] is not None:
            entry = attached_meshes[robot_idx]
            entry["mesh"].T = robot.fkine(robot.q) * entry["T_rel"]

        env.step(dt)
        time.sleep(dt)

    # pause between steps for clarity
    time.sleep(1.5)
