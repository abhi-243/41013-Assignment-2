import time
import numpy as np
from roboticstoolbox.robot.Robot import Robot

class AbhiRobot(Robot):
    def __init__(self):
        urdf_path = r"C:\Users\abhin\OneDrive\Documents\UTS\Spring Semester 2025\41013 Industrial Robotics\Assignments\A2\41013-Assignment-2\Robots\Abhi\abhi.urdf.xml"
        links, name, urdf_string, urdf_filepath = self.URDF_read(urdf_path)

        super().__init__(
            links,
            name=name,
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )

        self.qz = np.zeros(self.n)
        self.addconfiguration("qz", self.qz)

    def test_sweep(self, env, steps=50, delay=0.05):
        """
        Sweeps each joint individually across its joint limits.
        Skips fixed joints automatically.
        """
        for i in range(self.n):
            # Skip joint if qlim is None or degenerate
            if self.qlim is None or i >= len(self.qlim):
                continue
            q_limits = self.qlim[i]
            if q_limits is None or np.allclose(q_limits[0], q_limits[1]):
                print(f"Skipping joint {i} ({self.links[i+1].name}): fixed or no limits")
                continue

            q_start, q_end = q_limits
            print(f"Sweeping joint {i} ({self.links[i+1].name}) from {q_start} to {q_end}")

            for q_val in np.linspace(q_start, q_end, steps):
                self.q[i] = q_val
                env.step(0.01)
                time.sleep(delay)

            # Return joint to zero
            self.q[i] = 0
            env.step(0.01)
            time.sleep(delay)

if __name__ == "__main__":
    import swift
    env = swift.Swift()
    env.launch()

    robot = AbhiRobot()
    env.add(robot)
    robot.q = robot.qz

    input("Press Enter to start joint sweep test...")
    robot.test_sweep(env)

    input("Press Enter to exit...")