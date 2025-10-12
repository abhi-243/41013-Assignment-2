import swift
from IRB120 import IRB120
import numpy as np
from time import sleep

# Initialize Swift server
env = swift.Swift()
env.launch(realtime=True)

# Create robot
robot = IRB120()
robot.add_to_env(env)  # adds robot to Swift

# Step once to display initial pose
env.step()
sleep(1)

# Move all joints by pi/3
q_move = np.array([np.pi/3] * 6)

# Animate the motion gradually so Swift updates
steps = 50
q_start = robot.q.copy()
for alpha in np.linspace(0, 1, steps):
    robot.q = q_start + alpha * (q_move - q_start)
    env.step(0.02)  # update Swift with small delay

input("Press Enter to exit...")