import adsk
import adsk.core
import adsk.fusion
import math
from . import app_context
from . import vector
from . import matrix

def build_object(radius, newComp, angle=math.pi, transl_vec=None):

    assert(radius > 0)
    # Create a new sketch.
    sketches = newComp.sketches
    root_comp = app_context.design.rootComponent
    xy_plane = root_comp.xYConstructionPlane
    sketch0 = sketches.add(xy_plane)

    circles = sketch0.sketchCurves.sketchCircles

    p0 = adsk.core.Point3D.create(0, 0, 0)

    circles.addByCenterRadius(p0, radius)  # outer circle

    lines = sketch0.sketchCurves.sketchLines
    axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(0, -radius-1, 0), adsk.core.Point3D.create(0, radius+1, 0))

    prof = sketch0.profiles.item(0)
    revolves = newComp.features.revolveFeatures
    revInput = revolves.createInput(prof, axisLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    angle = adsk.core.ValueInput.createByReal(angle)
    revInput.setAngleExtent(False, angle)
    obj = revolves.add(revInput)

    obj_collection = adsk.core.ObjectCollection.create()
    # add finger tubes
    for i in range(obj.bodies.count):
        obj_collection.add(obj.bodies.item(i))

    if transl_vec is not None:
        if not vector.is_zero(transl_vec):
            transform = adsk.core.Matrix3D.create()
            transform.translation = adsk.core.Vector3D.create(transl_vec[0], transl_vec[1], transl_vec[2])
            moveFeats = newComp.features.moveFeatures
            moveFeatureInput = moveFeats.createInput(obj_collection, transform)
            moveFeats.add(moveFeatureInput)

    return obj_collection


def build_object_translated(radius, newComp, angle=math.pi, transl_mat=None):

    assert(radius > 0)
    # Create a new sketch.
    sketches = newComp.sketches
    root_comp = app_context.design.rootComponent
    xy_plane = root_comp.xYConstructionPlane
    sketch0 = sketches.add(xy_plane)

    circles = sketch0.sketchCurves.sketchCircles

    p0 = adsk.core.Point3D.create(0, 0, 0)

    circles.addByCenterRadius(p0, radius)  # outer circle

    lines = sketch0.sketchCurves.sketchLines
    axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(0, -radius-1, 0), adsk.core.Point3D.create(0, radius+1, 0))

    prof = sketch0.profiles.item(0)
    revolves = newComp.features.revolveFeatures
    revInput = revolves.createInput(prof, axisLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    angle = adsk.core.ValueInput.createByReal(angle)
    revInput.setAngleExtent(False, angle)
    obj = revolves.add(revInput)

    obj_collection = adsk.core.ObjectCollection.create()
    # add finger tubes
    for i in range(obj.bodies.count):
        obj_collection.add(obj.bodies.item(i))

    if transl_mat is not None:
        if not matrix.is_zero(transl_mat):
            transform = adsk.core.Matrix3D.create()
            tm_serialized = matrix.serialize(transl_mat)
            transform.setWithArray(tm_serialized)
            moveFeats = newComp.features.moveFeatures
            moveFeatureInput = moveFeats.createInput(obj_collection, transform)
            moveFeats.add(moveFeatureInput)

    return obj_collection