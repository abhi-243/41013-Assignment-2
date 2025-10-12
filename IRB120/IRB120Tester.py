from IRB120 import IRB120
import swift
import roboticstoolbox as rtb
from spatialmath import SE3
import numpy as np
import logging
from math import pi

# Configure logging (can be overridden by calling script)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# =====================================================================
# Robot Tester
# =====================================================================
class IRB120Tester:
    """Provides test routines for the ABB IRB120 robot."""

    def __init__(self, robot: IRB120):
        self.robot = robot
        self.env = None
        self.fig = None

    # -----------------------------------------------------------------
    def initialize(self, use_swift=True):
        """Initialize Swift environment and matplotlib plot."""
        if use_swift:
            self.env = swift.Swift()
            self.env.launch(realtime=True)
            self.robot.env = self.env  # <-- store env in the robot
            self.robot.add_to_env(self.env)

        #self.fig = self.robot.plot(self.robot.q, block=False)
        log.info("Visualization initialized.")


    # -----------------------------------------------------------------
    def trajectory_test(self, steps=50, delay=0.02):
        """Move all joints together along a trajectory."""
        log.info("Running trajectory test...")
        q_goal = np.array(self.robot.q) - pi/3
        qtraj = rtb.jtraj(self.robot.q, q_goal, steps).q

        for q in qtraj:
            self.robot.q = q
            if self.env:
                self.env.step(delay)
            if self.fig:
                self.fig.step(delay)

        log.info("Trajectory test complete.")

    # -----------------------------------------------------------------
    def joint_test(self, joint_index=None, delay=0.005, steps=50):
        """Test rotation of one or all joints."""
        joints = range(self.robot.n) if joint_index is None else [joint_index]

        for j in joints:
            qmin, qmax = self.robot.links[j].qlim
            log.info(f"Testing joint {j+1}: 0 → {qmax:.2f} → 0 → {qmin:.2f} → 0")
            q = [0] * self.robot.n
            self.robot.q = q
            if self.env: self.env.step(0.1)
            if self.fig: self.fig.step(0.1)

            # Motion sequence
            sequences = [
                np.linspace(0, qmax, steps),
                np.linspace(qmax, 0, steps),
                np.linspace(0, qmin, steps),
                np.linspace(qmin, 0, steps)
            ]

            for seq in sequences:
                for angle in seq:
                    q[j] = angle
                    self.robot.q = q
                    if self.env: self.env.step(delay)
                    if self.fig: self.fig.step(delay)

        log.info("Joint rotation test complete.")
        
    def move_to_pose(self, target_pose, steps=50, delay=0.02):
        """Move robot from current pose to target SE3 pose."""
        q_target = self.robot.ik(target_pose)
        if q_target is None:
            log.warning("IK failed for target pose.")
            return
        qtraj = rtb.jtraj(self.robot.q, q_target, steps).q
        for q in qtraj:
            self.robot.q = q
            if self.env: self.env.step(delay)
            if self.fig: self.fig.step(delay)
        log.info("Move-to-pose complete.")
        
    def reset(self):
        """Reset robot to home and clear Swift scene."""
        if self.env:
            self.env.reset()
            self.robot.add_to_env(self.env)
        self.robot.home()
        log.info("Environment reset and robot homed.")
        
    def ik_trajectory_test(self, method='jtraj', steps=75, delay=0.02):
        """
        Full pick-and-place inverse kinematics test.

        Motion sequence:
            Home (0) → Pick → Place → Home (0)

        Parameters
        ----------
        method : str
            One of {'jtraj', 'ctraj', 'mstraj'}
        steps : int
            Number of interpolation steps per segment
        delay : float
            Delay between frames for Swift animation
        """
        log.info(f"Starting IK trajectory test using method='{method}'...")

        # -----------------------------
        # Define poses
        # -----------------------------
        T_home  = self.robot.fkine(np.zeros(self.robot.n))
        T_pick  = SE3(0,  0.45, 0.15) * SE3.RPY(0, 0, 0, order='xyz')
        T_place = SE3(0, -0.45, 0.15) * SE3.RPY(0, 0, 0, order='xyz')

        # Compute IK for all key poses
        q_home  = np.zeros(self.robot.n)
        q_pick  = self.robot.ik(T_pick, q0=q_home)
        q_place = self.robot.ik(T_place, q0=q_home)

        if q_pick is None or q_place is None:
            log.warning("IK failed for one or both target poses.")
            return

        # -----------------------------
        # Ensure environment exists
        # -----------------------------
        if not self.env:
            self.env = swift.Swift()
            self.env.launch(realtime=True)
            self.robot.env = self.env
            self.robot.add_to_env(self.env)

        # Helper for joint motion animation
        def animate(q_sequence):
            for q in q_sequence:
                self.robot.q = q
                if self.env:
                    self.env.step(delay)
                if self.fig:
                    self.fig.step(delay)

        # -----------------------------
        # Trajectory selection
        # -----------------------------
        if method.lower() == 'jtraj':
            # Joint-space motion for each phase
            traj1 = rtb.jtraj(q_home,  q_pick,  steps).q
            traj2 = rtb.jtraj(q_pick,  q_place, steps).q
            traj3 = rtb.jtraj(q_place, q_home,  steps).q
            q_full = np.vstack((traj1, traj2, traj3))

        elif method.lower() == 'ctraj':
            # Cartesian linear motion (IK per step)
            T_traj1 = rtb.ctraj(T_home,  T_pick,  steps)
            T_traj2 = rtb.ctraj(T_pick,  T_place, steps)
            T_traj3 = rtb.ctraj(T_place, T_home,  steps)
            q_full = []
            for T in list(T_traj1) + list(T_traj2) + list(T_traj3):
                q = self.robot.ik(T)
                if q is not None:
                    q_full.append(q)
            if not q_full:
                log.warning("CTRAJ failed to generate valid path.")
                return

        elif method.lower() == 'mstraj':
            # Multi-segment joint trajectory (with lift phase)
            q_lift = np.copy(q_pick)
            q_lift[2] -= 0.2  # small upward motion before moving laterally
            path1 = np.vstack((q_home, q_pick))
            path2 = np.vstack((q_pick, q_lift, q_place))
            path3 = np.vstack((q_place, q_home))

            tsegment = [1.0, 2.0]
            tacc = 0.3

            traj1 = rtb.mstraj(path1, tacc=tacc, dt=delay, tsegment=[1.0])
            traj2 = rtb.mstraj(path2, tacc=tacc, dt=delay, tsegment=tsegment)
            traj3 = rtb.mstraj(path3, tacc=tacc, dt=delay, tsegment=[1.5])
            q_full = np.vstack((traj1.q, traj2.q, traj3.q))

        else:
            log.warning("Invalid method specified. Choose 'jtraj', 'ctraj', or 'mstraj'.")
            return

        # -----------------------------
        # Animate full motion
        # -----------------------------
        animate(q_full)

        log.info(f"IK + {method.upper()} full pick-and-place trajectory complete.")