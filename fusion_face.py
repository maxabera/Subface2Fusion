__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

import adsk
import adsk.core
import adsk.fusion

from . import face
from . import app_context
from . import material
from . import color_constants
from . import units
from . import matrix
from . import fusion_bolt
from . import fusion_parts as fup


def build_object(a_face, newComp):

    # Create a new sketch.
    sketches = newComp.sketches
    xyPlane = newComp.xYConstructionPlane
    sketch0 = sketches.add(xyPlane)

    sketch_lines = sketch0.sketchCurves.sketchLines
    sketch_points = sketch0.sketchPoints

    # sketch polygon
    poly = a_face.grounded_polypoints
    n_points = len(poly)
    # FACES
    if n_points > 0:
        for i in range(n_points - 1):
            p0 = units.distance_array(poly[i], app_context.active_attrs.import_distance_units, units.Unit.centimeter)
            p1 = units.distance_array(poly[i+1], app_context.active_attrs.import_distance_units, units.Unit.centimeter)

            sketch_lines.addByTwoPoints(adsk.core.Point3D.create(p0[0], p0[1], p0[2]),
                                        adsk.core.Point3D.create(p1[0], p1[1], p1[2]))

        p0 = units.distance_array(poly[-1], app_context.active_attrs.import_distance_units, units.Unit.centimeter)
        p1 = units.distance_array(poly[0], app_context.active_attrs.import_distance_units, units.Unit.centimeter)

        sketch_lines.addByTwoPoints(adsk.core.Point3D.create(p0[0], p0[1], p0[2]),
                                    adsk.core.Point3D.create(p1[0], p1[1], p1[2]))

    prof = sketch0.profiles.item(0)

    # extrude
    extrudes = newComp.features.extrudeFeatures
    extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    th_cm = units.Distance(a_face.thickness, app_context.active_attrs.import_distance_units).cm
    distance = adsk.core.ValueInput.createByReal(th_cm)
    distanceDefinition = adsk.fusion.DistanceExtentDefinition.create(distance)
    extrudeInput.setOneSideExtent(distanceDefinition, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    obj = extrudes.add(extrudeInput)

    comp = obj.parentComponent


    # Get the single occurrence that references the component.
    occs = app_context.design.rootComponent.allOccurrencesByComponent(comp)
    occ = occs.item(0)
    occ.appearance = material.plastic_abs_appearance(color_constants.LIMEGREEN)

    face_name = app_context.active_attrs.model_id
    occ.component.name = '{}_{:03d}'.format(face_name, a_face.fidx)


    # make_holes(a_face, obj)

    # move face to final position
    # transform
    tm = matrix_to_array(a_face.transformation_matrix)
    # Create a transform to do move
    transform = adsk.core.Matrix3D.create()
    transform.setWithArray(tm)

    # Create a collection of entities for move
    bodies = adsk.core.ObjectCollection.create()
    bodies.add(obj.bodies.item(0))
    moveFeats = newComp.features.moveFeatures
    moveFeatureInput = moveFeats.createInput(bodies, transform)
    moveFeats.add(moveFeatureInput)

    return obj.bodies.item(0)

def matrix_to_array(m):
    # convert
    tm = list()

    for row_i, row in enumerate(m):
        for cell_i, cell in enumerate(row):
            cell_cm = cell
            if cell_i == 3 and row_i < 3:
                # convert origin coordinates to centimeters
                cell_cm = units.Distance(cell, app_context.active_attrs.import_distance_units).cm
            tm.append(cell_cm)
    return tm



def draw_holes(a_face, a_sketch):

    n_holes = len(a_face.holes)
    if n_holes > 0:
        for h in a_face.holes:
            x = units.Distance(h.position[0], app_context.active_attrs.import_distance_units).cm
            y = units.Distance(h.position[1], app_context.active_attrs.import_distance_units).cm
            z = units.Distance(h.position[2], app_context.active_attrs.import_distance_units).cm
            r = units.Distance(h.diameter/2.0, app_context.active_attrs.import_distance_units).cm
            # create a SketchCircle with a placeholder radius. centerPoint is a Point3D
            circle = a_sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(x, y, z),r)


def make_holes(a_face, extrusion: adsk.fusion.ExtrudeFeature):

    rootComp = app_context.design.rootComponent
    start_faces = extrusion.endFaces
    start_face = start_faces.item(0)

    # Create a construction plane by offsetting the end face
    planes = rootComp.constructionPlanes
    sketches = rootComp.sketches
    planeInput = planes.createInput()
    offsetVal = adsk.core.ValueInput.createByReal(1.0)
    planeInput.setByOffset(start_face, offsetVal)
    offsetPlane = planes.add(planeInput)

    offsetSketch = sketches.add(offsetPlane)
    offsetSketchPoints = offsetSketch.sketchPoints

    # HOLES
    ptColl = adsk.core.ObjectCollection.create()
    n_holes = len(a_face.holes)
    if n_holes > 0:
        for h in a_face.holes:
            x = units.Distance(h.position[0], app_context.active_attrs.import_distance_units).cm
            y = units.Distance(h.position[1], app_context.active_attrs.import_distance_units).cm
            z = units.Distance(h.position[2], app_context.active_attrs.import_distance_units).cm
            new_pt = offsetSketchPoints.add(adsk.core.Point3D.create(x, y, z))
            ptColl.add(new_pt)

    # Create a hole input
    holes = rootComp.features.holeFeatures
    holeInput = holes.createSimpleInput(adsk.core.ValueInput.createByString('2 mm'))
    holeInput.setPositionBySketchPoints(ptColl)

    th_cm = units.Distance(a_face.thickness, app_context.active_attrs.import_distance_units).cm
    distance = adsk.core.ValueInput.createByReal(th_cm)
    holeInput.setDistanceExtent(distance)

    hole = holes.add(holeInput)
    return hole

def is_main_face(face):
    # return false if face is subface of coplanar multiface
    # return true if face is face representative of multiface
    # return true if face is not multiface
    if face.coplanar_to is None:
        return True
    if len(face.coplanar_to) <= 1:
        return True
    if min(face.coplanar_to) == face.fidx:
        return True
    return False



def create_faces(face_list, bolt_list, skip_coplanar=True):


    make_fingers = True
    make_pads = True
    make_bridges = True
    make_phalanxes = True
    make_nodemark = True
    make_bolts = True
    weld = True


    for a_face in face_list:

        if not is_main_face(a_face):
            continue

        new_comp = app_context.createNewComponent()
        if new_comp is None:
            app_context.ui.messageBox('New component failed to create', 'New Component Failed')
            return

        main_body = build_object(a_face, new_comp)
        negative_bodies = adsk.core.ObjectCollection.create()

        if make_bolts:
            node_bolts = list()
            for blt in bolt_list:
                if blt.fidx == a_face.fidx:
                    node_bolts.append(blt)

            blts = fusion_bolt.Bolt(node_bolts, do_trunk=True, overshot=0.1)
            negative_bodies = fup.append_to_collection(blts.create_negative_bodies(new_comp), negative_bodies)


        if weld:
            combineFeatures = new_comp.features.combineFeatures
            combineFeatureInput = combineFeatures.createInput(main_body, negative_bodies)
            combineFeatureInput.isKeepToolBodies = False
            combineFeatureInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
            combineFeatureInput.isNewComponent = False
            combineFeatures.add(combineFeatureInput)