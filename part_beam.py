__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from . import json_strings as JS
from . import vector
from .part import Part
from .units import Unit
from . import matrix

from typing import List
import math



class Beam(Part):

    def __init__(self):
        super().__init__()

        # core data

        self.beam_id = -1
        self.node_idx0 = -1
        self.node_idx1 = -1

        # halfedges
        self.heidx0 = -1
        self.heidx1 = -1

        # position
        self._start = [0, 0, 0]
        self._end = [0, 0, 100]
        self._direction_vector = [100, 100, 0]  # opposite of middle vector of both normal vectors

        # dimensions
        self._outer_d = 10
        self._inner_d = 8

        # faces
        self._face_angle = math.pi/2
        self.fidx0 = -1
        self.fidx1 = -1

        # fingers
        self.fiisqn0 = -1
        self.fiisqn1 = -1
        self.fiidx0 = -1  # finger0 index
        self.fiidx1 = -1  # finger1 index
        self.fii_len0 = 0  # finger0 length
        self.fii_len1 = 0  # finger1 length

        # manufacturing infor
        self.cart_position = "1A5"
        self.is_ignored = False

        # transformation
        self._x_base0 = [0, 0, 1]
        self._x_base1 = [0, 0, 1]
        self._tm = matrix.identity(4)  # transformation matrix

        # near bolts distance
        self._inc_distance = 0
        self._out_distance = 0

    def name(self):
        return "beam{}_{}".format(self.node_idx0, self.node_idx1)

    @property
    def length(self):
        return vector.magnitude([self.start, self.end])

    @property
    def visible_length(self):
        return self.length - self.fii_len0 - self.fii_len1

    @property
    def netto_length(self):  # cut_length
        return self.length

    @property
    def inc_bolts_distance(self):
        return self.distance(self._inc_distance)

    def set_inc_bolts_distance(self, value, input_unit: Unit.millimeter):
        self._inc_distance = self.set_distance(value, input_unit)

    @property
    def direction(self):
        return self.vector(self._direction_vector)

    def set_direction(self, direction3d, input_unit=Unit.millimeter):
        self._direction_vector = self.set_vector(direction3d, input_unit)

    @property
    def start(self):
        return self.point_3d(self._start)

    def set_start(self, point3d, input_unit=Unit.millimeter):
        self._start = self.set_point3d(point3d, input_unit)

    @property
    def end(self):
        return self.point_3d(self._end)

    def set_end(self, point3d, input_unit=Unit.millimeter):
        self._end = self.set_point3d(point3d, input_unit)

    @property
    def face_angle(self):
        return self._face_angle

    def set_face_angle(self, angle, input_unit=Unit.radian):
        self._face_angle = self.set_angle(angle, input_unit)

    @property
    def outer_d(self):
        return self.distance(self._outer_d)

    @outer_d.setter
    def outer_d(self, value):
        self._outer_d = self.set_distance(value, self.input_distance_units)

    def set_outer_d(self, value, distance_unit=None):
        if distance_unit is None:
            distance_unit = self.input_distance_units
        self._outer_d = self.set_distance(value, distance_unit)

    @property
    def inner_d(self):
        return self.distance(self._inner_d)

    @inner_d.setter
    def inner_d(self, value):
        self._inner_d = self.set_distance(value, self.input_distance_units)

    def set_inner_d(self, value, distance_unit=None):
        if distance_unit is None:
            distance_unit = self.input_distance_units
        self._inner_d = self.set_distance(value, distance_unit)

    @property
    def out_bolts_distance(self):
        return self.distance(self._out_distance)

    def set_out_bolts_distance(self, value, input_unit: Unit.millimeter):
        self._out_distance = self.set_distance(value, input_unit)

    @property
    def fii_len0(self):
        return self.distance(self._fii_len0)

    @fii_len0.setter
    def fii_len0(self, value):
        self._fii_len0 = self.set_distance(value, self.input_distance_units)

    def set_fii_len0(self, value, distance_unit=None):
        if distance_unit is None:
            distance_unit = self.input_distance_units
        self._fii_len0 = self.set_distance(value, distance_unit)

    @property
    def x_base0(self):
        return self.vector(self._x_base0)

    def set_xbase0(self, direction3d, input_unit=Unit.millimeter):
        self._x_base0 = self.set_vector(direction3d, input_unit)

    @property
    def x_base1(self):
        return self.vector(self._x_base1)

    def set_xbase1(self, direction3d, input_unit=Unit.millimeter):
        self._x_base1 = self.set_vector(direction3d, input_unit)

    @property
    def t_matrix(self):
        return self.matrix(self._tm)

    def set_t_matrix(self, tm, input_unit=Unit.millimeter):
        self._tm = self.set_matrix(tm, input_unit)

    @property
    def fii_len1(self):
        return self.distance(self._fii_len1)

    @fii_len1.setter
    def fii_len1(self, value):
        self._fii_len1 = self.set_distance(value, self.input_distance_units)

    def set_fii_len1(self, value, distance_unit=None):
        if distance_unit is None:
            distance_unit = self.input_distance_units
        self._fii_len1 = self.set_distance(value, distance_unit)

    def equal(self, new_beam):
        if self.heidx0 == new_beam.inc_heidx and self.heidx1 == new_beam.out_heidx:
            return True
        if self.heidx0 == new_beam.out_heidx and self.heidx1 == new_beam.inc_heidx:
            return True
        return False


    def to_dict(self):

        face_json = {

            JS.ID: self.beam_id,
            JS.NODE_IDX0: self.node_idx0,
            JS.NODE_IDX1: self.node_idx1,

            JS.HEIDX0: self.heidx0,
            JS.HEIDX1: self.heidx1,

            JS.BEAM_START: self.start,
            JS.BEAM_END: self.end,
            JS.DIRECTION: self.direction,

            JS.INNER_DIAMETER: self.inner_d,
            JS.OUTSIDE_DIAMETER: self.outer_d,

            JS.FACE_ANGLE: self.face_angle,
            JS.FIDX0: self.fidx0,
            JS.FIDX1: self.fidx1,

            JS.FIISQN0: self.fiisqn0,
            JS.FIISQN1: self.fiisqn1,
            JS.FIIDX0: self.fiidx0,
            JS.FIIDX1: self.fiidx1,
            JS.FIILEN0: self.fii_len0,
            JS.FIILEN1: self.fii_len1,
            #
            JS.BEAM_CART_POS: self.cart_position,
            JS.IS_IGNORED: self.is_ignored,

            JS.XBASE0: self.x_base0,
            JS.XBASE1: self.x_base1,
            JS.TRANSFORMATION_MATRIX: self.t_matrix
        }
        return face_json

    @staticmethod
    def create_list_dict(list_of_faces: List['Beam']):
        dict_list_faces = list()
        for h in list_of_faces:
            dict_hole = h.to_dict()
            dict_list_faces.append(dict_hole)
        return dict_list_faces

    @staticmethod
    def create_from_dict(json_beam, distance_units=Unit.millimeter):
        b = Beam()

        b.beam_id = json_beam.get(JS.ID, -1)
        b.node_idx0 = json_beam.get(JS.NODE_IDX0, -1)
        b.node_idx1 = json_beam.get(JS.NODE_IDX1, -1)

        b.heidx0 = json_beam.get(JS.HEIDX0, -1)
        b.heidx1 = json_beam.get(JS.HEIDX1, -1)

        b.set_start(json_beam.get(JS.BEAM_START, [0, 0, 0]), distance_units)
        b.set_end(json_beam.get(JS.BEAM_END, [0, 0, 10]), distance_units)
        b.set_direction(json_beam.get(JS.DIRECTION, [0, 0, 10]), distance_units)

        b.set_inner_d(json_beam.get(JS.INNER_DIAMETER, 8), distance_units)
        b.set_outer_d(json_beam.get(JS.OUTSIDE_DIAMETER, 10), distance_units)

        b.set_face_angle(json_beam.get(JS.FACE_ANGLE, math.pi/2), Unit.radian)
        b.fidx0 = json_beam.get(JS.FIDX0, -1)
        b.fidx1 = json_beam.get(JS.FIDX1, -1)

        b.fiisqn0 = json_beam.get(JS.FIISQN0, -1)
        b.fiisqn1 = json_beam.get(JS.FIISQN1, -1)

        b.fiidx0 = json_beam.get(JS.FIIDX0, -1)
        b.fiidx1 = json_beam.get(JS.FIIDX1, -1)

        b.fii_len0 = json_beam.get(JS.FIILEN0, -1)
        b.fii_len1 = json_beam.get(JS.FIILEN1, -1)

        b.set_xbase0(json_beam.get(JS.XBASE0, [0, 0, 10]), distance_units)
        b.set_xbase1(json_beam.get(JS.XBASE1, [0, 0, 10]), distance_units)
        b.set_t_matrix(json_beam.get(JS.TRANSFORMATION_MATRIX, matrix.identity(4)), distance_units)

        b.cart_position = json_beam.get(JS.BEAM_CART_POS, '---')
        b.is_ignored = json_beam.get(JS.IS_IGNORED, 'False')

        return b

    @staticmethod
    def create_list_from_dict(dict_face_list):
        list_of_faces = list()
        for dh in dict_face_list:
            h = Beam.create_from_dict(dh)
            list_of_faces.append(h)
        return list_of_faces

