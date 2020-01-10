__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

import adsk
import adsk.core
import adsk.fusion
from . import vector
from . import units
from . import part_beam
from . import matrix
from . import app_context
from . import material
from . import color_constants
import math


def create_beams(beam_list, progress=None):
    succesfully_finished = True

    mat = material.aluminum_rough_appearance(color_constants.GRAY90)
    make_beams = True
    for idx, a_beam in enumerate(beam_list):


        if progress is not None:
            if progress.wasCancelled:
                succesfully_finished = False
                break
            # Update progress value of progress dialog
            progress.progressValue = idx

        if make_beams:
            if not a_beam.is_ignored:
                new_comp = app_context.createNewComponent()
                if new_comp is None:
                    app_context.ui.messageBox('New component failed to create', 'New Component Failed')
                    return

                build_object(a_beam, new_comp)

                occs = app_context.design.rootComponent.allOccurrencesByComponent(new_comp)
                occ = occs.item(0)
                occ.appearance = mat
                occ.component.name = a_beam.name()


def build_object(a_beam: part_beam.Beam, newComp):
    """
    :param newComp:
    :return:
    """
    dist_unit = app_context.active_attrs.import_distance_units
    radius = a_beam.outer_d / 2
    in_r = a_beam.inner_d /2
    start_pos = a_beam.start
    end_pos = a_beam.end
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
    if in_r > 0:
        circles.addByCenterRadius(p0, in_r)  # inner circle

    distance = adsk.core.ValueInput.createByReal(length)
    prof = sketch0.profiles.item(0)
    extrudes = newComp.features.extrudeFeatures
    extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distanceDefinition = adsk.fusion.DistanceExtentDefinition.create(distance)
    extrudeInput.setOneSideExtent(distanceDefinition, adsk.fusion.ExtentDirections.PositiveExtentDirection)

    obj = extrudes.add(extrudeInput)
    if obj.bodies.count > 0:
        body = obj.bodies.item(0)

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

    if not matrix.is_zero(a_beam.tm):
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

    newComp.name = a_beam.name()

    return obj.bodies.item(0)