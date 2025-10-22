from IRB120.IRB120 import IRB120
from myCobot320m5.milan import myCobot
from XI1305_module.XI1305_robot import XI1305
from Environment_Meshes.test import stl_data
from teach_pendant import TeachPendant
from ir_support import UR3, EllipsoidRobot
from itertools import chain
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

ellipsoids_robot1 = EllipsoidRobot(IRB120_Abhi, default_height=0.05, default_width=0.05)
ellipsoids_robot2 = EllipsoidRobot(UR3_Given, default_height=0.05, default_width=0.05)
ellipsoids_robot3 = EllipsoidRobot(myCobot320m5, default_height=0.05, default_width=0.05)
ellipsoids_robot4 = EllipsoidRobot(XI1305_Hamish, default_height=0.05, default_width=0.05)

ellipsoids_robot1.ellipsoid_for_robot_links(IRB120_Abhi.q)
#ellipsoids_robot1.plot_ellipsoids()
ellipsoids_robot2.ellipsoid_for_robot_links(UR3_Given.q)
#ellipsoids_robot2.plot_ellipsoids()
ellipsoids_robot3.ellipsoid_for_robot_links(myCobot320m5.q)
#ellipsoids_robot3.plot_ellipsoids()
ellipsoids_robot4.ellipsoid_for_robot_links(XI1305_Hamish.q)
#ellipsoids_robot4.plot_ellipsoids()

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
for robot in [IRB120_Abhi, UR3_Given, myCobot320m5, XI1305_Hamish]:
    for link in robot.links:
        if link.collision is None:
            # Assign the visual mesh as collision mesh
            link.collision = link.visual

# === Load environment mesh ===
env_mesh = sg.Mesh(filename=env_mesh_path)
env_mesh.color = (0.6, 0.6, 0.6)
env_mesh.T = sm.SE3(0, 0, 0)
env.add(env_mesh)
env_objects = [env_mesh]  # include main environment
print("Collision objects:")
for o in env_objects:
    print(type(o))

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
            
            mesh.is_brick = True  # <-- mark it as a brick
            
            env.add(mesh)
            env.step(0.01)  # Step after each addition
            print(f"Loaded {file} → Pos: {pos}, Rot: {rpy}, Color: {mesh.color}")

            # Add brick mesh to collision objects list
            env_objects.append(mesh)
            
        except Exception as e:
            print(f"Failed to load {file}: {e}")
            
brick_points_list = []
for mesh in env_objects:
    # Only bricks (skip main environment)
    if getattr(mesh, "is_brick", False):
        points = mesh.v  # or sample points
        brick_points_list.append(points)

# Start all robots from zero
q_zero = np.zeros(IRB120_Abhi.n)
IRB120_Abhi.q = q_zero
UR3_Given.q = q_zero
myCobot320m5.q = q_zero
XI1305_Hamish.q = q_zero
env.step(0.1)

def check_robot_collision(robot_ellipsoid, other_ellipsoids):
    for other in other_ellipsoids:
        if other == robot_ellipsoid:
            continue
        for i1 in range(len(robot_ellipsoid.ellipsoid_matrices)):
            T1, r1 = robot_ellipsoid.get_ellipsoid_transform_and_radii(i1)
            for i2 in range(len(other.ellipsoid_matrices)):
                T2, r2 = other.get_ellipsoid_transform_and_radii(i2)
                dist = np.linalg.norm(T1 - T2)  # <-- fixed here
                if dist < (np.linalg.norm(r1) + np.linalg.norm(r2)):
                    return True
    return False

def get_link_meshes(link):
    """
    Recursively extract all Mesh objects from a link's collision object.
    Works for Mesh or SceneGroup (any depth).
    """
    meshes = []

    if link.collision is None:
        return meshes

    if isinstance(link.collision, sg.Mesh):
        meshes.append(link.collision)
    elif isinstance(link.collision, sg.SceneGroup):
        try:
            # Iterate over SceneGroup items
            for obj in link.collision:
                if isinstance(obj, sg.Mesh):
                    meshes.append(obj)
                elif isinstance(obj, sg.SceneGroup):
                    # Recursive call
                    link_dummy = type('LinkDummy', (), {'collision': obj})()
                    meshes.extend(get_link_meshes(link_dummy))
        except TypeError:
            # Fallback for SceneGroup not directly iterable
            pass

    return meshes

