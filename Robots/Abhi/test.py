##  @file
#   @brief 1-DOF robot test with frames and stick
#   @author Adam Scicluna
#   @date August 23, 2025

import swift
import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3
from ir_support.robots.DHRobot3D import DHRobot3D
import time
import os
from math import pi

class myRobot(DHRobot3D):
    def __init__(self):
        """
        1-DOF robot with axis visualization and a 1m stick attached.
        """
        # DH links
        links = self._create_DH()

        # Names of 3D links
        link3D_names = dict(
            link0='baseD',
            link1='link1D'
        )

        # Joint configuration
        qtest = [0]

        # Base transforms (no mesh rotation needed, Swift frame will show axes)
        base_transform = spb.transl(0, 0, 0)
        joint_transform = spb.transl(0, 0, 0)

        qtest_transforms = [
            base_transform,
            joint_transform
        ]

        dae_path = os.path.abspath(os.path.dirname(__file__))

        super().__init__(
            links,
            link3D_names,
            name='myRobot',
            link3d_dir=dae_path,
            qtest=qtest,
            qtest_transforms=qtest_transforms
        )

        self.base = self.base * SE3.Rx(pi/2) * SE3.Ry(pi/2)
        self.q = qtest

    # ---------------------- DH ----------------------#
    def _create_DH(self):
        dh_params = [
            (0.146, 0, pi/2, 0, [-pi, pi])  # Only 1 joint
        ]
        links = []
        for (d, a, alpha, offset, qlim) in dh_params:
            links.append(rtb.RevoluteDH(d=d, a=a, alpha=alpha, offset=offset, qlim=qlim))
        return links

    # ---------------------- Test movement ----------------------#
    def test(self):
        """
        Rotate joint 90° and visualize frames with a stick.
        """
        env = swift.Swift()
        env.launch(realtime=True)
        self.q = [0]
        
        # Add the robot with frames visible
        self.add_to_env(env )

        # Attach a 1m stick along X of joint 1
        stick_length = 1.0
        stick_trans = SE3(stick_length/2, 0, 0)  # center of stick at joint axis
        env.add_box(length=stick_length, width=0.05, height=0.05, pose=stick_trans, color=(1,0,0))

        # Initial FK
        print("Initial end of stick position:", self.fkine(self.q) * SE3(stick_length,0,0))

        # Rotate 90 degrees
        q_goal = [pi/2]
        qtraj = rtb.jtraj(self.q, q_goal, 50).q

        for q in qtraj:
            self.q = q
            env.step(0.02)

        
        # Final FK
        print("Final end of stick position:", self.fkine(q_goal) * SE3(stick_length,0,0))

        env.hold()
        time.sleep(5)

    def test_static(self):
        """
        Static visualization with frames
        """
        env = swift.Swift()
        env.launch(realtime=True)
        self.q = [0]
        self.add_to_env(env, frame=True)
        env.hold()
        time.sleep(3)


# ---------------------- Main ----------------------#
if __name__ == "__main__":
    r = myRobot()
    input("Press enter to test movement of myRobot")
    r.test()
    input("Press Enter to exit...")