import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import numpy as np


class TeachPendant:
    """
    ImGui-based Teach Pendant for manual control of multiple robot arms.
    Provides real-time joint control sliders, reset, and random pose buttons.
    """

    def __init__(self, env, robots, window_title="Teach Pendant", size=(500, 650)):
        """
        Initialize the teach pendant window and setup ImGui rendering.

        Parameters:
        - env: Swift environment instance (for env.step updates)
        - robots: dict of { "Name": robot_instance }
        - window_title: title of the ImGui control window
        - size: (width, height) of the window
        """
        self.env = env
        self.robots = robots
        self.title = window_title

        # === Initialize GLFW + ImGui ===
        if not glfw.init():
            raise Exception("Could not initialize GLFW")

        self.window = glfw.create_window(size[0], size[1], window_title, None, None)
        glfw.make_context_current(self.window)

        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        print(f"[TeachPendant] GUI window '{window_title}' initialized.")

    # === Helper: Generate random joint angles ===
    @staticmethod
    def random_joint_angles(robot):
        try:
            q_min, q_max = robot.qlim
            return np.random.uniform(q_min, q_max)
        except AttributeError:
            return np.random.uniform(-np.pi, np.pi, robot.n)

    # === Helper: Render sliders for one robot ===
    def _robot_control_panel(self, name, robot):
        # Create a collapsible section for each robot
        expanded, _ = imgui.collapsing_header(f"🤖 {name}", visible=True)
        if expanded:
            changed = False
            q = robot.q.copy()

            for i in range(robot.n):
                # Unique ID per slider avoids duplicates
                imgui.push_id(f"{name}_joint_{i}")
                changed_joint, q[i] = imgui.slider_float(
                    f"Joint {i + 1}", float(q[i]), -np.pi, np.pi, format="%.2f rad"
                )
                imgui.pop_id()
                changed |= changed_joint

            if changed:
                robot.q = q
                self.env.step(0.02)

            if imgui.button(f"Reset##{name}"):
                robot.q = np.zeros(robot.n)
                self.env.step(0.02)
            imgui.same_line()
            if imgui.button(f"Random##{name}"):
                robot.q = self.random_joint_angles(robot)
                self.env.step(0.02)
            imgui.separator()

    # === Main control loop ===
    def run(self):
        print("[TeachPendant] Running manual control interface... (close window to exit)")
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            imgui.new_frame()

            # Main control window
            imgui.set_next_window_position(10, 10, imgui.ONCE)
            imgui.set_next_window_size(460, 600, imgui.ONCE)
            imgui.begin(self.title, True)
            imgui.text("Use sliders to manually control robot joints.")
            imgui.separator()

            # Render all robot panels safely
            for name, robot in self.robots.items():
                self._robot_control_panel(name, robot)

            imgui.end()
            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.shutdown()

    # === Graceful shutdown ===
    def shutdown(self):
        """Close ImGui + GLFW resources."""
        print("[TeachPendant] Shutting down GUI...")
        self.impl.shutdown()
        glfw.terminate()