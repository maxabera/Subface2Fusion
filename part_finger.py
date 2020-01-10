__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from . import json_strings as JS
from .part import Part
from . import units
from typing import List
from . import matrix


class Finger(Part):

    def __init__(self):
        super().__init__()
        # core data

        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter

        self.node_id = -1  # node id
        self.sq_num = -1  # finger sequence number within node
        self.fiidx = -1  # overal finger id

        self._start = [0, 0, 0]  # start postion of the finger
        self._end = [0, 0, 20]  # end of the finger
        self._length = 1
        self._effective_length = 1

        self.direction = [0, 0, 1]  # direction of the finger - start/end vector
        self.x_base = [1, 0, 0]  # perpendicular to main axis - direction of the finger

        self.is_ignored = False  # True if rendering of the finger will be ommited
        self.is_melted = False  # True if overlaps with opposite finger
        self._inner_d = 10  # inner diameter
        self._outer_d = 20  # outer diameter
        self._rod_encore = 20
        self._tm = matrix.identity(4)  # transformation matrix

    def name(self):
        return "fii_{:03d}_{:02d}".format(self.node_id, self.sq_num)

    def phalanx_name(self):
        return "px_{:03d}_{:02d}".format(self.node_id, self.sq_num)

    def part_num(self):
        return "FII{:04d}_{:03d}_{:02d}".format(self.fiidx, self.node_id, self.sq_num)

    @property
    def inner_d(self):
        return self.distance(self._inner_d)

    @inner_d.setter
    def inner_d(self, value):
        self._inner_d = self.set_distance(value, self.input_distance_units)

    @property
    def outer_d(self):
        return self.distance(self._outer_d)

    @outer_d.setter
    def outer_d(self, value):
        self._outer_d = self.set_distance(value, self.input_distance_units)

    @property
    def length(self):
        return self.distance(self._length)

    @length.setter
    def length(self, value):
        self._length = self.set_distance(value, self.input_distance_units)

    @property
    def effective_length(self):
        return self.distance(self._effective_length)

    @effective_length.setter
    def effective_length(self, value):
        self._effective_length = self.set_distance(value, self.input_distance_units)

    @property
    def rod_encore(self):
        return self.distance(self._rod_encore)

    @rod_encore.setter
    def rod_encore(self, value):
        self._rod_encore = self.set_distance(value, self.input_distance_units)

    @property
    def start(self):
        return self.point_3d(self._start)

    @start.setter
    def start(self, value):
        self._start = self.set_distance(value, self.input_distance_units)

    @property
    def end(self):
        return self.point_3d(self._end)

    @end.setter
    def end(self, value):
        self._end = self.set_distance(value, self.input_distance_units)

    @property
    def tm(self):
        v = self.matrix(self._tm)
        return v

    @tm.setter
    def tm(self, value):
        self._tm = self.set_matrix(value, self.input_distance_units)

    def tm_serialized(self):
        v = self.matrix_serialize(self._tm)
        return v

    def to_dict(self):

        finger_json = {
            JS.NODE_IDX: int(self.node_id),
            JS.SEQUENCE_NUMBER: int(self.sq_num),
            JS.FIIDX: int(self.fiidx),
            JS.START_POINT: self.start,
            JS.END_POINT: self.end,
            JS.LENGTH: self.length,
            JS.EFFECTIVE_LENGTH: self.effective_length,
            JS.DIRECTION: self.direction,
            JS.XBASE: self.x_base,
            JS.IS_IGNORED: self.is_ignored,
            JS.IS_MELTED: self.is_melted,
            JS.INNER_DIAMETER: self.inner_d,
            JS.OUTSIDE_DIAMETER: self.outer_d,
            JS.FINGER_ROD_ENCORE: self.rod_encore,
            JS.TRANSFORMATION_MATRIX: self.tm
        }

        return finger_json

    @staticmethod
    def create_list_dict(list_of_fingers: List['Finger']):
        dict_list_fingers = list()
        for h in list_of_fingers:
            dict_hole = h.to_dict()
            dict_list_fingers.append(dict_hole)
        return dict_list_fingers

    @staticmethod
    def create_from_dict(json_finger, input_distance_units=units.Unit.millimeter):
        new_object = Finger()
        new_object.input_distance_units = input_distance_units

        new_object.node_id = json_finger.get(JS.NODE_IDX, -1)
        new_object.sq_num = json_finger.get(JS.SEQUENCE_NUMBER, -1)
        new_object.fiidx = json_finger.get(JS.FIIDX, -1)
        new_object._start = json_finger.get(JS.START_POINT, [0, 0, 0])
        new_object._length = json_finger.get(JS.LENGTH, 1)
        new_object._effective_length = json_finger.get(JS.EFFECTIVE_LENGTH, 1)
        new_object._end = json_finger.get(JS.END_POINT, [0, 0, 10])
        new_object.direction = json_finger.get(JS.DIRECTION, [0, 0, 10])
        new_object.x_base = json_finger.get(JS.XBASE, [1, 0, 0])
        new_object.is_ignored = json_finger.get(JS.IS_IGNORED, False)
        new_object.is_melted = json_finger.get(JS.IS_MELTED, False)
        new_object._inner_d = json_finger.get(JS.INNER_DIAMETER, new_object._inner_d)
        new_object._outer_d = json_finger.get(JS.OUTSIDE_DIAMETER, new_object._outer_d)
        new_object._rod_encore = json_finger.get(JS.FINGER_ROD_ENCORE, new_object._rod_encore)
        new_object._tm = json_finger.get(JS.TRANSFORMATION_MATRIX, new_object._tm)

        return new_object

    @staticmethod
    def create_list_from_dict(dict_fingers_list):
        list_of_fingers = list()
        for dh in dict_fingers_list:
            h = Finger.create_from_dict(dh)
            list_of_fingers.append(h)
        return list_of_fingers
