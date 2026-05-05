import maya.cmds as cmds

def is_curve(obj):
    shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
    return any(cmds.nodeType(shape) == "nurbsCurve" for shape in shapes)


def is_mesh(obj):
    shapes = cmds.listRelatives(obj, shapes=True) or []
    return any(cmds.nodeType(shape) == "mesh" for shape in shapes)


class BBox:
    def __init__(self, obj):
        min_x, min_y, min_z, max_x, max_y, max_z = cmds.exactWorldBoundingBox(obj)
        self.x = max_x - min_x
        self.y = max_y - min_y
        self.z = max_z - min_z
