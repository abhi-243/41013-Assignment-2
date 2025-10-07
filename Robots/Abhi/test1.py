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

class IRB120(DHRobot3D):
    def __init__(self):
        # DH links
        links = self._create_DH()

        # Names of the robot link files in the directory
        link3D_names = dict(link0 = 'link0', color0 = (0.2,0.2,0.2,1),      # color option only takes effect for stl file
                            link1 = 'link1', color1=(0.5,0,0,1),
                            link2 = 'link2',
                            link3 = 'link3',
                            link4 = 'link4',
                            link5 = 'link5',
                            link6 = 'link6')

        # A joint config and the 3D object transforms to match that config
        qtest = [0,0,0,0,0,0]
        qtest_transforms = [spb.transl(0,0,0),
                            spb.transl(0,0,0.166) @ spb.trotz(np.pi),
                            spb.transl(0,0,0.290) @ spb.trotz(np.pi),
                            spb.transl(0,-0.0095,0.560),
                            spb.transl(-0.1496,0,0.630),
                            spb.transl(-0.302,0,0.630) @ spb.trotx(np.pi/2),
                            spb.transl(-0.3614,0,0.630),]

        current_path = os.path.abspath(os.path.dirname(__file__))
        super().__init__(links, link3D_names, name = 'IRB120', link3d_dir = current_path, qtest = qtest, qtest_transforms = qtest_transforms)
        #self.base = self.base * SE3.Rx(pi/2) * SE3.Ry(pi/2)
        self.q = qtest

    def _create_DH(self):
            """
            Create robot's standard DH model
            """
            links = [] 
            a = [0, 0.270, 0.070, 0, 0, 0]
            d = [0.290, 0, 0, 0.302, 0, 0.072]
            alpha = [-np.pi/2, 0, -np.pi/2, np.pi/2, -np.pi/2, 0]
            offset = [0, -pi/2, 0, 0, 0,0]
            qlim = [[-np.pi, np.pi] for _ in range(6)]
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
            self.q = [-qi for qi in q]
            env.step(0.02)
            fig.step(0.01)
        time.sleep(3)
        # env.hold()

# ---------------------------------------------------------------------------------------#
if __name__ == "__main__":
    r = IRB120()
    r.test()
    input("press enter to quit")