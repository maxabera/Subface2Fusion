__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

import adsk
import adsk.core
import adsk.fusion
from . import vector
from . import units
from . import part_finger
from . import matrix
from . import app_context
import math


def build_object(a_finger: part_finger.Finger, newComp):
    """

    :param start_pos: [x, y, z]
    :param end_pos: [x, y, z]
    :param radius:
    :param newComp:
    :return:
    """
    dist_unit = app_context.active_attrs.import_distance_units
    radius = a_finger.inner_d/2
    start_pos = a_finger.start
    end_pos = a_finger.end
    encore = a_finger.rod_encore
    length = vector.distance(start_pos, end_pos)

    assert(radius > 0)
    assert (length > 0)

    # Create a new sketch.
    sketches = newComp.sketches
    xyPlane = newComp.xYConstructionPlane
    sketch0 = sketches.add(xyPlane)

    circles = sketch0.sketchCurves.sketchCircles

    p0 = adsk.core.Point3D.create(0, 0, 0)

    # create beam profile
    if radius > 0:
        circles.addByCenterRadius(p0, radius)  # outer circle

    distance = adsk.core.ValueInput.createByReal(length+encore)
    prof = sketch0.profiles.item(0)
    extrudes = newComp.features.extrudeFeatures
    extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distanceDefinition = adsk.fusion.DistanceExtentDefinition.create(distance)
    extrudeInput.setOneSideExtent(distanceDefinition, adsk.fusion.ExtentDirections.PositiveExtentDirection)

    obj = extrudes.add(extrudeInput)
    if obj.bodies.count > 0:
        body = obj.bodies.item(0)
        body.name = a_finger.phalanx_name()

    # Create a collection of entities for move
    bodies = adsk.core.ObjectCollection.create()
    # add finger tubes
    for i in range(obj.bodies.count):
        bodies.add(obj.bodies.item(i))

    # Create a transform to do move
    move_vector = adsk.core.Vector3D.create(start_pos[0],
                                            start_pos[1],
                                            start_pos[2])

    vec = vector.create(start_pos, end_pos)
    beam_vector = adsk.core.Vector3D.create(vec[0], vec[1], vec[2])
    start_vector = adsk.core.Vector3D.create(0, 0, 1)
    beam_vector.normalize()

    if not matrix.is_zero(a_finger.tm):
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

    bodies = adsk.core.ObjectCollection.create()
    bodies.add(obj.bodies.item(0))

    return bodies