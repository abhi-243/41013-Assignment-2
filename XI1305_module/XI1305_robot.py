import swift
import roboticstoolbox as rtb
import spatialmath.base as spb
import numpy as np
from spatialmath import SE3
from ir_support.robots.DHRobot3D import DHRobot3D
import time
import os

# Useful variables
from math import pi

class XI1305(DHRobot3D):
    def __init__(self):
        # DH links
        links = self._create_DH()

        # Names of the robot link files in the directory
        link3D_names = dict(link0 = 'Arm1', color0 = (0.2,0.2,0.2,1),      # color option only takes effect for stl file
                            link1 = 'Arm2', color1=(0.5,0,0,1),
                            link2 = 'Arm3',
                            link3 = 'Arm4',
                            link4 = 'Arm5',
                            link5 = 'Arm6',
                            link6 = 'XI1305_7')

        # A joint config and the 3D object transforms to match that config
        qtest = [0,0,0,0,0,0]
        qtest_transforms = [spb.transl(0,0,0),
                            spb.transl(0,0,0.146901),
                            spb.transl(0,0.062271,0.264968),
                            spb.transl(0.053091,0.044067 ,0.549595),
                            spb.transl(0.130547,-0.00214,0.387046),
                            spb.transl(0.1317,-0.014134,0.207184),
                            spb.transl(0.207821,0,0.143596)]
        #for i in range(len(qtest_transforms)):
            #qtest_transforms[i] = qtest_transforms[i] @ spb.trotx(pi/2)

        current_path = os.path.abspath(os.path.dirname(__file__))
        super().__init__(links, link3D_names, name = 'XI1305', link3d_dir = current_path, qtest = qtest, qtest_transforms = qtest_transforms)
        #self.base = self.base * SE3.Rx(pi/2)# * SE3.Ry(pi/2)
        self.q = qtest

    def _create_DH(self):
            """
            Create robot's standard DH model
            """
            links = [] 
            a = [0, 0.28948866, 0.0775, 0, 0.076, 0]
            d = [0.267, 0, 0, 0.3425, 0, 0.097]
            alpha = [-pi/2, 0, -pi/2, pi/2, -pi/2, 0]
            offset = [0, -1.3849179, 1.3849179, 0, 0, 0]
            qlim = [[-2*pi, 2*pi] for _ in range(6)]
            for i in range(6):
                link = rtb.RevoluteDH(d=d[i], a=a[i], alpha=alpha[i], offset=offset[i], qlim=qlim[i])
                links.append(link)
            return links
    
    def test(self):
        """
        Test the class by adding 3d objects into a new Swift window and do a simple movement
        """
        env = swift.Swift()
        env.launch(realtime= True)
        self.q = self._qtest
        self.add_to_env(env)
        fig = self.plot(self.q)
        input("delay")
        q_goal = [self.q[i]-pi/3 for i in range(self.n)]
        qtraj = rtb.jtraj(self.q, q_goal, 50).q
        
        for q in qtraj:
            self.q = q
            env.step(0.02)
            fig.step(0.01)
        time.sleep(3)
        env.hold()

# ---------------------------------------------------------------------------------------#
if __name__ == "__main__":
    r = XI1305()
    r.test()
