__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from .part import Part
from . import json_strings as JS
from . import units
from typing import List





class Bump(Part):

    # bump type
    # bump simple
    # bump bolt_DIN912
    # bump bolt_DIN965

    def __init__(self):
        super().__init__()

        # defaults in mm

        self.type = JS.BUMP_SIMPLE
        self._height = 10
        self._width = 10
        self._delta = 3

        self.input_distance_units = units.Unit.millimeter
        self.output_distance_units = units.Unit.centimeter

    @property
    def height(self):
        return self.distance(self._height)

    @property
    def width(self):
        return self.distance(self._width)

    @property
    def delta(self):
        return self.distance(self._delta)

    def to_dict(self):

        dict_object = {
            JS.BUMP_TYPE: self.type,
            JS.BUMP_HEIGHT: self.height,
            JS.BUMP_WIDTH: self.width,
            JS.BUMP_DELTA: self.delta,
        }
        return dict_object

    @staticmethod
    def create_list_dict(list_of_objects: List['Bump']):
        dict_list_objects = list()
        for h in list_of_objects:
            dict_object = h.to_dict()
            dict_list_objects.append(dict_object)
        return dict_list_objects

    @staticmethod
    def create_from_dict(json_obj, input_distance_units=units.Unit.millimeter):

        new_object = Bump()
        new_object.input_distance_units = input_distance_units
        new_object.type = json_obj.get(json_obj[JS.BUMP_TYPE], new_object.type)
        new_object._height = json_obj.get(json_obj[JS.BUMP_HEIGHT], new_object._height)
        new_object._width = json_obj.get(json_obj[JS.BUMP_WIDTH], new_object._width)
        new_object._delta = json_obj.get(json_obj[JS.BUMP_DELTA], new_object._delta)

        return new_object

    @staticmethod
    def create_list_from_dict(dict_object_list):
        list_of_objects = list()
        for dh in dict_object_list:
            h = Bump.create_from_dict(dh)
            list_of_objects.append(h)
        return list_of_objects


class BumpBolt912(Bump):

    def __init__(self):
        super().__init__()

        self._bolt_z = 5  # hole position from end
        self._hole_d = 3.25 # hole diameter

    @property
    def bolt_z(self):
        return self.distance(self._bolt_z)

    @property
    def hole_d(self):
        return self.distance(self._hole_d)


    def to_dict(self):
        dict_object = super().to_dict()

        dict_object[JS.BUMP_TYPE] = JS.BUMP_BOLT_DIN912
        dict_object[JS.DIAMETER] = self._hole_d
        dict_object[JS.BOLT_Z] = self._bolt_z

        return dict_object

    @staticmethod
    def create_list_dict(list_of_objects: List['BumpBolt912']):
        dict_list_objects = list()
        for h in list_of_objects:
            dict_object = h.to_dict()
            dict_list_objects.append(dict_object)
        return dict_list_objects

    @staticmethod
    def create_from_dict(json_obj, input_distance_units=units.Unit.millimeter):


        new_object = BumpBolt912()
        new_object.input_distance_units = input_distance_units
        new_object.type= json_obj.get(json_obj[JS.BUMP_TYPE], new_object.type)
        new_object._height = json_obj.get(json_obj[JS.BUMP_HEIGHT], new_object._height)
        new_object._width = json_obj.get(json_obj[JS.BUMP_WIDTH], new_object._width)
        new_object._delta = json_obj.get(json_obj[JS.BUMP_DELTA], new_object._delta)
        new_object._bolt_z = json_obj.get(json_obj[JS.BUMP_DELTA], new_object._bolt_z)
        new_object._hole_d = json_obj.get(json_obj[JS.DIAMETER], new_object._hole_d)


        return new_object

    @staticmethod
    def create_list_from_dict(dict_object_list):
        list_of_objects = list()
        for dh in dict_object_list:
            h = BumpBolt912.create_from_dict(dh)
            list_of_objects.append(h)
        return list_of_objects