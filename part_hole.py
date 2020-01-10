from . import json_strings as JS
from typing import List
import math

class Hole:

    # holetype
    SIMPLE = 1
    COUNTER_BORE = 2
    COUNTER_SINK = 3
    COUNTER_HEX = 4

    def __init__(self):
        self.position = [0, 0, 0]
        self.diameter = 3
        self.length = 20
        self.vidx = 0
        self.sequence_number = 0
        self.fidx = -1

        self.counter_diameter = 6
        self.counter_angle = math.pi/2.0
        self.holetype = Hole.SIMPLE


    def to_dict(self):

        dict_hole = {
            JS.POSITION: self.position,
            JS.DIAMETER: self.diameter,
            JS.VERTEX_ID: self.vidx,
            JS.SEQUENCE_NUMBER: self.sequence_number,
            JS.FIDX: self.fidx
        }
        return dict_hole

    @staticmethod
    def create_list_dict(list_of_holes: List['Hole']):
        dict_list_holes = list()
        for h in list_of_holes:
            dict_hole = h.to_dict()
            dict_list_holes.append(dict_hole)
        return dict_list_holes


    @staticmethod
    def create_from_dict(dict_hole):

        new_hole = Hole()
        new_hole.position = dict_hole[JS.POSITION]
        new_hole.diameter = dict_hole[JS.DIAMETER]
        new_hole.vidx = dict_hole[JS.VERTEX_ID]
        new_hole.sequence_number = dict_hole[JS.SEQUENCE_NUMBER]
        new_hole.fidx = dict_hole[JS.FIDX]

        return new_hole

    @staticmethod
    def create_list_from_dict(dict_hole_list):

        list_of_holes = list()

        for dh in dict_hole_list:
            h = Hole.create_from_dict(dh)
            list_of_holes.append(h)

        return list_of_holes

