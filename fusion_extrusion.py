__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

import math

import adsk
import adsk.core
import adsk.fusion

from . import part_font
from . import fusion_parts
from . import units

class PolygonExtrusion:

    def __init__(self):
        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter
        self.input_angle_units = units.Unit.radian
        self.output_angle_units = units.Unit.degree
        self._up = 5
        self._down = 10

    @property
    def up(self):
        v = units.distance(self._up, self.input_distance_units, self.output_distance_units)
        return v

    @property
    def down(self):
        v = units.distance(self._down, self.input_distance_units, self.output_distance_units)
        return v

    def _draw_poly(self, sketch, poly):
        sketch_lines = sketch.sketchCurves.sketchLines
        n_points = len(poly)
        for i in range(n_points - 1):
            p0 = poly[i]
            p1 = poly[i + 1]
            sketch_lines.addByTwoPoints(adsk.core.Point3D.create(p0[0], p0[1], p0[2]),
                                        adsk.core.Point3D.create(p1[0], p1[1], p1[2]))
        p0 = poly[-1]
        p1 = poly[0]

        sketch_lines.addByTwoPoints(adsk.core.Point3D.create(p0[0], p0[1], p0[2]),
                                    adsk.core.Point3D.create(p1[0], p1[1], p1[2]))

    def _create_poly(self):
        a = 10 / 2  # square with size 10
        poly = [
            [-a, -a, 0],
            [a, -a, 0],
            [a, a, 0],
            [-a, a, 0]
        ]
        return poly

    def extrude_polygon(self, new_comp, constr_plane, height, name="", transl_mat=None):
        """

        :param new_comp: component
        :param constr_plane: newComp.xYConstructionPlane or zYConstructionPlane
        :param poly: polygon to extrude
        :param height: extrude distance
        :param name: name of the created body
        :return: body or None if failed
        """

        # Create a new sketch.
        sketches = new_comp.sketches
        sketch0 = sketches.add(constr_plane)

        poly = self._create_poly()
        self._draw_poly(sketch0, poly)

        prof = sketch0.profiles.item(0)

        # extrude
        extrudes = new_comp.features.extrudeFeatures
        extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        distance = adsk.core.ValueInput.createByReal(height)
        distance_definition = adsk.fusion.DistanceExtentDefinition.create(distance)
        extrude_input.setOneSideExtent(distance_definition, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        obj = extrudes.add(extrude_input)

        obj_collect = adsk.core.ObjectCollection.create()

        if obj.bodies.count == 1:  # single body
            body = obj.bodies.item(0)
            if len(name) > 0:
                body.name = name
            obj_collect.add(body)
        else:  # multiple bodies or empty
            for i in range(obj.bodies.count):
                body = obj.bodies.item(i)
                body.name = "{}_{}".format(name, i)
                obj_collect.add(body)

        if transl_mat is not None:
            fusion_parts.translate(new_comp,obj_collect, transl_mat )

        return obj_collect

    def extrude_polygon_up_down(self, new_comp, constr_plane, name="", transl_mat=None):
        """

        :param new_comp: component
        :param constr_plane: newComp.xYConstructionPlane or zYConstructionPlane
        :param poly: polygon to extrude
        :param height: extrude distance
        :param name: name of the created body
        :return: body or None if failed
        """

        # Create a new sketch.
        sketches = new_comp.sketches
        sketch0 = sketches.add(constr_plane)

        poly = self._create_poly()
        self._draw_poly(sketch0, poly)

        prof = sketch0.profiles.item(0)

        # extrude
        extrudes = new_comp.features.extrudeFeatures
        extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        ddef_up = adsk.core.ValueInput.createByReal(self.up)
        ddef_down = adsk.core.ValueInput.createByReal(self.down)

        distance_up = adsk.fusion.DistanceExtentDefinition.create(ddef_up)
        distance_down = adsk.fusion.DistanceExtentDefinition.create(ddef_down)
        extrude_input.setTwoSidesExtent(distance_up, distance_down)
        obj = extrudes.add(extrude_input)

        obj_collect = adsk.core.ObjectCollection.create()

        if obj.bodies.count == 1:  # single body
            body = obj.bodies.item(0)
            if len(name) > 0:
                body.name = name
            obj_collect.add(body)
        else:  # multiple bodies or empty
            for i in range(obj.bodies.count):
                body = obj.bodies.item(i)
                body.name = "{}_{}".format(name, i)
                obj_collect.add(body)

        if transl_mat is not None:
            fusion_parts.translate(new_comp,obj_collect, transl_mat )

        return obj_collect



    @staticmethod
    def center_y(bounding_box):
        return (bounding_box.maxPoint.y + bounding_box.minPoint.y) / 2

    @staticmethod
    def collection_bbox(body_collection):
        """
        bounding box of the collection
        summary bounding box of all bodies in collection
        """

        n = body_collection.count
        assert (n > 0)
        body = body_collection.item(0)
        max_point = body.boundingBox.maxPoint
        min_point = body.boundingBox.minPoint

        n = body_collection.count
        for i in range(1, n):
            body = body_collection.item(i)
            if max_point.x < body.boundingBox.maxPoint.x:
                max_point.x = body.boundingBox.maxPoint.x
            if max_point.y < body.boundingBox.maxPoint.y:
                max_point.y = body.boundingBox.maxPoint.y
            if max_point.z < body.boundingBox.maxPoint.z:
                max_point.z = body.boundingBox.maxPoint.z
            if min_point.x > body.boundingBox.minPoint.x:
                min_point.x = body.boundingBox.minPoint.x
            if min_point.y > body.boundingBox.minPoint.y:
                min_point.y = body.boundingBox.minPoint.y
            if min_point.z > body.boundingBox.minPoint.z:
                min_point.z = body.boundingBox.minPoint.z

        return min_point, max_point

class FingerBump(PolygonExtrusion):

    def __init__(self, a_finger, a_bump):
        super().__init__()

        # construction data
        self._bump_h = a_bump.height
        self._bump_m = a_bump.width / 2
        self._bump_d = a_bump.delta  # perpendicular distance distance from cylinder
        self._radius = a_finger.outer_d / 2
        self._finger_length = a_finger.length

    def construction_height(self):
        constr_height = self._bump_h + (self._radius + self._bump_d) + 0.1  # defined height + 't' to be cut by wedge
        return constr_height

    def _calculate_bump_k(self, r, d, m):
        t = r + d
        g_sq = m * m + t * t
        v_sq = g_sq - r * r
        v = math.sqrt(v_sq)
        g = math.sqrt(g_sq)
        tau = math.asin(v / g)
        delta = math.atan(m / t)
        gama = math.pi / 2 - delta - tau
        b = v * math.cos(gama)
        a = v * math.sin(gama)
        k = a + m
        l = t - b
        self.width = 2 * k
        self.depth = t - l
        return l, k

    def _create_poly(self):
        d = self._bump_d
        m = self._bump_m
        r = self._radius

        l, k = self._calculate_bump_k(r, d, m)

        t = d + r
        poly = [

            [l, -k, 0],
            [t, -m, 0],
            [t, m, 0],
            [l, k, 0]
        ]
        return poly


class FingerWedge(PolygonExtrusion):

    def __init__(self, size):
        super().__init__()

        self._size = size

    def _create_poly(self):
        dd = self._size
        poly = [
            [-dd, dd, 0],
            [dd, dd, 0],
            [dd, -dd, 0]
        ]
        return poly

class FingerText(PolygonExtrusion):

    def __init__(self, font: part_font.Font, text=""):
        super().__init__()
        self._font = font
        self.text = text

        self.text_width = 0
        self.text_height = 0

    def extrude_polygon(self, new_comp, construction_plane, height, name="", transl_mat=None):
        # Create a new sketch.
        sketches = new_comp.sketches
        sketch = sketches.add(construction_plane)

        # Get sketch texts
        sketchTexts = sketch.sketchTexts

        # Create sketch text input
        point = adsk.core.Point3D.create(0.0, 0.0, 0.0)
        # formattedText, height, position

        sketchTextInput = sketchTexts.createInput(self.text, self._font.size, point)
        # Set sketch text style
        sketchTextInput.textStyle = adsk.fusion.TextStyles.TextStyleBold
        sketchTextInput.angle = math.pi / 2
        sketchTextInput.fontName = self._font.font_name

        sketchTexts.add(sketchTextInput)

        # prof = sketch.profiles.item(0)
        prof = sketch.sketchTexts.item(0)

        # Define that the extent is a distance extent of 5 cm.
        distance = adsk.core.ValueInput.createByReal(0.5)
        # Create the extrusion.
        extrudes = new_comp.features.extrudeFeatures
        ext = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        move_objs = adsk.core.ObjectCollection.create()
        # print("ext.bodies.count: ", ext.bodies.count)

        for i in range(ext.bodies.count):
            move_objs.add(ext.bodies.item(i))

        min_point, max_point = self.collection_bbox(move_objs)

        self.text_width = max_point.y - min_point.y
        self.text_height = max_point.z - min_point.z

        return move_objs


class NodeMarkingPad(PolygonExtrusion):

    def __init__(self, size=1, height=0.5):
        super().__init__()
        self._size = size
        self._height = height

    def _create_poly(self):
        a = self._size / 2
        q = self._size / 4
        c = a + q
        i = self._size / 10
        d = a - i
        poly = [
            [-a, -a, 0],  # 0
            [a, -a, 0],  # 1
            [c, 0, 0],
            [a, a, 0],
            [i, a, 0],
            [0, d, 0],
            [-i, a, 0],
            [-a, a, 0],  # 6
            [-c, 0, 0]  # 7
        ]
        return poly


class Hexagon(PolygonExtrusion):


    def __init__(self, circum_d = 16, up=10, down=10):
        super().__init__()

        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter

        self._d = circum_d
        self._up = up
        self._down = down

    @property
    def d(self):
        return units.distance(self._d, self.input_distance_units, self.output_distance_units)

    def _create_poly(self):

        r = self.d/2.0

        sq3 = math.sqrt(3)
        poly = [
            [r, 0, 0],
            [r/2, r*sq3/2, 0],
            [- r / 2, r * sq3 / 2, 0],
            [-r, 0, 0],
            [-r / 2, -r * sq3 / 2, 0],
            [r / 2, -r * sq3 / 2, 0],
        ]

        return poly


class Notch(PolygonExtrusion):


    def __init__(self, circum_d = 16, side_a = 1, up=10, down=10):
        super().__init__()

        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter

        self._d = circum_d
        self._side_a = side_a
        self._up = up
        self._down = down


    @property
    def d(self):
        return units.distance(self._d, self.input_distance_units, self.output_distance_units)

    @property
    def side_a(self):
        return units.distance(self._side_a, self.input_distance_units, self.output_distance_units)

    def _create_poly(self):

        r = self.d/2.0
        a = self.side_a

        sq3 = math.sqrt(3)
        poly = [
            [0, (r * sq3 / 2) - a, 0],
            [a, r * sq3 / 2, 0],
            [0, (r * sq3 / 2) + a, 0],
            [-a, r * sq3 / 2, 0],
        ]

        return poly



class CenterText(PolygonExtrusion):

    def __init__(self, font: part_font.Font, text="", up=2, down=2):
        super().__init__()
        self._font = font
        self.text = text
        self.angle = 0

        self._text_width = 0
        self._text_height = 0
        self._zero_point = [0, 0, 0]

        self._up = up
        self._down = down

    @property
    def text_width(self):
        return units.distance(self._text_width, self.input_distance_units, self.output_distance_units)

    @property
    def text_height(self):
        return units.distance(self._text_height, self.input_distance_units, self.output_distance_units)

    @text_height.setter
    def text_height(self, value, dist_units=None ):
        if dist_units is None:
            dist_units = self.input_distance_units
        self._text_height = units.distance(value,  self.output_distance_units, dist_units)

    @text_width.setter
    def text_width(self, value, dist_units=None ):
        if dist_units is None:
            dist_units = self.input_distance_units
        self._text_width = units.distance(value,  self.output_distance_units, dist_units)


    def extrude_polygon_up_down(self, new_comp, constr_plane, name="", transl_mat=None):
        # Create a new sketch.
        sketches = new_comp.sketches
        sketch = sketches.add(constr_plane)

        # Get sketch texts
        sketchTexts = sketch.sketchTexts

        # Create sketch text input
        point = adsk.core.Point3D.create(0.0, 0.0, 0.0)
        # formattedText, height, position

        sketchTextInput = sketchTexts.createInput(self.text, self._font.size, point)
        # Set sketch text style
        sketchTextInput.textStyle = adsk.fusion.TextStyles.TextStyleBold
        sketchTextInput.angle = self.angle
        sketchTextInput.fontName = self._font.font_name

        sketchTexts.add(sketchTextInput)

        # prof = sketch.profiles.item(0)
        prof = sketch.sketchTexts.item(0)

        # extrude
        extrudes = new_comp.features.extrudeFeatures
        extrude_input = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        ddef_up = adsk.core.ValueInput.createByReal(self.up)
        ddef_down = adsk.core.ValueInput.createByReal(self.down)

        distance_up = adsk.fusion.DistanceExtentDefinition.create(ddef_up)
        distance_down = adsk.fusion.DistanceExtentDefinition.create(ddef_down)
        extrude_input.setTwoSidesExtent(distance_up, distance_down)

        # Create the extrusion.
        extrudes = new_comp.features.extrudeFeatures
        extrude_input.setTwoSidesExtent(distance_up, distance_down)
        obj = extrudes.add(extrude_input)

        obj_collect = adsk.core.ObjectCollection.create()

        for i in range(obj.bodies.count):
            obj_collect.add(obj.bodies.item(i))

        min_point, max_point = self.collection_bbox(obj_collect)

        dx = self.text_width = max_point.x - min_point.x
        dy = self.text_height = max_point.y - min_point.y

        move_vec = [-dx/2, -dy/2, -0.2]
        fusion_parts.move_bodies(new_comp, obj_collect, move_vec)

        if transl_mat is not None:
            fusion_parts.translate(new_comp, obj_collect, transl_mat )


        return obj_collect


class CradleWedgeXY(PolygonExtrusion):


    def __init__(self, basic_a = 8, up=0, down=10):
        super().__init__()

        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter

        self._a = basic_a
        self._up = up
        self._down = down

    @property
    def a(self):
        return units.distance(self._a, self.input_distance_units, self.output_distance_units)

    def _create_poly(self):

        a = self.a
        b = a/2
        poly = [
            [a, -b, 0],
            [a+b, 0, 0],
            [a, a-b, 0],
            [-a, a-b, 0],
            [-a-b, 0, 0],
            [-a, -b, 0]
        ]

        return poly

class CradleWedgeYZ(PolygonExtrusion):


    def __init__(self, basic_a = 8, depth = 2, up=16, down=16):
        super().__init__()

        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter

        self._a = basic_a
        self._d = depth

        self._up = up
        self._down = down

    @property
    def a(self):
        return units.distance(self._a, self.input_distance_units, self.output_distance_units)

    @property
    def d(self):
        return units.distance(self._d, self.input_distance_units, self.output_distance_units)

    def _create_poly(self):
        a = self.a
        b = a/2
        d = self.d
        poly = [
            [-d,    -b - d - d, 0],
            [ d + b, 0,         0],
            [-d,     b + d + d, 0]
        ]

        return poly


