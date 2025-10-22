# collision_utils.py
import numpy as np
from itertools import combinations
from spatialgeometry import Sphere
from roboticstoolbox import DHRobot
from spatialmath.base import *
from spatialgeometry import Sphere
from roboticstoolbox import DHRobot, jtraj
from ir_support import line_plane_intersection

def is_intersection_point_inside_triangle(intersect_p, triangle_verts):
    u = triangle_verts[1, :] - triangle_verts[0, :]
    v = triangle_verts[2, :] - triangle_verts[0, :]
    uu = np.dot(u, u)
    uv = np.dot(u, v)
    vv = np.dot(v, v)
    w = intersect_p - triangle_verts[0, :]
    wu = np.dot(w, u)
    wv = np.dot(w, v)
    D = uv * uv - uu * vv
    s = (uv * wv - vv * wu) / D
    if s < 0.0 or s > 1.0:
        return False
    t = (uv * wu - uu * wv) / D
    if t < 0.0 or (s + t) > 1.0:
        return False
    return True

def get_link_poses(robot: DHRobot, q=None):
    if q is None:
        return robot.fkine_all().A
    return robot.fkine_all(q).A

def is_collision(robot, q_matrix, faces, vertices, face_normals, collisions=[], env=None, return_once_found=True):
    result = False
    for q in q_matrix:
        tr = get_link_poses(robot, q)
        for i in range(np.size(tr,2)-1):
            for j, face in enumerate(faces):
                vert_on_plane = vertices[face][0]
                intersect_p, check = line_plane_intersection(face_normals[j], vert_on_plane, tr[i][:3,3], tr[i+1][:3,3])
                triangle_list = np.array(list(combinations(face,3)),dtype=int)
                if check == 1:
                    for triangle in triangle_list:
                        if is_intersection_point_inside_triangle(intersect_p, vertices[triangle]):
                            if env is not None:
                                new_collision = Sphere(radius=0.05, color=[1,0,0,1])
                                new_collision.T = transl(intersect_p[0], intersect_p[1], intersect_p[2])
                                env.add(new_collision)
                                collisions.append(new_collision)
                            result = True
                            if return_once_found:
                                return result
                            break
    return result

def fine_interpolation(q1, q2, max_step_radians=np.deg2rad(1)):
    steps = 2
    while np.any(max_step_radians < np.abs(np.diff(jtraj(q1, q2, steps).q, axis=0))):
        steps += 1
    return jtraj(q1,q2,steps).q

def interpolate_waypoints_radians(waypoints, max_step_radians=np.deg2rad(1)):
    q_matrix = []
    for i in range(len(waypoints)-1):
        q_matrix.extend(fine_interpolation(waypoints[i], waypoints[i+1], max_step_radians))
    return q_matrix