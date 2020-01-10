__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from . import json_strings as JS
from typing import List
from . import part_hole
from .part import Part
from .units import Unit
from . import matrix

class Pad(Part):

    def __init__(self):
        super().__init__()

        # core data
        self.node_id = -1
        self.inc_finger = -1
        self.out_finger = -1
        self.seq_num = -1

        self.grounded_polypoints = None   # polygon transformed to XY plane
        self.transformation_matrix = None  # transformation matrix
        self.original_polypoints = None   # polygon in original position in 3d space
        self.orig_nv = None   # normal vector of original polygon
        self.thickness = 1
        self.hole_position = None

    @property
    def component_name(self):
        s = "P{:03d}_{:02d}".format(self.node_id, self.seq_num)
        return s

    def list_to_int(self, list_of_numbers):
        list_of_int = list()
        for item in list_of_numbers:
            list_of_int.append(int(item))
        return list_of_int

    def to_dict(self):
        pad_json = {
            JS.NODE_IDX: int(self.node_id),
            JS.SEQUENCE_NUMBER: int(self.seq_num),
            JS.INC_FIIDX: int(self.inc_finger),
            JS.OUT_FIIDX: int(self.out_finger),
            JS.THICKNESS: self.thickness,
            JS.NUMBER_OF_POINTS: len(self.grounded_polypoints),
            JS.POLYPOINTS_GROUNDED: self.grounded_polypoints,
            JS.HOLE_POSITION: self.hole_position,
            JS.TRANSFORMATION_MATRIX: self.transformation_matrix
        }
        return pad_json

    @staticmethod
    def create_list_dict(list_of_pads: List['Pad']):
        dict_list_pads = list()
        for h in list_of_pads:
            dict_hole = h.to_dict()
            dict_list_pads.append(dict_hole)
        return dict_list_pads

    @staticmethod
    def create_from_dict(json_pad,  input_distance_units=Unit.millimeter):
        f = Pad()


        f.node_id = json_pad.get(JS.NODE_IDX, -1)
        f.seq_num = json_pad.get(JS.SEQUENCE_NUMBER, -1)
        f.inc_finger = json_pad.get(JS.INC_FIIDX, -1)
        f.out_finger = json_pad.get(JS.OUT_FIIDX, -1)
        f.thickness = json_pad.get(JS.THICKNESS, 1)
        f.grounded_polypoints = json_pad.get(JS.POLYPOINTS_GROUNDED, list())
        f.transformation_matrix = json_pad.get(JS.TRANSFORMATION_MATRIX, matrix.identity(4))
        f.hole_position = json_pad.get(JS.HOLE_POSITION, None)
        return f


    @staticmethod
    def create_list_from_dict(dict_pad_list):
        list_of_pads = list()
        for dh in dict_pad_list:
            h = Pad.create_from_dict(dh)
            list_of_pads.append(h)
        return list_of_pads
