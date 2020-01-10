import adsk
import adsk.core
import adsk.fusion
from typing import List

from . fusion_parts import FusionPart
from .part_bolt import Bolt as PartBolt
from . import fusion_parts

from .part_bolt import BoltType as PartBoltType
from . import matrix


class Bolt(FusionPart):

    def __init__(self, list_of_bolts: List['PartBolt'], do_trunk=True, overshot=0.1):
        super().__init__()

        self._list_of_bolts = list_of_bolts  # bolts must be on same plane
        self.do_trunk = do_trunk  # if True bolt will be created on the xy plane and positive Z extruded
        self.overshot = overshot # distance to start below or above construction plane

    # def create_positive_bodies() not overloaded

    def bolt_diameter(self, b: PartBolt):

        if self.do_trunk:
            return b.trunk_diameter

        return b.tail_diameter

    def create_negative_bodies(self, new_comp):

        bolt_bodies = adsk.core.ObjectCollection.create()
        for b in self._list_of_bolts:
            r = self.bolt_diameter(b)/2.0
            length = b.min_length * 1.1  # add 10% of the length
            if self.do_trunk:
                up = length
                down = self.overshot
            else:
                up = self.overshot
                down = length
            tm = b.t_matrix
            fb = self.build_cylinder(new_comp, r, up, down, tm)  # fusion bolt

            bolt_bodies.add(fb)
        return bolt_bodies


    def draw_circle(self, circle_sketch, xy_pos, radius):

        if radius <= 0:
            return

        p0 = adsk.core.Point3D.create(xy_pos[0], xy_pos[1], 0)
        # create beam profile
        if radius > 0:
            circle_sketch.addByCenterRadius(p0, radius)  # outer circle


    def build_cylinder(self, new_comp, radius, up, down, t_matrix):
        """
        :param new_comp:
        :param radius:
        :return:
        """
        assert (radius > 0)

        # Create a new sketch.
        sketches = new_comp.sketches
        xyPlane = new_comp.xYConstructionPlane
        sketch0 = sketches.add(xyPlane)

        circles = sketch0.sketchCurves.sketchCircles

        # draw circle on the sketch
        self.draw_circle(circles, [0, 0], radius)

        adsk_up = adsk.core.ValueInput.createByReal(up)
        adsk_down = adsk.core.ValueInput.createByReal(down)

        prof = sketch0.profiles.item(0)
        extrudes = new_comp.features.extrudeFeatures
        extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        up_def = adsk.fusion.DistanceExtentDefinition.create(adsk_up)
        down_def = adsk.fusion.DistanceExtentDefinition.create(adsk_down)

        extrude_input.setTwoSidesExtent(up_def, down_def)

        obj = extrudes.add(extrude_input)

        obj_collection = adsk.core.ObjectCollection.create()
        # add finger tubes
        for i in range(obj.bodies.count):
            obj_collection.add(obj.bodies.item(i))

        if t_matrix is not None:
            if not matrix.is_zero(t_matrix):
                transform = adsk.core.Matrix3D.create()
                tm_serialized = matrix.serialize(t_matrix)
                transform.setWithArray(tm_serialized)
                moveFeats = new_comp.features.moveFeatures
                moveFeatureInput = moveFeats.createInput(obj_collection, transform)
                moveFeats.add(moveFeatureInput)

        return obj_collection.item(0)


