__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from .units import Unit
from typing import List

class Part:

    def __init__(self):
        self.input_distance_units = Unit.millimeter
        self.output_distance_units = Unit.centimeter
        self.input_angle_units = Unit.radian
        self.output_angle_units = Unit.degree

    def set_output_units(self, distance=None, angle=None):
        if distance is not None:
            self.output_distance_units = distance
        if angle is not None:
            self.output_angle_units = angle

    def set_input_units(self, distance=None, angle=None):
        if distance is not None:
            self.input_distance_units = distance
        if angle is not None:
            self.input_angle_units = angle

    def distance(self, value):
        d = Unit.distance(value, self.input_distance_units, self.output_distance_units)
        return d

    def vector(self, vec):
        v = Unit.distance_array(vec, self.input_distance_units, self.output_distance_units)
        return v

    def point_3d(self, point):
        v = Unit.distance_array(point, self.input_distance_units, self.output_distance_units)
        return v

    def angle(self, alpha):
        a = Unit.angle(alpha, self.input_angle_units, self.output_angle_units)
        return a

    def matrix(self, mat):
        a = Unit.matrix(mat, self.input_distance_units, self.output_distance_units)
        return a

    def matrix_serialize(self, m):
        a = Unit.matrix_serialize(m, self.input_distance_units, self.output_distance_units)
        return a

    def to_dict(self):
        return {}

    def create_from_dict(self, json_obj):
        return list()

    def set_point3d(self, value, distance_unit):
        v = Unit.distance_array(value, distance_unit, self.input_distance_units)
        return v

    def set_vector(self, value, distance_unit):
        v = Unit.distance_array(value, distance_unit, self.input_distance_units)
        return v

    def set_matrix(self, value, distance_unit):
        v = Unit.matrix(value, distance_unit, self.input_distance_units)
        return v

    def set_distance(self, value, distance_unit):
        v = Unit.distance(value, distance_unit, self.input_distance_units)
        return v

    def set_angle(self, value, angle_unit):
        v = Unit.angle(value, angle_unit, self.input_angle_units)
        return v

    @staticmethod
    def create_list_dict(list_of_nodes: List['Part']):
        """
        creates json-dictionary from list of Parts
        :param list_of_nodes:
        :return:
        """
        list_of_part_dict = list()

        return list_of_part_dict

