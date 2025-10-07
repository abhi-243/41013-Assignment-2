import swift
import roboticstoolbox as rtb
import spatialmath.base as spb
import numpy as np
from spatialmath import SE3
from ir_support.robots.DHRobot3D import DHRobot3D
import time
import os
from math import pi

class IRB120(DHRobot3D):
    def __init__(self):
        links = self._create_DH()

        link3D_names = dict(
            link0='link0', color0=(0.2,0.2,0.2,1),
            link1='link1', color1=(0.5,0,0,1),
            link2='link2',
            link3='link3',
            link4='link4',
            link5='link5',
            link6='link6'
        )

        qtest = [0, 0, 0, 0, 0, 0]
        qtest_transforms = [
            spb.transl(0,0,0),
            spb.transl(0,0,0.166) @ spb.trotz(np.pi),
            spb.transl(0,0,0.290) @ spb.trotz(np.pi),
            spb.transl(0,-0.0095,0.560),
            spb.transl(-0.1496,0,0.630),
            spb.transl(-0.302,0,0.630),
            spb.transl(-0.3614,0,0.630)
        ]

        current_path = os.path.abspath(os.path.dirname(__file__))
        super().__init__(
            links, link3D_names, name='IRB120',
            link3d_dir=current_path,
            qtest=qtest, qtest_transforms=qtest_transforms
        )
        self.q = qtest

    def _create_DH(self):
        a = [0, 0.270, 0.070, 0, 0, 0]
        d = [0.290, 0, 0, 0.302, 0, 0.072]
        alpha = [-np.pi/2, 0, -np.pi/2, np.pi/2, -np.pi/2, 0]
        offset = [0, -pi/2, 0, 0, 0, 0]
        qlim = [[-np.pi, np.pi] for _ in range(6)]

        links = [rtb.RevoluteDH(d=d[i], a=a[i], alpha=alpha[i],
                                offset=offset[i], qlim=qlim[i]) for i in range(6)]
        return links

    # ----------------------------------------------------------------------------------
    def test(self, env=None, fig=None):
        """
        Test full trajectory in both Swift and Matplotlib plot
        """
        print("\nRunning trajectory test...")
        if env is None:
            env = swift.Swift()
            env.launch(realtime=True)
            self.add_to_env(env)

        if fig is None:
            fig = self.plot(self.q, block=False)

        q_goal = [self.q[i] - pi/3 for i in range(self.n)]
        qtraj = rtb.jtraj(self.q, q_goal, 50).q

        for q in qtraj:
            self.q = q
            env.step(0.02)
            fig.step(0.02)

        print("Trajectory test complete.")

    # ----------------------------------------------------------------------------------
    def test_joint(self, env, fig, joint_index=None, delay=0.005, steps=50):
        """
        Test one or all joints over their full limits, synchronized with plot.
        """
        if joint_index is None:
            joints_to_test = range(self.n)
        else:
            joints_to_test = [joint_index]

        for j in joints_to_test:
            qmin, qmax = self.links[j].qlim
            print(f"\n--- Testing joint {j+1} from {qmin:.2f} to {qmax:.2f} ---")

            self.q = [0] * self.n
            env.step(0.1)
            fig.step(0.1)
            q = self.q.copy()

            # Sweep forward
            for angle in np.linspace(qmin, qmax, steps):
                q[j] = angle
                self.q = q
                env.step(delay)
                fig.step(delay)

            # Sweep backward
            for angle in np.linspace(qmax, qmin, steps):
                q[j] = angle
                self.q = q
                env.step(delay)
                fig.step(delay)

        print("\nJoint rotation test complete.")

# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    r = IRB120()

    # Launch one Swift env and one plot
    env = swift.Swift()
    env.launch(realtime=True)
    r.add_to_env(env)
    fig = r.plot(r.q, block=False)

    while True:
        print("\n-----------------------------------------")
        print("Select test mode:")
        print("1. Run trajectory test (all joints move together)")
        print("2. Test one joint")
        print("3. Test all joints")
        print("4. Exit")
        print("-----------------------------------------")

        choice = input("Select (1/2/3/4): ").strip()

        if choice == "1":
            r.test(env=env, fig=fig)
        elif choice == "2":
            j = int(input("Enter joint number (1-6): ")) - 1
            r.test_joint(env=env, fig=fig, joint_index=j)
        elif choice == "3":
            r.test_joint(env=env, fig=fig, joint_index=None)
        elif choice == "4":
            print("\nExiting program.")
            break
        else:
            print("Invalid choice, please try again.")