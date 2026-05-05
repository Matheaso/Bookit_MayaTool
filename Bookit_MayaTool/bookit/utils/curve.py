import math

import maya.cmds as cmds

def get_curve_length(curve: str) -> float:
    shapes = cmds.listRelatives(curve, shapes=True, fullPath=True) or []

    if not shapes:
        cmds.warning(f"{curve} has no shape")
        return 0.0

    shape = shapes[0]

    curve_info = cmds.createNode("curveInfo")

    cmds.connectAttr(
        f"{shape}.worldSpace[0]",
        f"{curve_info}.inputCurve",
        force=True
    )

    length = cmds.getAttr(f"{curve_info}.arcLength")

    cmds.delete(curve_info)

    return length


def sample_curve_at_percent(curve: str, percent: float):
    shapes = cmds.listRelatives(curve, shapes=True, fullPath=True) or []
    if not shapes:
        cmds.warning("No shape found")
        return 0, 0, 0

    shape = shapes[0]

    mp = cmds.createNode("motionPath")
    cmds.connectAttr(f"{shape}.worldSpace[0]", f"{mp}.geometryPath", force=True)

    cmds.setAttr(f"{mp}.fractionMode", True)
    cmds.setAttr(f"{mp}.uValue", percent)

    pos = cmds.getAttr(f"{mp}.allCoordinates")[0]

    cmds.delete(mp)

    return pos


def offset_side_curve(pos, next_pos, offset):
    dir_x = next_pos[0] - pos[0]
    dir_z = next_pos[2] - pos[2]

    length = (dir_x**2 + dir_z**2) ** 0.5

    if length == 0:
        return pos

    dir_x /= length
    dir_z /= length

    side_x = -dir_z
    side_z = dir_x

    return (
        pos[0] + side_x * offset,
        pos[1],
        pos[2] + side_z * offset,
    )


def get_y_rotation_from_points(p1, p2):
    dx = p2[0] - p1[0]
    dz = p2[2] - p1[2]

    angle = math.degrees(math.atan2(dx, dz))
    return angle