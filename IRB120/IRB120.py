import swift
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3
from spatialgeometry import Cuboid, Cylinder
import numpy as np
from ir_support.robots.DHRobot3D import DHRobot3D
from math import pi
import os
import logging

# Configure logging (can be overridden by calling script)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# =====================================================================
# Robot Definition
# =====================================================================
class IRB120(DHRobot3D):
    def __init__(self):
        links = self._create_DH()

        link3D_names = dict(
            link0='link0', color0=(0.8,0.8,0.8),
            link1='link1', color1=(0.8,0.8,0.8),
            link2='link2', color2=(0.8,0.8,0.8),
            link3='link3', color3=(0.8,0.8,0.8),
            link4='link4', color4=(0.8,0.8,0.8),
            link5='link5', color5=(0.8,0.8,0.8),
            link6='link6', color6=(0.3,0.3,0.3)
        )

        qtest = [0, 0, 0, 0, 0, 0]
        qtest_transforms = [
            spb.transl(0,        0.0095,    0    ) @ spb.rpy2tr(np.pi,  0,          0,          order="xyz"),
            spb.transl(0,        0.0095,    0.166) @ spb.rpy2tr(np.pi,  0,          0,          order="xyz"),
            spb.transl(0,        0.0095,    0.290) @ spb.rpy2tr(np.pi,  0,          np.pi/2,    order="xyz"),
            spb.transl(0,        0.0095,    0.560) @ spb.rpy2tr(np.pi,  0,          np.pi/2,    order="xyz"),
            spb.transl(0.1496,   0,         0.630) @ spb.rpy2tr(np.pi,  np.pi/2,    0,          order="xyz"),
            spb.transl(0.302,    0,         0.630) @ spb.rpy2tr(np.pi,  0,          np.pi/2,    order="xyz"),
            spb.transl(0.3614,   0,         0.630) @ spb.rpy2tr(np.pi,  np.pi/2,    0,          order="xyz")
        ]
        
        self.link_offsets = [
            SE3.Trans(0.06,     0,      0.084 ), #link0
            SE3.Trans(0,        0,      0.093 ), #link1
            SE3.Trans(0,        -0.125, 0     ), #link2
            SE3.Trans(-0.03,    -0.045, 0     ), #link3
            SE3.Trans(0.007,    0,      0.1   ), #link4
            SE3.Trans(0,        0,      0     ), #link5
            SE3.Trans(0,        0,      0.006 )  #link6
        ]
        
        self.collision_shapes = [
            Cuboid(scale=[0.294, 0.180, 0.168], base=qtest_transforms[0] * self.link_offsets[0], collision=True, color=(1,  0.5,    0,  0.0001)),  # link0
            Cuboid(scale=[0.217, 0.214, 0.186], base=qtest_transforms[1] * self.link_offsets[1], collision=True, color=(1,  0.5,    0,  0.0001)),  # link1
            Cuboid(scale=[0.114, 0.389, 0.219], base=qtest_transforms[2] * self.link_offsets[2], collision=True, color=(1,  0.5,    0,  0.0001)),  # link2
            Cuboid(scale=[0.246, 0.194, 0.115], base=qtest_transforms[3] * self.link_offsets[3], collision=True, color=(1,  0.5,    0,  0.0001)),  # link3
            Cuboid(scale=[0.105, 0.126, 0.193], base=qtest_transforms[4] * self.link_offsets[4], collision=True, color=(1,  0.5,    0,  0.0001)),  # link4
            Cuboid(scale=[0.132, 0.082, 0.070], base=qtest_transforms[5] * self.link_offsets[5], collision=True, color=(1,  0.5,    0,  0.0001)),  # link5
            Cuboid(scale=[0.040, 0.040, 0.013], base=qtest_transforms[6] * self.link_offsets[6], collision=True, color=(1,  0.5,    0,  0.0001))   # link6 / EE
        ]

        current_path = os.path.abspath(os.path.dirname(__file__))
        super().__init__(
            links,
            link3D_names,
            name='IRB120',
            link3d_dir=current_path,
            qtest=qtest,
            qtest_transforms=qtest_transforms
        )
        self.q = qtest

    def _create_DH(self):
        a       =   [0,         0.270,  0.070,      0,          0,          0]
        d       =   [0.290,     0,      0,          0.302,      0,          0.072]
        alpha   =   [-np.pi/2,  0,      -np.pi/2,   np.pi/2,    -np.pi/2,   0]
        offset  =   [0,         -pi/2,  0,          0,          0,          pi]
        qlimits = {
            "joint1": [-165 * pi/180, 165 * pi/180],
            "joint2": [-110 * pi/180, 110 * pi/180],
            "joint3": [-110 * pi/180, 70  * pi/180],
            "joint4": [-160 * pi/180, 160 * pi/180],
            "joint5": [-120 * pi/180, 120 * pi/180],
            "joint6": [-400 * pi/180, 400 * pi/180]
        }

        qlim = [
            qlimits["joint1"],
            qlimits["joint2"],
            qlimits["joint3"],
            qlimits["joint4"],
            qlimits["joint5"],
            qlimits["joint6"]
        ]

        links = [rtb.RevoluteDH(d=d[i],
                                a=a[i],
                                alpha=alpha[i],
                                offset=offset[i],
                                qlim=qlim[i]) for i in range(6)]
        return links
    
    def update_collisions(self, q=None):
        """Update link poses for collision detection."""
        q = self.q if q is None else q
        for i, shape in enumerate(self.collision_shapes):
            T_link = self.fk(q, end=i+1)  # transform up to link i+1
            shape.pose = T_link * self.link_offsets[i]

    def check_environment_collision(self, external_objects, q=None):
        """
        Returns True if any link collides with an object in the environment.
        :param external_objects: list of CollisionShape objects
        """
        self.update_collisions(q)
        for link_shape in self.collision_shapes:
            for obj in external_objects:
                if link_shape.iscollided(obj):
                    return True
        return False

    def move_with_env_check(self, q_target, external_objects, steps=50, delay=0.02):
        qtraj = rtb.jtraj(self.q, q_target, steps).q
        for q in qtraj:
            self.q = q
            if self.check_environment_collision(external_objects):
                log.warning("Collision with environment detected! Motion aborted.")
                return False
            if hasattr(self, "env") and self.env:
                self.env.step(delay)
        return True

    
    def ee_pose(self):
        """Return the current end-effector pose (SE3)."""
        return self.fkine(self.q)

    def ee_position(self):
        """Return the end-effector position as a NumPy array [x, y, z]."""
        return np.array(self.ee_pose().t)

    def ee_orientation(self, as_euler=True):
        """Return orientation as Euler (rpy) or rotation matrix."""
        T = self.ee_pose()
        return T.rpy(order='xyz') if as_euler else T.R
    
    def fk(self, q=None):
        """Compute forward kinematics for given joint angles."""
        return self.fkine(self.q if q is None else q)

    def ik(self, target_pose, q0=None):
        """Compute inverse kinematics (numerical)."""
        sol = self.ikine_LM(target_pose, q0=self.q if q0 is None else q0)
        return sol.q if sol.success else None
    
    def home(self):
        """Move robot to home position (q = 0)."""
        self.q = np.zeros(self.n)
        log.info("Robot moved to home position.")

    def within_limits(self, q=None):
        """Check if joint configuration is within limits."""
        q = self.q if q is None else q
        return all(self.qlim[i, 0] <= q[i] <= self.qlim[i, 1] for i in range(self.n))
    
    def info(self):
        """Print robot model summary."""
        print(f"\nRobot: {self.name}")
        print(f"Number of joints: {self.n}")
        print(f"Current joint config (rad): {np.round(self.q, 3)}")
        print(f"End-effector position (m): {np.round(self.ee_position(), 3)}")