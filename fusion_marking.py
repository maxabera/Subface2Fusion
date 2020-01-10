__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

import adsk
import adsk.core
import adsk.fusion
import math

from . import app_context
from . import vector
from . import part_finger
from . import part_font
from . import part_bump
from .part_node import Node
from .part_node_marking import NodeMarking
from . import part_cradle

from . import fusion_extrusion
from . import fusion_parts
from . import fusion_sphere




class FingerMarking:

    def __init__(self, a_finger: part_finger.Finger, a_bump: part_bump.Bump, a_font: part_font.Font):

        self._font = a_font
        self._bump = a_bump
        self._finger = a_finger
        self._finger_bump = fusion_extrusion.FingerBump(a_finger, a_bump)
        self._finger_length = a_finger.length

        # bump_height and bump_width creates the area for number

        self._sqnum = a_finger.sq_num

        # self.text_height = 10 * a_font.size / 75  # suppose the real font size is only 75% convert mm to cm
        # self.text_width = a_font.size * 0.1
        # self.text_pos = [
        #     0, 0, self._finger_length - self._bump.height / 2
        # ]

        # intern
        self.width = 0  # Y
        self.height = 0  # Z
        self.depth = 0  # X

        self._positive_bodies = None
        self._negative_bodies = None

    @property
    def positive_bodies(self):
        return self._positive_bodies

    @property
    def negative_bodies(self):
        return self._negative_bodies

    def _name(self, prefix):
        return "{}_{:01d}".format(prefix, self._sqnum)

    def create_positive_bodies(self, new_comp):
        root_comp = app_context.design.rootComponent
        xy_plane = root_comp.xYConstructionPlane
        yz_plane = root_comp.yZConstructionPlane
        xz_plane = root_comp.xZConstructionPlane

        fi_bump = self._finger_bump
        constr_height = fi_bump.construction_height()

        coll_bump_bodies = fi_bump.extrude_polygon(new_comp, xy_plane, constr_height, name=self._name("bmp"))
        move_vec = [0, 0, self._finger_length - constr_height]
        moved_bump = self.move_bodies(new_comp, coll_bump_bodies, move_vec)

        fi_wedge = fusion_extrusion.FingerWedge(self._finger.outer_d * 2)
        wedge_h = self._finger.outer_d * 2
        coll_wedge_bodies = fi_wedge.extrude_polygon(new_comp, xz_plane, wedge_h, name=self._name("neg_w"))
        move_vec = [fi_bump._radius + fi_bump._bump_d, -fi_bump._radius * 2, self._finger_length - fi_bump._bump_h]
        moved_wedge = self.move_bodies(new_comp, coll_wedge_bodies, move_vec)

        negative_bodies = moved_wedge
        self.combine_cut_multiple(new_comp, moved_bump, negative_bodies)

        return moved_bump

    def build_object(self, new_comp):

        self._positive_bodies = self.create_positive_bodies(new_comp)
        self._negative_bodies = self.create_negative_bodies(new_comp)

        self.combine_cut(new_comp, self._positive_bodies.item(0), self._negative_bodies)

        return self._positive_bodies

    def create_negative_bodies(self, new_comp):

        root_comp = app_context.design.rootComponent
        xy_plane = root_comp.xYConstructionPlane
        yz_plane = root_comp.yZConstructionPlane
        xz_plane = root_comp.xZConstructionPlane

        depth = self._font.negative_depth
        text_plane = self.offset_construction_plane(yz_plane,
                                                    self._finger_bump._radius + self._finger_bump._bump_d - depth)

        text_string = "{}".format(self._sqnum)
        # self, new_comp, construction_plane, text, height, name = ""

        fi_text = fusion_extrusion.FingerText(self._font, text_string)
        text_bodies = fi_text.extrude_polygon(new_comp, text_plane, text_string)

        text_pos_y = -fi_text.text_width / 2
        text_pos_z = self._finger_length - self._finger_bump._bump_h / 2 - fi_text.text_height / 2

        self.move_bodies(new_comp, text_bodies, [0, text_pos_y, text_pos_z])

        return text_bodies

    def move_bodies(self, new_comp, bodies_collection, move_vec):

        if vector.is_zero(move_vec):
            return None

        move_vector = adsk.core.Vector3D.create(move_vec[0], move_vec[1], move_vec[2])
        move_matrix = adsk.core.Matrix3D.create()
        move_matrix.translation = move_vector
        move_feats = new_comp.features.moveFeatures
        move_feature_input = move_feats.createInput(bodies_collection, move_matrix)
        move_feats.add(move_feature_input)
        return bodies_collection

    def combine_cut(self, new_comp, primary_body, cut_bodies):

        combineFeatures = new_comp.features.combineFeatures
        combineFeatureInput = combineFeatures.createInput(primary_body, cut_bodies)
        combineFeatureInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        combineFeatureInput.isKeepToolBodies = False
        combineFeatureInput.isNewComponent = False
        new_obj = combineFeatures.add(combineFeatureInput)

        return new_obj

    def combine_cut_multiple(self, new_comp, coll_primary_b, coll_cut_bodies):
        for i in range(coll_primary_b.count):
            main_body = coll_primary_b.item(i)
            combineFeatures = new_comp.features.combineFeatures
            combineFeatureInput = combineFeatures.createInput(main_body, coll_cut_bodies)
            if i == range(coll_primary_b.count)[-1]:  # if last body
                combineFeatureInput.isKeepToolBodies = False
            else:  # not last body
                combineFeatureInput.isKeepToolBodies = True
            combineFeatureInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
            combineFeatureInput.isNewComponent = False
            combineFeatures.add(combineFeatureInput)

        return coll_primary_b

    def extrude_symetric_polygon(self, newComp, constPlane, poly, height, name=""):
        """

        :param newComp: component
        :param constPlane: newComp.xYConstructionPlane or zYConstructionPlane
        :param poly: polygon to extrude
        :param height: extrude distance
        :param name: name of the created body
        :return: body or None if failed
        """

        # Create a new sketch.
        sketches = newComp.sketches
        sketch0 = sketches.add(constPlane)

        self._draw_poly(sketch0, poly)

        prof = sketch0.profiles.item(0)

        # extrude
        extrudes = newComp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        distance = adsk.core.ValueInput.createByReal(height)
        distanceDefinition = adsk.fusion.SymmetricExtentDefinition.create(distance, False)
        extrudeInput.setSymmetricExtent(distanceDefinition, False)
        obj = extrudes.add(extrudeInput)

        if obj.bodies.count > 0:
            body = obj.bodies.item(0)
            body.name = name

        return obj

    def offset_construction_plane(self, basis_plane, offset):

        root_comp = app_context.design.rootComponent
        # Get construction planes
        planes = root_comp.constructionPlanes
        # Create construction plane input
        plane_input = planes.createInput()

        # Add construction plane by offset
        offset_value = adsk.core.ValueInput.createByReal(offset)
        plane_input.setByOffset(basis_plane, offset_value)
        new_plane = planes.add(plane_input)

        return new_plane




