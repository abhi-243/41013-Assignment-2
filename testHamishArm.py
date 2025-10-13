from XI1305_module.XI1305_robot import XI1305  # ⬅️ Import your robot class

import swift
import time
from math import pi
import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import models, jtraj, trapezoidal
from spatialmath import SE3
from spatialmath.base import *

# Instantiate the robot
robot = XI1305()

# Launch a Swift window
env = swift.Swift()
env.launch(realtime=True)

# Add the robot
robot.add_to_env(env)
steps = 50

def moveArm(T): #moves the arm given a target transform matrix and a brick that is to be transported
    pose_offset = SE3(0,0,0.05)
    down_orientation = SE3.Rz(pi) * SE3.Rx(pi)
    target_pose = T*pose_offset*down_orientation
    q_guess = robot.q

    solution = robot.ikine_LM(target_pose,q0=q_guess,joint_limits=True)
    traj = rtb.jtraj(robot.q,solution.q,steps)

    q_guess = robot.q + np.random.uniform(-0.01, 0.01, size=len(robot.q))
    solution = robot.ikine_LM(target_pose,q0=q_guess,joint_limits=True)
    traj = rtb.jtraj(robot.q,solution.q,steps)

    for i,q in enumerate(traj.q):
        robot.q = q
        env.step(0.05)

# Test a movement
q_start = robot.q
q_end = [q - pi/4 for q in q_start]
q_end[0] = -0.8  # if using prismatic rail

#traj = rtb.jtraj(q_start, q_end, 50).q

#for q in traj:
#    robot.q = q
#    env.step(0.02)
while(True):
    T = transl(0.5,0.5,0)
    moveArm(T)
    T2 = transl(-0.2,-0.2,0)
    moveArm(T2) 

#env.hold()
