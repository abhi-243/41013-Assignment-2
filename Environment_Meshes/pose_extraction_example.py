from Environment_Meshes.test import stl_data
import spatialmath as sm

brick_name = "2.stl"  # Example brick

brick_data = stl_data.get(brick_name)

if brick_data:
    # Extract raw data
    pos_start = brick_data["pos_start"]
    rot_start = brick_data["rot_start"]
    pos_end = brick_data["pos_end"]
    rot_end = brick_data["rot_end"]

    # Create SE3 transformation matrices (position + orientation)
    T_start = sm.SE3(*pos_start) * sm.SE3.RPY(*rot_start, order="xyz")
    T_end = sm.SE3(*pos_end) * sm.SE3.RPY(*rot_end, order="xyz")

    print(f"Brick: {brick_name}")
    print("Pick Pose (Start):\n", T_start)
    print("Place Pose (End):\n", T_end)
else:
    print(f"Brick '{brick_name}' not found in stl_data.")