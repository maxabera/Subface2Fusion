import math

import adsk
import adsk.core
import adsk.fusion

from . import app_context
from . import part_finger
from . import fusion_marking
from . import fusion_sphere
from . import part_font
from . import part_bump
from . import fusion_parts
from . import units
from . import vector
from . import matrix


def build_object(a_finger: part_finger.Finger, new_comp):
    # Create a new sketch.

    assert(a_finger is not None), "Finger is NONE"
    a_finger.output_distance_units = units.Unit.centimeter
    sketches = new_comp.sketches

    root_comp = app_context.design.rootComponent
    xy_plane = root_comp.xYConstructionPlane
    sketch0 = sketches.add(xy_plane)

    circles = sketch0.sketchCurves.sketchCircles

    p0 = adsk.core.Point3D.create(0, 0, 0)

    outer_d = a_finger.outer_d
    inner_d = a_finger.inner_d

    # create beam profile
    if outer_d > 0:
        circles.addByCenterRadius(p0, outer_d / 2.0)  # outer circle

    start_pos = a_finger.start
    end_pos = a_finger.end

    finger_length = vector.distance(start_pos, end_pos)

    if finger_length == 0:
        return

    distance = adsk.core.ValueInput.createByReal(finger_length)
    prof = sketch0.profiles.item(0)
    extrudes = new_comp.features.extrudeFeatures
    extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance_definition = adsk.fusion.DistanceExtentDefinition.create(distance)
    extrude_input.setOneSideExtent(distance_definition, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    obj = extrudes.add(extrude_input)
    if obj.bodies.count > 0:
        body = obj.bodies.item(0)
        body.name = a_finger.name()
    obj.name = a_finger.name()
    obj.partNumber = a_finger.part_num()

    # sphere
    spheres = fusion_sphere.build_object((outer_d-0.01)/2, new_comp, angle=2 * math.pi)

    # bumps
    # finger_diameter, bump_height, bump_width, bump_delta, sq_num

    bump = part_bump.Bump()
    font = part_font.Font()

    # a_finger, a_bump, a_font
    finger_marking = fusion_marking.FingerMarking(a_finger, bump, font)
    bumps = finger_marking.build_object(new_comp)

    # Create a collection of entities for move
    bodies = adsk.core.ObjectCollection.create()
    # add finger tubes
    for i in range(obj.bodies.count):
        bodies.add(obj.bodies.item(i))

    # add finger bottoms
    for i in range(spheres.count):
        bodies.add(spheres.item(i))

    # add finger bottoms
    for i in range(bumps.count):
        bodies.add(bumps.item(i))

    if not matrix.is_zero(a_finger.tm):
        make_move04(bodies, new_comp, a_finger.tm)  # OK

    positive_bodies = adsk.core.ObjectCollection.create()
    for i in range(bodies.count):
        positive_bodies.add(bodies.item(i))

    return positive_bodies


def create_cylinder():
    pass

def make_move04(bodies, new_comp, transf_matrix):

    # move face to final position
    # transform
    tm = matrix.serialize(transf_matrix)
    # Create a transform to do move
    transform = adsk.core.Matrix3D.create()
    transform.setWithArray(tm)

    # Create a collection of entities for move
    moveFeats = new_comp.features.moveFeatures
    moveFeatureInput = moveFeats.createInput(bodies, transform)
    moveFeats.add(moveFeatureInput)


def make_move02(bodies, new_comp, start_pos, end_pos):

    # Create a transform to do move
    move_vector = adsk.core.Vector3D.create(start_pos[0],
                                            start_pos[1],
                                            start_pos[2])

    vec = vector.create(start_pos, end_pos)
    vec_length = vector.magnitude(vec)
    beam_vector = adsk.core.Vector3D.create(vec[0], vec[1], vec[2])
    start_vector = adsk.core.Vector3D.create(0, 0, 1)
    beam_vector.normalize()

    # radial distance
    transform = adsk.core.Matrix3D.create()
    transform.setToRotateTo(start_vector, beam_vector)
    move_feats = new_comp.features.moveFeatures
    move_feature_input = move_feats.createInput(bodies, transform)
    move_feats.add(move_feature_input)

    if move_vector.length != 0:
        transform = adsk.core.Matrix3D.create()
        transform.translation = move_vector
        move_feats = new_comp.features.moveFeatures
        move_feature_input = move_feats.createInput(bodies, transform)
        move_feats.add(move_feature_input)


def make_move01(a_finger, bodies, new_comp, start_pos, end_pos):

    from_origin = adsk.core.Point3D.create(0, 0, 0)
    from_x_axis = adsk.core.Vector3D.create(1, 0, 0)
    from_y_axis = adsk.core.Vector3D.create(0, 1, 0)
    from_z_axis = adsk.core.Vector3D.create(0, 0, 1)

    to_origin = adsk.core.Point3D.create(start_pos[0], start_pos[1], start_pos[2])
    to_x_axis = adsk.core.Vector3D.create(a_finger.x_base[0], a_finger.x_base[1], a_finger.x_base[2])
    to_x_axis.normalize()

    start_p3d = adsk.core.Point3D.create(start_pos[0], start_pos[1], start_pos[2])
    end_p3d = adsk.core.Point3D.create(end_pos[0], end_pos[1], end_pos[2])
    to_z_axis = start_p3d.vectorTo(end_p3d)
    to_z_axis.normalize()

    vec = vector.create(start_pos, end_pos)
    to_z_axis = adsk.core.Vector3D.create(vec[0], vec[1], vec[2])
    to_z_axis.normalize()

    to_y_axis = adsk.core.Vector3D.create(to_x_axis.x, to_x_axis.y, to_x_axis.z)
    to_y_axis = to_y_axis.crossProduct(to_z_axis)
    to_y_axis.normalize()

    s = ""
    s += "node: {}\n".format(a_finger.node_id)
    s += "finger: {}\n".format(a_finger.sq_num)
    s += "to_origin: {}\n".format(str(to_origin.asArray()))
    s += "to_x_axis: {}\n".format(str(to_x_axis.asArray()))
    s += "to_y_axis: {}\n".format(str(to_y_axis.asArray()))
    s += "to_z_axis: {}\n".format(str(to_z_axis.asArray()))

    # app_context.ui.messageBox(s)

    transform = adsk.core.Matrix3D.create()
    transform.setToAlignCoordinateSystems(from_origin, from_x_axis, from_y_axis, from_z_axis,
                                          to_origin, to_x_axis, to_y_axis, to_z_axis)

    move_feats = new_comp.features.moveFeatures
    move_feature_input = move_feats.createInput(bodies, transform)
    move_feats.add(move_feature_input)


def make_move03(a_finger, bodies, new_comp, start_pos, end_pos):

    to_origin = adsk.core.Point3D.create(start_pos[0], start_pos[1], start_pos[2])

    to_x_axis = adsk.core.Vector3D.create(a_finger.x_base[0], a_finger.x_base[1], a_finger.x_base[2])

    start_p3d = adsk.core.Point3D.create(start_pos[0], start_pos[1], start_pos[2])
    end_p3d = adsk.core.Point3D.create(end_pos[0], end_pos[1], end_pos[2])
    to_z_axis = start_p3d.vectorTo(end_p3d)

    to_y_axis = adsk.core.Vector3D.create(to_x_axis.x, to_x_axis.y, to_x_axis.z)
    to_y_axis = to_y_axis.crossProduct(to_z_axis)

    to_x_axis = to_z_axis.crossProduct(to_y_axis)

    to_z_axis.normalize()
    to_y_axis.normalize()
    to_x_axis.normalize()

    s = ""
    s += "node: {}\n".format(a_finger.node_id)
    s += "finger: {}\n".format(a_finger.sq_num)
    s += "to_origin: {}\n".format(str(to_origin.asArray()))
    s += "to_x_axis: {}\n".format(str(to_x_axis.asArray()))
    s += "to_y_axis: {}\n".format(str(to_y_axis.asArray()))
    s += "to_z_axis: {}\n".format(str(to_z_axis.asArray()))


    # app_context.ui.messageBox(s)

    transform = adsk.core.Matrix3D.create()
    transform.setWithCoordinateSystems(to_origin, to_x_axis, to_y_axis, to_z_axis)

    move_feats = new_comp.features.moveFeatures
    move_feature_input = move_feats.createInput(bodies, transform)
    move_feats.add(move_feature_input)