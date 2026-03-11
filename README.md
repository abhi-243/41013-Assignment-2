# 41013 Assignment 2 — Pick-and-Place DoGoodBot

**Subject:** 41013 Industrial Robotics  
**University:** University of Technology Sydney (UTS)  
**Author:** Abhi Naglapura, Quoc Duong, Hamish Judson
**License:** MIT

---

## Overview

This project implements a **multi-robot pick-and-place simulation** for the DoGoodBot assignment in UTS 41013 Industrial Robotics. Four robot arms operate inside a **Swift** simulator environment, each assigned a set of numbered brick STL meshes to pick from scattered start positions and place onto a structured target configuration — together constructing a collaborative assembly.

Motion is controlled via **RMRC (Resolved Motion Rate Control)**, and the system includes a real-time **ImGui GUI** with software E-STOP and a physical **hardware E-STOP** button wired to an Arduino microcontroller.

---

## Robots

| Robot | Module | Assigned To |
|-------|--------|-------------|
| ABB IRB120 | `IRB120/IRB120.py` | Abhi |
| UR3 | `ir_support` (given) | — |
| myCobot 320 M5 | `myCobot320m5/milan.py` | Milan |
| XI1305 | `XI1305_module/XI1305_robot.py` | Hamish |

Each robot is defined as a custom class wrapping `roboticstoolbox`, with its own DH parameters and STL link meshes.

---

## Repository Structure

```
41013-Assignment-2/
│
├── main.py                     # Main simulation entry point
├── GUI.py                      # ImGui Robot Control Panel (E-STOP + joint sliders)
├── teach_pendant.py            # ImGui Teach Pendant for manual joint control
├── requirements.txt            # Python dependencies
├── imgui.ini                   # ImGui layout state
│
├── IRB120/                     # ABB IRB120 robot module (Abhi)
│   ├── IRB120.py               # Robot class definition
│   ├── link0.stl – link6.stl   # Visual meshes
│   └── *.pdf                   # IRB120 reference datasheets
│
├── myCobot320m5/               # Elephant Robotics myCobot 320 M5 module (Milan)
│   └── milan.py
│
├── XI1305_module/              # XI1305 robot module (Hamish)
│   └── XI1305_robot.py
│
├── Environment_Meshes/         # Scene meshes
│   ├── Environment/            # City_Street_Set .dae scene file
│   ├── Bricks/                 # 30 numbered brick STL meshes (1.stl – 30.stl)
│   ├── Race_Car_correct.dae    # Decorative race car mesh
│   └── test.py                 # Brick position/colour/rotation data (stl_data dict)
│
├── External E-Stop/            # Arduino hardware E-STOP firmware
│   ├── src/main.cpp            # Debounced button → Serial "PRESSED"/"RELEASED"
│   └── platformio.ini          # PlatformIO build config
│
├── Lab Assignment 2 - Pick-and-Place DoGoodBot.pdf   # Assignment brief
├── 6394097.pdf                 # Submitted report
└── LICENSE
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│                                                              │
│  Swift Env ──► 4 Robots + Bricks + Scene Mesh               │
│                                                              │
│  Global Sequence → per-robot RMRC loop                       │
│       ↓                                                      │
│  fk_pose() → position/orientation error                      │
│       ↓                                                      │
│  jacob0() → damped-least-squares joint velocities            │
│       ↓                                                      │
│  clip_to_qlim() → robot.q update → env.step()               │
│                                                              │
│  On convergence → attach_mesh / detach_mesh                  │
└─────────────┬───────────────────────┬───────────────────────┘
              │                       │
     ┌────────▼────────┐    ┌─────────▼──────────┐
     │    GUI.py        │    │  External E-Stop    │
     │  ImGui Panel     │    │  Arduino (COM9)     │
     │  • E-STOP btn    │    │  Button → Serial    │
     │  • Joint sliders │    │  "PRESSED"/"RELEASED│
     │  • Per-robot     │    └─────────────────────┘
     │    collapsibles  │
     └──────────────────┘
```

---

## Motion Control — RMRC

Each robot moves via the **Resolved Motion Rate Control** law:

