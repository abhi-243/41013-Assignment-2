##  @file
#   @brief Rough version of my own robot defined by standard static DH parameters with 3D model
#   @author Adam Scicluna
#   @date August 23, 2025

import swift
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3
from ir_support.robots.DHRobot3D import DHRobot3D
import time
import os
# Useful variables
from math import pi

# -----------------------------------------------------------------------------------#
class myRobot(DHRobot3D):
    def __init__(self):
        """
        Standard 6DOF Robot
        """
        # DH links
        links = self._create_DH()

        # Names of the robot link files in the directory
        link3D_names = dict(link0 = 'baseD',
                            link1 = 'link1D',
                            link2 = 'link2D',
                            link3 = 'link3D',
                            link4 = 'link4D',
                            link5 = 'link6D',
                            link6 = 'link6D'
                            )

        # A joint config and the 3D object transforms to match that config
        qtest = [0,-pi/2,0,0,0,0]
        qtest_transforms = [
            # Base link (link0) – no translation, rotate so Swift sees correct axis
            spb.transl(0, 0, 0) @ spb.rpy2tr(0, 0, 0, order='xyz'),

            # Link1
            spb.transl(0, 0, 0) @ spb.rpy2tr(0, 0, 0, order='xyz'),

            # Link2
            spb.transl(0, 0, 0) @ spb.rpy2tr(0, 0, 0, order='xyz'),

            # Link3
            spb.transl(0, 0, 0) @ spb.rpy2tr(0, 0, 0, order='xyz'),

            # Link4
            spb.transl(0, 0, 0) @ spb.rpy2tr(0, 0, 0, order='xyz'),

            # Link5
            spb.transl(0, 0, 0) @ spb.rpy2tr(0, 0, 0, order='xyz'),

            # Link6 (end-effector)
            spb.transl(0, 0, 0) @ spb.rpy2tr(0, 0, 0, order='xyz')
        ]


        dae_path = os.path.abspath(os.path.dirname(__file__))
        super().__init__(links, link3D_names, name = 'myRobot', link3d_dir = dae_path, 
                         qtest = qtest, qtest_transforms = qtest_transforms)
        self.base = self.base * SE3.Rx(pi/2) * SE3.Ry(pi/2)
        self.q = qtest

    # -----------------------------------------------------------------------------------#
    def _create_DH(self):
        """
        Create robot's standard DH model.
        Easy to edit: each joint's parameters are in one place.
        """
        dh_params = [
            (0.146,   0,       pi/2,   0,           [-pi, pi]),        # Joint 1
            (0,      -0.24365, 0,      0,           [-pi/2, pi/2]),    # Joint 2
            (0,      -0.21325, 0,      0,           [0, pi]),          # Joint 3
            (0.121,   0,       pi/2,   0,           [-2*pi, 2*pi]),    # Joint 4
            (0.083,   0,      -pi/2,   0,           [-pi/2, pi/2]),    # Joint 5
            (0.0819,  0,       0,      0,           [-pi, pi])         # Joint 6
        ]

        links = []
        for (d, a, alpha, offset, qlim) in dh_params:
            link = rtb.RevoluteDH(d=d, a=a, alpha=alpha,
                                  offset=offset, qlim=qlim)
            links.append(link)
        return links


    # -----------------------------------------------------------------------------------#
    def test(self):
        """
        Test the class by adding 3d objects into a new Swift window and do a simple movement
        """
        env = swift.Swift()
        env.launch(realtime= True)
        self.q = self._qtest
        self.add_to_env(env)

        q_goal = [self.q[i]-pi/3 for i in range(self.n)]
        q_goal[0] = -0.8 # Move the rail link
        qtraj = rtb.jtraj(self.q, q_goal, 50).q
        # fig = self.plot(self.q, limits= [-1,1,-1,1,-1,1])
        # fig._add_teach_panel(self, self.q)
        for q in qtraj:
            self.q = q
            env.step(0.02)
            # fig.step(0.01)
        # fig.hold()
        env.hold()
        time.sleep(3)
    
    def test_static(self):
        """
        Test the class by adding 3D objects into a new Swift window without movement
        """
        env = swift.Swift()
        env.launch(realtime=True)
        self.q = self._qtest
        self.add_to_env(env)

        # Keep the window open with the robot in its initial pose
        env.hold()
        time.sleep(3)


# ---------------------------------------------------------------------------------------#
if __name__ == "__main__":
    r = myRobot()
    input("Press enter to test movement of myRobot")
    r.test()
    #r.test_static()