class NodeMarkingMiddle:

    def __init__(self, a_node_id, a_node_marking: NodeMarking, a_cradle: part_cradle.Cradle, a_font: part_font.Font):

        self.node_id = a_node_id
        self._node_mark = a_node_marking
        self._cradle = a_cradle
        self._font = a_font

        self._positive_bodies = None
        self._negative_bodies = None

    def build_object(self, new_comp):

        self._positive_bodies = self.create_positive_bodies(new_comp)
        self._negative_bodies = self.create_negative_bodies(new_comp)

        # self.combine_cut(new_comp, self._positive_bodies.item(0), self._negative_bodies)

        return self._positive_bodies

    def create_positive_bodies(self, new_comp):
        root_comp = app_context.design.rootComponent
        xy_plane = root_comp.xYConstructionPlane
        yz_plane = root_comp.yZConstructionPlane
        xz_plane = root_comp.xZConstructionPlane

        radius = self._cradle.ball_d/2
        sphere = fusion_sphere.build_object_translated(radius, new_comp, math.pi, self._node_mark.t_matrix)

        hx = fusion_extrusion.Hexagon()
        hexagon = hx.extrude_polygon_up_down(new_comp, xy_plane, transl_mat=self._node_mark.t_matrix)

        combineFeatures = new_comp.features.combineFeatures
        combineFeatureInput = combineFeatures.createInput(sphere.item(0), hexagon)

        combineFeatureInput.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation
        combineFeatureInput.isKeepToolBodies = False
        combineFeatureInput.isNewComponent = False
        combineFeatures.add(combineFeatureInput)

        nt = fusion_extrusion.Notch(side_a=2)
        notch = nt.extrude_polygon_up_down(new_comp, xy_plane, transl_mat=self._node_mark.t_matrix)

        combineFeatures = new_comp.features.combineFeatures
        combineFeatureInput = combineFeatures.createInput(sphere.item(0), notch)
        combineFeatureInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        combineFeatureInput.isKeepToolBodies = False
        combineFeatureInput.isNewComponent = False
        combineFeatures.add(combineFeatureInput)

        fnt = part_font.Font()
        txt = "{}.".format(self.node_id)
        ct = fusion_extrusion.CenterText(fnt, txt, up=5, down=5)
        text = ct.extrude_polygon_up_down(new_comp, xy_plane, transl_mat=self._node_mark.t_matrix)

        combineFeatures = new_comp.features.combineFeatures
        combineFeatureInput = combineFeatures.createInput(sphere.item(0), text)
        combineFeatureInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        combineFeatureInput.isKeepToolBodies = False
        combineFeatureInput.isNewComponent = False
        combineFeatures.add(combineFeatureInput)

        return sphere

    def create_negative_bodies(self, new_comp):
        root_comp = app_context.design.rootComponent
        xy_plane = root_comp.xYConstructionPlane
        yz_plane = root_comp.yZConstructionPlane
        xz_plane = root_comp.xZConstructionPlane

        fnt = part_font.Font()
        txt = "{}.".format(self.node_id)
        ct = fusion_extrusion.CenterText(fnt, txt, up=5, down=5)
        text = ct.extrude_polygon_up_down(new_comp, xy_plane, transl_mat=self._node_mark.t_matrix)

        return text



