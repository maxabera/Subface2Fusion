__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from typing import List
from .part_finger import Finger
from . import pad
from . import finger_bridge
from .part_finger import Finger
from . import matrix

from .part import Part
from .part_node_marking import NodeMarking
from .units import Unit
from . import units


class Node(Part):

    NODE_IDX = 'node_idx'
    VALENCY = 'valency'
    REAL_VALENCY = 'real_valency'
    IS_MELTED = 'is_melted'
    FINGERS = 'fingers'
    PADS = 'pads'
    FINGER_BRIDGES = 'finger_bridges'
    NODE_MARKINGS = 'node_markings'

    def __init__(self):
        super().__init__()
        self.node_id = -1
        self.valency = 1  # number of faces
        self.real_valency = 1 # number of non coplanar faces
        self.is_melted = False
        self.list_of_pads = list()
        self.list_of_fingers = list()
        self.list_of_fibridges = list()
        self.list_of_node_markings = list()

    def name(self, prefix=""):
        return "{}node_{:03d}".format(prefix, self.node_id)

    def part_num(self):
        return "NODE{:03d}".format(self.node_id)

    def list_to_int(self, list_of_numbers):
        list_of_int = list()
        for item in list_of_numbers:
            list_of_int.append(int(item))
        return list_of_int

    @staticmethod
    def create_list_from_dict(dict_object_list):
        list_of_objects = list()
        for dh in dict_object_list:
            h = Node.create_from_dict(dh)
            list_of_objects.append(h)
        return list_of_objects

    def add_node_marking(self, node_marking):
        self.list_of_node_markings.append(node_marking)

    def to_dict(self):

        node_json = {
            Node.NODE_IDX: int(self.node_id),
            Node.VALENCY: int(self.valency),
            Node.REAL_VALENCY: int(self.real_valency),
            Node.IS_MELTED: self.is_melted,
            Node.FINGERS: Finger.create_list_dict(self.list_of_fingers),
            Node.PADS: pad.Pad.create_list_dict(self.list_of_pads),
            Node.FINGER_BRIDGES: finger_bridge.FingerBridge.create_list_dict(self.list_of_fibridges),
            Node.NODE_MARKINGS: NodeMarking.create_list_dict(self.list_of_node_markings)
        }
        return node_json

    @staticmethod
    def create_from_dict(json_obj, distance_units=Unit.millimeter):

        new_object = Node()
        new_object.node_id = json_obj.get(Node.NODE_IDX, new_object.node_id)
        new_object.valency = json_obj.get(Node.VALENCY, new_object.valency)
        new_object.real_valency = json_obj.get(Node.REAL_VALENCY, new_object.real_valency)
        new_object.list_of_fingers = Finger.create_list_from_dict(json_obj[Node.FINGERS])
        new_object.list_of_pads = pad.Pad.create_list_from_dict(json_obj[Node.PADS])
        new_object.list_of_fibridges = finger_bridge.FingerBridge.create_list_from_dict(json_obj[Node.FINGER_BRIDGES])
        new_object.list_of_node_markings = NodeMarking.create_list_dict(json_obj[Node.NODE_MARKINGS])

        return new_object



