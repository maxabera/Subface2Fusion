
from . import vector

from . import units
from . import app_context
from . import finger_bridge
from . import fusion_sphere

import math
import adsk.core
import adsk.fusion
import adsk


def build_object(a_fibridge: finger_bridge.FingerBridge, newComp):
    # Create a new sketch.
    sketches = newComp.sketches
    xyPlane = newComp.xYConstructionPlane
    sketch0 = sketches.add(xyPlane)

    circles = sketch0.sketchCurves.sketchCircles

    p0 = adsk.core.Point3D.create(0, 0, 0)

    outer_d = units.distance(a_fibridge.diameter, app_context.active_attrs.import_distance_units, units.Unit.centimeter)

    # create beam profile
    if outer_d > 0:
        circles.addByCenterRadius(p0, outer_d / 2.0)  # outer circle

    start_pos = units.distance_array(a_fibridge.start, app_context.active_attrs.import_distance_units,
                                     units.Unit.centimeter)
    end_pos = units.distance_array(a_fibridge.end, app_context.active_attrs.import_distance_units, units.Unit.centimeter)

    fibridge_len = vector.distance(start_pos, end_pos)

    if fibridge_len == 0:
        return

    distance = adsk.core.ValueInput.createByReal(fibridge_len)
    prof = sketch0.profiles.item(0)
    extrudes = newComp.features.extrudeFeatures
    extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distanceDefinition = adsk.fusion.DistanceExtentDefinition.create(distance)
    extrudeInput.setOneSideExtent(distanceDefinition, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    obj = extrudes.add(extrudeInput)
    if obj.bodies.count > 0:
        body = obj.bodies.item(0)
        body.name = a_fibridge.name()
    obj.name = a_fibridge.name()
    obj.partNumber = a_fibridge.part_num()

    # make +0.01 spheres a bit bigger for better combine.join operation
    spheres0 = fusion_sphere.build_object(outer_d / 2+0.01, newComp, angle=2*math.pi)
    spheres1 = fusion_sphere.build_object(outer_d / 2+0.01, newComp, angle=-2*math.pi, transl_vec=[0, 0, fibridge_len])

    # Create a collection of entities for move
    bodies = adsk.core.ObjectCollection.create()
    # add finger tubes
    for i in range(obj.bodies.count):
        bodies.add(obj.bodies.item(i))

    # add finger bottoms
    for i in range(spheres0.count):
        bodies.add(spheres0.item(i))

    # add finger bottoms
    for i in range(spheres1.count):
        bodies.add(spheres1.item(i))

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
    if not start_vector.isEqualTo(beam_vector):
        transform = adsk.core.Matrix3D.create()
        transform.setToRotateTo(start_vector, beam_vector)
        moveFeats = newComp.features.moveFeatures
        moveFeatureInput = moveFeats.createInput(bodies, transform)
        moveFeats.add(moveFeatureInput)

    if move_vector.length != 0:
        transform = adsk.core.Matrix3D.create()
        transform.translation = move_vector
        moveFeats = newComp.features.moveFeatures
        moveFeatureInput = moveFeats.createInput(bodies, transform)
        moveFeats.add(moveFeatureInput)

    # Get the single occurrence that references the component.

    positive_bodies = adsk.core.ObjectCollection.create()
    for i in range(bodies.count):
        positive_bodies.add(bodies.item(i))

    return positive_bodies