class NodeMarkingPadEdge:

    def __init__(self, a_node_id, a_node_marking: NodeMarking, a_cradle: part_cradle.CradleWedge, a_font: part_font.Font):

        self.node_id = a_node_id
        self._node_mark = a_node_marking
        self._cradle = a_cradle
        self._font = a_font

        self._positive_bodies = None
        self._negative_bodies = None

    def build_object(self, new_comp):

        self._positive_bodies = self.create_positive_bodies(new_comp)
        self._negative_bodies = self.create_negative_bodies(new_comp)

        # self.combine_cut(new_comp, self._positive_bodies.item(0), self._negative_bodies)

        return self._positive_bodies

    def create_positive_bodies(self, new_comp):
        root_comp = app_context.design.rootComponent
        xy_plane = root_comp.xYConstructionPlane
        yz_plane = root_comp.yZConstructionPlane
        xz_plane = root_comp.xZConstructionPlane

        cw_xy = fusion_extrusion.CradleWedgeXY()
        cwxy_objs = cw_xy.extrude_polygon_up_down(new_comp, xy_plane, "", self._node_mark.t_matrix)

        cw_yz = fusion_extrusion.CradleWedgeYZ()
        cwyz_objs = cw_yz.extrude_polygon_up_down(new_comp, yz_plane, "", self._node_mark.t_matrix)

        combineFeatures = new_comp.features.combineFeatures
        combineFeatureInput = combineFeatures.createInput(cwxy_objs.item(0), cwyz_objs)
        combineFeatureInput.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation
        combineFeatureInput.isKeepToolBodies = False
        combineFeatureInput.isNewComponent = False
        combineFeatures.add(combineFeatureInput)

        # fnt = part_font.Font()
        # txt = "{}.".format(self.node_id)
        # ct = fusion_extrusion.CenterText(fnt, txt, up=5, down=1)
        # ct.angle = 0
        # text = ct.extrude_polygon_up_down(new_comp, xy_plane) # , transl_mat=self._node_mark.t_matrix)

        # combineFeatures = new_comp.features.combineFeatures
        # combineFeatureInput = combineFeatures.createInput(cwxz_objs.item(0), text)
        # combineFeatureInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        # combineFeatureInput.isKeepToolBodies = False
        # combineFeatureInput.isNewComponent = False
        # combineFeatures.add(combineFeatureInput)

        return cwxy_objs

    def create_negative_bodies(self, new_comp):

        root_comp = app_context.design.rootComponent
        xy_plane = root_comp.xYConstructionPlane
        yz_plane = root_comp.yZConstructionPlane
        xz_plane = root_comp.xZConstructionPlane

        fnt = part_font.Font()
        txt = "{}.".format(self.node_id)
        ct = fusion_extrusion.CenterText(fnt, txt, up=5, down=1)
        ct.angle = 0
        text = ct.extrude_polygon_up_down(new_comp, xy_plane, transl_mat=self._node_mark.t_matrix)

        return text