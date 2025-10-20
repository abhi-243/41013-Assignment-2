import glfw
import OpenGL.GL as gl
import imgui
import numpy as np
from imgui.integrations.glfw import GlfwRenderer


class RobotControlUI:
    def __init__(self, robots, names=None):
        self.robots = robots
        self.names = names or [f"Robot {i+1}" for i in range(len(robots))]
        self.estop_triggered = False
        self.selected_angles = [list(robot.q.copy()) for robot in robots]

        self.window = None
        self.impl = None

    def initialize(self):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        self.window = glfw.create_window(1280, 720, "Robot Control UI", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self.window)

        # ImGui setup
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        # Theme
        self._setup_style()

    def _setup_style(self):
        imgui.style_colors_dark()
        style = imgui.get_style()
        colors = style.colors
        colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.1, 0.1, 0.1, 1)
        colors[imgui.COLOR_TEXT] = (1.0, 1.0, 1.0, 1)
        colors[imgui.COLOR_BUTTON] = (1.0, 0.5, 0.0, 1)
        colors[imgui.COLOR_BUTTON_HOVERED] = (1.0, 0.0, 0.0, 1)

    def render(self):
        if self.window is None:
            self.initialize()

        glfw.poll_events()
        self.impl.process_inputs()
        imgui.new_frame()

        self._render_ui()

        # Draw
        gl.glClearColor(0.1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        self.impl.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)
        #self.shutdown()

    def _render_ui(self):
        imgui.begin("Robot Control Panel")

        if imgui.button("🚨 E-STOP"):
            self.estop_triggered = True
            print("E-STOP pressed!")

        imgui.separator()

        for i, robot in enumerate(self.robots):
            name = self.names[i]

            if imgui.collapsing_header(f"🤖 {name}", visible=True):
                dof = len(robot.q)
                changed = False

                # Sliders for joints inside collapsing header
                for j in range(dof):
                    angle = self.selected_angles[i][j]
                    changed_joint, new_angle = imgui.slider_float(f"{name} - Joint {j+1}", angle, -3.14, 3.14)
                    if changed_joint:
                        self.selected_angles[i][j] = new_angle
                        changed = True

                # Joint angles display inside collapsing header
                imgui.text("Current Joint Angles:")
                for j in range(dof):
                    imgui.text(f"J{j+1}: {robot.q[j]:.2f} rad")

                if changed and not self.estop_triggered:
                    robot.q = self.clip_to_qlim(robot, np.array(self.selected_angles[i]))

        imgui.end()

    def shutdown(self):
        if self.impl:
            self.impl.shutdown()
        glfw.terminate()

    @staticmethod
    def clip_to_qlim(robot, q):
        try:
            qmin, qmax = robot.qlim
            q_clipped = np.minimum(np.maximum(q, qmin), qmax)
            return q_clipped
        except Exception:
            return q