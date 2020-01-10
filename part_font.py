__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from .part import Part
from . import json_strings as JS
from . import units
from typing import List


class Font(Part):

    def __init__(self):
        super().__init__()

        self.font_name = "OCR A Extended"
        self._size = 5
        self._positive_height = 1
        self._negative_depth = 2

        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter

    @property
    def size(self):
        return self.distance(self._size)

    @property
    def positive_height(self):
        return self.distance(self._positive_height)

    @property
    def negative_depth(self):
        return self.distance(self._negative_depth)

    def to_dict(self):

        dict_object = {
            JS.FONT_NAME: self.font_name,
            JS.FONT_SIZE: self.size,
            JS.POSITIVE_HEIGHT: self.positive_height,
            JS.NEGATIVE_DEPTH: self.negative_depth
        }
        return dict_object

    @staticmethod
    def create_list_dict(list_of_objects: List['Font']):
        dict_list_objects = list()
        for h in list_of_objects:
            dict_object = h.to_dict()
            dict_list_objects.append(dict_object)
        return dict_list_objects

    @staticmethod
    def create_from_dict(json_obj, input_distance_units=units.Unit.millimeter):

        new_object = Font()
        new_object.input_distance_units = input_distance_units
        new_object.font_name = json_obj.get(json_obj[JS.FONT_NAME], new_object.font_name)
        new_object._size = json_obj.get(json_obj[JS.FONT_SIZE], new_object.size)
        new_object._positive_height = json_obj.get(json_obj[JS.POSITIVE_HEIGHT], new_object.positive_height)
        new_object._negative_depth = json_obj.get(json_obj[JS.NEGATIVE_DEPTH], new_object.negative_depth)

        return new_object

    @staticmethod
    def create_list_from_dict(dict_object_list):

        list_of_objects = list()

        for dh in dict_object_list:
            h = Font.create_from_dict(dh)
            list_of_objects.append(h)

        return list_of_objects