```
ẋ = J(q) · q̇
q̇ = J⁺ · ẋ_des    (with damped least squares, λ = 0.2)
```

Where:
- `ẋ_des = Kp · e` with `Kp = 2`
- `e` is the 6-DOF pose error (position + rotation)
- Position error is computed from forward kinematics (`fkine`)
- Rotation error uses the cross-product skew-symmetric formulation across all three rotation axes
- Joint velocity is integrated with `dt = 0.1 s`, capped at `vel_limit = 0.8 m/s`
- Joint limits are enforced via `clip_to_qlim()` at every step

Convergence threshold: `tol_pos = 0.01 m`. When reached, the robot either **attaches** (pick) or **detaches** (place) the brick mesh.

---

## Pick-and-Place Sequence

Bricks are assigned to robots and executed via a **global sequence** of `(robot_idx, action, stl_name)` tuples. Robots move one at a time through the sequence.

| Robot | Bricks Handled |
|-------|---------------|
| IRB120 | 7, 15, 17, 18, 19, 20, 26, 30 |
| UR3 | 2, 3, 4, 5, 6, 16, 25, 29 |
| myCobot320 | 9, 12, 13, 21, 22, 24, 28 |
| XI1305 | 8, 10, 11, 14, 23, 27 |

Each brick has a `pos_start` (scattered) and a target pose defined in `targets[]` in `main.py`. An approach offset of `0.05 m` above the target is used before each pick/place.

---

## GUI — Robot Control Panel

`GUI.py` implements a **GLFW + ImGui** control panel with:

- 🚨 **E-STOP button** — immediately halts all robot motion when clicked
- Collapsible panels per robot with **joint angle sliders** (respects `qlim`)
- Dark theme with orange/red button highlights

`teach_pendant.py` provides a separate **Teach Pendant** window for manual joint control with per-robot **Reset** and **Random pose** buttons.

---

## Hardware E-STOP

The `External E-Stop/` folder contains Arduino firmware for a **physical emergency stop button**:

- Built with **PlatformIO** (Arduino framework)
- Button wired to **GPIO 2** with `INPUT_PULLUP`
- 10 ms debounce logic
- Sends `"PRESSED"` or `"RELEASED"` over **Serial at 9600 baud**

`main.py` reads from `COM9` in a polling loop (`check_hardware_estop()`). When `"PRESSED"` is received, `hardware_estop_triggered = True` halts the simulation loop.

> **Note:** Update `COM9` in `main.py` to match your system's serial port.

---

## Dependencies

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

Key packages include:

| Package | Purpose |
|---------|---------|
| `roboticstoolbox-python` | Robot kinematics, Jacobians, `rtb` models |
| `swift` | 3D browser-based robot simulator |
| `spatialmath` | SE3 transforms, rotation utilities |
| `spatialgeometry` | STL/DAE mesh loading for Swift |
| `imgui[glfw]` | ImGui Python bindings for GUI |
| `pyserial` | Hardware E-STOP serial comms |
| `numpy` | Matrix/vector math |
| `ir-support` | UR3 model (provided by subject) |
| `open3d`, `pybullet` | Additional geometry/physics utilities |

---

## Running the Simulation

### Prerequisites

- Python 3.9+
- Dependencies installed via `pip install -r requirements.txt`
- (Optional) Arduino flashed with `External E-Stop/` firmware and connected on `COM9`

### Launch

```bash
python main.py
```

This will:
1. Launch the **Swift** simulator in your browser
2. Add all four robots and the city street environment to the scene
3. Load all 30 brick meshes at their start positions
4. Open the **ImGui Robot Control Panel**
5. Execute the global pick-and-place sequence using RMRC

---

## Notes

- The simulation is run in **realtime** (`swift.launch(realtime=True)`)
- `check_self_collision()` is currently stubbed out (`return False`) — a placeholder for future implementation
- `client.setInsecure()` equivalent: TLS is not relevant here, but the hardware E-STOP serial port (`COM9`) must be updated per machine
- If no Arduino is connected, comment out the `serial.Serial(...)` line and the `check_hardware_estop()` calls in `main.py`

---

## License

MIT License © 2025 Abhi Naglapura
