__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from .part import Part
from . import matrix
from . import units

from enum import Enum


class NodeMarkType(Enum):

    UNKNOWN = 0
    MIDDLE = 1
    PAD_EDGE = 2
    PEAK = 3

    # to string
    # NodeMarkType.UNKNOWN.name

    # from string
    # NodeMarkType('UNKNOWN')

    @staticmethod
    def from_string(value):
        return NodeMarkType[value]


class NodeMarking(Part):

    # Node Marking Type

    MIDDLE_VECTOR = 'middle_vector'
    POSITION = 'position'
    TRANSFORMATION_MATRIX = 'transformation_matrix'
    TYPE = 'type'

    def __init__(self):
        super().__init__()

        self._middle_vector = [0, 0, 1]
        self._position = [0, 0, 0]
        self._x_base = [1, 0, 0]
        self.type = NodeMarkType.UNKNOWN
        self._tm = matrix.identity(4) # transformation matrix

    @property
    def middle_vector(self):
        v = self.vector(self._middle_vector)
        return v

    @property
    def position(self):
        v = self.point_3d(self._position)
        return v

    @property
    def x_base(self):
        v = self.vector(self._x_base)
        return v

    @property
    def t_matrix(self):
        v = self.matrix(self._tm)
        return v

    @middle_vector.setter
    def middle_vector(self, value, dist_units=None):
        if dist_units is None:
            dist_units = self.input_distance_units
        self._middle_vector = self.set_vector(value, dist_units)

    @position.setter
    def position(self, value, dist_units=None):
        if dist_units is None:
            dist_units = self.input_distance_units
        self._position = self.set_point3d(value, dist_units)

    @x_base.setter
    def x_base(self, value, dist_units=None):
        if dist_units is None:
            dist_units = self.input_distance_units
        self._x_base = self.set_point3d(value, dist_units)

    @t_matrix.setter
    def t_matrix(self, value, dist_units=None):
        if dist_units is None:
            dist_units = self.input_distance_units
        self._tm = self.set_matrix(value, dist_units)

    def to_dict(self):
        node_json = {
            NodeMarking.MIDDLE_VECTOR: self.middle_vector,
            NodeMarking.POSITION: self.position,
            NodeMarking.TYPE: self.type.name,
            NodeMarking.TRANSFORMATION_MATRIX: self.t_matrix
        }
        return node_json

    @staticmethod
    def create_from_dict(json_obj, input_distance_units=units.Unit.millimeter):

        new_object = NodeMarking()
        new_object.input_distance_units = input_distance_units

        new_object._middle_vector = json_obj.get(NodeMarking.MIDDLE_VECTOR, new_object._middle_vector)
        new_object._position = json_obj.get(NodeMarking.POSITION, new_object._position)
        new_object._tm = json_obj.get(NodeMarking.TRANSFORMATION_MATRIX, new_object._tm)
        new_object.type = NodeMarkType.from_string(json_obj.get(NodeMarking.TYPE, new_object.type))

        return new_object

    @staticmethod
    def create_list_from_dict(dict_obj_list):
        list_of_parts = list()
        for dh in dict_obj_list:
            h = NodeMarking.create_from_dict(dh)
            list_of_parts.append(h)
        return list_of_parts