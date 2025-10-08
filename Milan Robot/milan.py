import swift
import roboticstoolbox as rtb
import spatialmath.base as spb
import numpy as np
from spatialmath import SE3
from ir_support.robots.DHRobot3D import DHRobot3D
import time
import os

from math import pi

class myCobot(DHRobot3D):
    def __init__(self):
        # DH links
        links = self._create_DH()

        # Names of the robot link files in the directory
        link3D_names = dict(
            link0='myCobotLink_1', color0=(0.2,0.2,0.2,1),
            link1='myCobotLink_1.1', color1=(0.5,0,0,1),
            link2='myCobotLink_3.2', 
            link3='myCobotLink_4.1',
            link4='myCobotLink_5.1',
            link5='myCobotLink_6.1',
            link6='myCobotAttach'
        )

        # A joint config and the 3D object transforms to match that config
        qtest = [0,0,0,0,0,0]

        # Small offsets to align STL links visually with joint axes
        qtest_transforms = [
            spb.transl(0,0,0)@ spb.r2t(spb.rotz(3/2*pi)),
            spb.transl(0, 0, 0) @ spb.r2t(spb.rotz(pi)),  # adjust link2 to stay connected
            spb.transl(0,0,0)@ spb.r2t(spb.rotz(3/2*pi)),
            spb.transl(0,0,0)@ spb.r2t(spb.rotz(3/2*pi)),
            spb.transl(0,0,0)@ spb.r2t(spb.rotz(3/2*pi)),
            spb.transl(0,0,0)@ spb.r2t(spb.rotz(3/2*pi)),
            spb.transl(0,0,0)@ spb.r2t(spb.rotz(3/2*pi))
        ]

        current_path = os.path.abspath(os.path.dirname(__file__))
        link3d_dir = os.path.join(current_path, "robotlinkstl")
        super().__init__(
            links, link3D_names, name='myCobot',
            link3d_dir=link3d_dir, qtest=qtest,
            qtest_transforms=qtest_transforms
        )

        self.q = qtest

    def _create_DH(self):
        """
        Create robot's DH model.
        Joint 2 rotates left-right (vertical axis).
        """

        links = []
        a = [0, 0.4, 0.120, 0, 0, 0]
        d = [0.68, 0, 0, 0.09878, 0.095, 0.0655]
        alpha = [pi/2, 0, 0, pi/2, -pi/2, -pi]
        offset = [0,pi/2, 0, pi/2, pi, -pi/2]

        qlim = [[-pi/2, pi/2] for _ in range(6)]
        for i in range(6):
            link = rtb.RevoluteDH(d=d[i], a=a[i], alpha=alpha[i], offset=offset[i], qlim=qlim[i])
            links.append(link)
        return links


def test(self):
    """Add robot to Swift and show default pose"""
    self.q = [0, 0, 0, 0, 0, 0]
    self.add_to_env(env)
    self.plot(self.q)
    time.sleep(1)


if __name__ == "__main__":
    env = swift.Swift()
    env.launch(realtime=True)

    r = myCobot()
    r.add_to_env(env)
    r.q = [0, 0, 0, 0, 0, 0]
    r.plot(r.q)




    # Helper function to rotate one joint back and forth
    def test_joint(robot, joint_index, angle_range=np.linspace(-pi/2, pi/2, 40), delay=0.05):
        q = robot.q.copy()
        print(f"\n--- Testing joint {joint_index+1} ---")
        for angle in angle_range:
            q[joint_index] = angle
            robot.q = q
            env.step(delay)
        for angle in reversed(angle_range):
            q[joint_index] = angle
            robot.q = q
            env.step(delay)


    # Sequentially test all joints
    for i in range(r.n):
        input(f"\nPress Enter to test joint {i+1}...")
        test_joint(r, i)

    print("\n✅ Joint rotation test complete!")



    
