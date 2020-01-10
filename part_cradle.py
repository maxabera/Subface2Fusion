__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from .part import Part
from . import json_strings as JS
from . import units
from typing import List


class Cradle(Part):

    CRADLE_BALL_D = 'cradle_ball_d'
    CRADLE_POLY_D = 'cradle_poly_d'
    CRADLE_NOTCH_A = 'cradle_notch_a'

    def __init__(self):
        super().__init__()

        # defaults in mm

        self._ball_d = 20  # diameter of the basic ball
        self._poly_d = 16  # diameter of symetric polygon circumscribed
        self._notch_a = 1  # side of the notch, to identify upper side of the text

    @property
    def ball_d(self):
        return self.distance(self._ball_d)

    @property
    def poly_d(self):
        return self.distance(self._poly_d)

    @property
    def notch_a(self):
        return self.distance(self._notch_a)

    def to_dict(self):

        dict_object = {
            Cradle.CRADLE_BALL_D: self.ball_d,
            Cradle.CRADLE_POLY_D: self.poly_d,
            Cradle.CRADLE_NOTCH_A: self.notch_a,
        }
        return dict_object

    @staticmethod
    def create_list_dict(list_of_objects: List['Cradle']):
        dict_list_objects = list()
        for h in list_of_objects:
            dict_object = h.to_dict()
            dict_list_objects.append(dict_object)
        return dict_list_objects

    @staticmethod
    def create_from_dict(json_obj, input_distance_units=units.Unit.millimeter):

        new_object = Cradle()
        new_object.input_distance_units = input_distance_units
        new_object._ball_d = json_obj.get(json_obj[Cradle.CRADLE_BALL_D], new_object._ball_d)
        new_object._poly_d = json_obj.get(json_obj[Cradle.CRADLE_POLY_D], new_object._poly_d)
        new_object._notch_a = json_obj.get(json_obj[Cradle.CRADLE_NOTCH_A], new_object._notch_a)

        return new_object

    @staticmethod
    def create_list_from_dict(dict_object_list):
        list_of_objects = list()
        for dh in dict_object_list:
            h = Cradle.create_from_dict(dh)
            list_of_objects.append(h)
        return list_of_objects



class CradleWedge(Part):

    CRADLE_WEDGE_DEPTH = 'cradle_wedge_depth'
    CRADLE_WEDGE_A = 'cradle_wedge_a'

    def __init__(self):
        super().__init__()

        # defaults in mm
        self._size_a = 8  # basic size
        self._depth = 2  # depth of the number shield

    @property
    def size_a(self):
        return self.distance(self._size_a)

    @property
    def depth(self):
        return self.distance(self._depth)

    def to_dict(self):

        dict_object = {
            CradleWedge.CRADLE_WEDGE_DEPTH: self.depth,
            CradleWedge.CRADLE_WEDGE_A: self.size_a
        }
        return dict_object

    @staticmethod
    def create_list_dict(list_of_objects: List['CradleWedge']):
        dict_list_objects = list()
        for h in list_of_objects:
            dict_object = h.to_dict()
            dict_list_objects.append(dict_object)
        return dict_list_objects

    @staticmethod
    def create_from_dict(json_obj, distance_units=units.Unit.millimeter):

        new_object = CradleWedge()
        new_object.input_distance_units = distance_units
        new_object._size_a = json_obj.get(CradleWedge.CRADLE_WEDGE_A, new_object._size_a)
        new_object._depth = json_obj.get(CradleWedge.CRADLE_WEDGE_DEPTH, new_object._depth)

        return new_object

    @staticmethod
    def create_list_from_dict(dict_object_list):
        list_of_objects = list()
        for dh in dict_object_list:
            h = Cradle.create_from_dict(dh)
            list_of_objects.append(h)
        return list_of_objects