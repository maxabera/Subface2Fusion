__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from . import json_strings as JS
from . import vector
from typing import List
from .part import Part
from . import units
from . import matrix

class Beam(Part):

    def __init__(self):
        super().__init__()

        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter

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
        self.direction_vector = [100, 100, 0]  # opposit of middle vector of both normal vectors
        self._face_nv0 = [0, -100, 0]  # normal vector of the face 0
        self._face_nv1 = [-100, 0, 0]  # normal vector of the face 1

        # dimensions
        self._outer_d = 10
        self._inner_d = 8

        # faces
        self.face_angle = 90
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
        self._cart_position = "1A5"
        self.is_ignored = False

        # transformation
        # transformation
        self.x_base0 = [0, 0, 1]
        self.x_base1 = [0, 0, 1]
        self.tm = None  # transformation matrix

    def name(self):
        return "beam_{:03d}_{:03d}".format(self.node_idx0, self.node_idx1)

    @property
    def length(self):
        return vector.magnitude([self.start, self.end])

    @property
    def visible_length(self):
        return self.length - self.fii_len0 - self.fii_len1

    @property
    def netto_length(self):  # cut_length
        return self.length

    def equal(self, new_beam):
        if self.heidx0 == new_beam.inc_heidx and self.heidx1 == new_beam.out_heidx:
            return True
        if self.heidx0 == new_beam.out_heidx and self.heidx1 == new_beam.inc_heidx:
            return True
        return False

    @property
    def inner_d(self):
        return self.distance(self._inner_d)

    @property
    def outer_d(self):
        return self.distance(self._outer_d)

    @property
    def start(self):
        return self.point_3d(self._start)

    @property
    def end(self):
        return self.point_3d(self._end)

    def to_dict(self):
        face_json = {

            JS.ID: self.beam_id,
            JS.NODE_IDX0: self.node_idx0,
            JS.NODE_IDX1: self.node_idx1,

            JS.HEIDX0: self.heidx0,
            JS.HEIDX1: self.heidx1,

            JS.BEAM_START: self.start,
            JS.BEAM_END: self.end,
            JS.DIRECTION: self.direction_vector,
            JS.FACE_NORMAL0: self._face_nv0,
            JS.FACE_NORMAL1: self._face_nv1,

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
            JS.BEAM_CART_POS: self._cart_position,
            JS.IS_IGNORED: self.is_ignored,

            JS.XBASE0: self.x_base0,
            JS.XBASE1: self.x_base1,
            JS.TRANSFORMATION_MATRIX: self.tm
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
    def create_from_dict(json_beam,  input_distance_units=units.Unit.millimeter ):
        b = Beam()

        b.beam_id = json_beam.get(JS.ID, -1)
        b.node_idx0 = json_beam.get(JS.NODE_IDX0, -1)
        b.node_idx1 = json_beam.get(JS.NODE_IDX1, -1)

        b.heidx0 = json_beam.get(JS.HEIDX0, -1)
        b.heidx1 = json_beam.get(JS.HEIDX1, -1)

        b._start = json_beam.get(JS.BEAM_START, [0, 0, 0])
        b._end = json_beam.get(JS.BEAM_END, [0, 0, 10])
        b.direction_vector = json_beam.get(JS.DIRECTION, [0, 0, 10])
        b._face_nv0 = json_beam.get(JS.FACE_NORMAL0, [0, 0, 10])
        b._face_nv1 = json_beam.get(JS.FACE_NORMAL1, [0, 0, 10])

        b._inner_d = json_beam.get(JS.INNER_DIAMETER, 8)
        b._outer_d = json_beam.get(JS.OUTSIDE_DIAMETER, 10)

        b.face_angle = json_beam.get(JS.FACE_ANGLE, 0)
        b.fidx0 = json_beam.get(JS.FIDX0, -1)
        b.fidx1 = json_beam.get(JS.FIDX1, -1)

        b.fiisqn0 = json_beam.get(JS.FIISQN0, -1)
        b.fiisqn1 = json_beam.get(JS.FIISQN1, -1)

        b.fiidx0 = json_beam.get(JS.FIIDX0, -1)
        b.fiidx1 = json_beam.get(JS.FIIDX1, -1)

        b.fii_len0 = json_beam.get(JS.FIILEN0, -1)
        b.fii_len1 = json_beam.get(JS.FIILEN1, -1)

        b.x_base0 = json_beam.get(JS.XBASE0, [0, 0, 10])
        b.x_base1 = json_beam.get(JS.XBASE1, [0, 0, 10])
        b.tm = json_beam.get(JS.TRANSFORMATION_MATRIX, matrix.identity(4))

        b._cart_position = json_beam.get(JS.BEAM_CART_POS, '---')
        b.is_ignored = json_beam.get(JS.IS_IGNORED, 'False')

        return b

    @staticmethod
    def create_list_from_dict(dict_face_list):
        list_of_faces = list()
        for dh in dict_face_list:
            h = Beam.create_from_dict(dh)
            list_of_faces.append(h)
        return list_of_faces

