import swift
import spatialgeometry as sg
import spatialmath as sm
import spatialmath.base as smb
import numpy as np
import time
from math import pi
from IRB120 import IRB120

# === Initialize Swift Environment ===
env = swift.Swift()
env.launch(realtime=True)
env.step(0.1)

# === Initialize IRB120 Robot ===
robot = IRB120()
robot.base = sm.SE3(0, 0, 0.05) * sm.SE3.RPY(-np.pi/2, 0, 0, order='xyz')
robot.q = np.zeros(robot.n)
robot.add_to_env(env)
env.step(0.1)

print("IRB120 robot added to Swift environment.")

# === RMRC Function ===
def rmrc(robot, env, target_pose, steps=150, gain=0.3, dt=0.05):
    """
    Perform Resolved Motion Rate Control (Cartesian velocity control)
    to move robot end-effector smoothly to a target pose.
 
    robot: Robot instance
    env: Swift environment
    target_pose: spatialmath.SE3 target pose
    steps: number of interpolation steps
    gain: proportional gain
    dt: time step (s)
    """
    q = robot.q
    for i in range(steps):
        T_current = robot.fkine(q)
        delta_x = smb.tr2delta(T_current.A, target_pose.A)  # 6D twist error
        J = robot.jacobe(q)

        # Damped least-squares inverse to avoid singularities
        λ2 = 0.01
        dq = gain * J.T @ np.linalg.inv(J @ J.T + λ2 * np.eye(6)) @ delta_x

        q = q + dq * dt
        robot.q = q
        env.step(dt)

# === Define RMRC Waypoints ===
waypoints = [
    sm.SE3(0.4, 0.2, 0.2) * sm.SE3.RPY(0, np.pi/2, 0, order='xyz'),
    sm.SE3(0.5, -0.2, 0.25) * sm.SE3.RPY(0, np.pi/2, np.pi/2, order='xyz'),
    sm.SE3(0.6, 0.0, 0.3) * sm.SE3.RPY(0, np.pi/2, np.pi, order='xyz'),
    sm.SE3(0.4, 0.2, 0.35) * sm.SE3.RPY(0, np.pi/2, -np.pi/2, order='xyz')
]

# === Visualize target points ===
for wp in waypoints:
    env.add(sg.Sphere(0.01, color=(1, 0, 0), pose=wp))

# === Execute RMRC Motions ===
for i, target in enumerate(waypoints):
    print(f"\n→ Moving to waypoint {i + 1}/{len(waypoints)}")
    rmrc(robot, env, target, steps=200, gain=0.9, dt=0.07)
    time.sleep(0.3)

print("\nAll RMRC movements complete.")
input("Press Enter to close Swift...")