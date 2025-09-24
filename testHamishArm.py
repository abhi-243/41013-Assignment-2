from XI1305_module.XI1305_robot import XI1305  # ⬅️ Import your robot class

import swift
import time
from math import pi
import numpy as np
import roboticstoolbox as rtb

# Instantiate the robot
robot = XI1305()

# Launch a Swift window
env = swift.Swift()
env.launch(realtime=True)

# Add the robot
robot.add_to_env(env)

# Test a movement
q_start = robot.q
q_end = [q - pi/4 for q in q_start]
q_end[0] = -0.8  # if using prismatic rail

traj = rtb.jtraj(q_start, q_end, 50).q

for q in traj:
    robot.q = q
    env.step(0.02)

env.hold()