def check_ellipsoid_collision(robot_ellipsoid, env_objects, brick_points_list):
    """
    Returns (collision_detected: bool, colliding_brick_index: int or None)
    """
    # Check bricks
    for idx, points in enumerate(brick_points_list):
        for ellipsoid_info in robot_ellipsoid.ellipsoid_matrices:
            T = ellipsoid_info['center']
            shape_matrix = ellipsoid_info['matrix']

            # Compute radii from shape matrix
            eigvals, _ = np.linalg.eigh(shape_matrix)
            radii = np.sqrt(eigvals)

            # Transform points to ellipsoid local frame
            points_local = (np.linalg.inv(np.vstack((
                                np.hstack((np.eye(3), T.reshape(3,1))),
                                np.array([0,0,0,1])
                              ))) @ np.hstack((points, np.ones((points.shape[0],1))).T))[:3,:].T
            dist = np.sum((points_local / radii)**2, axis=1)
            if np.any(dist < 1.0):
                return True, idx  # collision with this brick

    # Check environment meshes (coarse check: center distance)
    for ellipsoid_info in robot_ellipsoid.ellipsoid_matrices:
        link_center = ellipsoid_info['center']
        shape_matrix = ellipsoid_info['matrix']
        eigvals, _ = np.linalg.eigh(shape_matrix)
        radii = np.sqrt(eigvals)

        for obj in env_objects:
            if hasattr(obj, "T"):
                obj_center = np.array(sm.SE3(obj.T).t).flatten()
                if np.linalg.norm(link_center - obj_center) < np.max(radii):
                    return True, None  # collision with environment

    return False, None

# === Repulsive velocity for collision avoidance ===
def repulsive_velocity(robot, env_objects, eta=0.5, threshold=0.5):
    """
    Compute a repulsive velocity for all robot links against environment objects.
    """
    avoidance = np.zeros(3)

    # Get all robot link meshes
    robot_meshes = []
    for link in robot.links:
        robot_meshes.extend(get_link_meshes(link))

    for link_mesh in robot_meshes:
        try:
            link_pos = np.array(sm.SE3(link_mesh.T).t).flatten()
        except Exception:
            continue

        for obj in env_objects:
            if not hasattr(obj, 'T'):
                continue
            try:
                obj_pos = np.array(sm.SE3(obj.T).t).flatten()
            except Exception:
                continue

            vec = link_pos - obj_pos
            dist = np.linalg.norm(vec)
            if dist < threshold and dist > 1e-6:
                avoidance += eta * (1.0/dist - 1.0/threshold) * (vec/dist**3)

    return avoidance

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
ellipsoids = [ellipsoids_robot1, ellipsoids_robot2, ellipsoids_robot3, ellipsoids_robot4]

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

        # --- Update all ellipsoids with current robot configurations ---
        for robot, ellipsoid in zip(robots, ellipsoids):
            ellipsoid.ellipsoid_for_robot_links(robot.q)

        for i, robot in enumerate(robots):
            q = robot.q.copy()
            p_cur = fk_position(robot)
            p_des = p_des_all[i]

            error = p_des - p_cur
            err_norm = np.linalg.norm(error)

            if err_norm < 5e-3:
                continue
            all_reached = False

            # --- Desired velocity with repulsive effect ---
            v_des = Kp * error + repulsive_velocity(robot, env_objects)

            # Limit velocity
            v_norm = np.linalg.norm(v_des)
            if v_norm > vel_limit:
                v_des = (v_des / v_norm) * vel_limit

            # --- RMRC ---
            Jv = linear_jacobian(robot, q)
            dq = np.linalg.pinv(Jv).dot(v_des)
            q_next = clip_to_qlim(robot, q + dq * dt)

            # --- Collision Checks ---
            env_collision, brick_idx = check_ellipsoid_collision(ellipsoids[i], env_objects, brick_points_list)
            robot_collision = check_robot_collision(ellipsoids[i], [e for j,e in enumerate(ellipsoids) if j != i])

            if env_collision or robot_collision:
                q_next = q  # hold position
                if brick_idx is not None:
                    print(f"Robot {i} colliding with brick {brick_idx}")


            robot.q = q_next

        env.step(dt)
        time.sleep(dt)

        if all_reached:
            break

print("\n✅ RMRC with ellipsoid collision demo complete.")
input("Press Enter to exit...")