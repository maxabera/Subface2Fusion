from typing import List
from . import part_finger
from . import pad
from . import finger_bridge
from . import matrix

from .part import Part
from .part_node_marking import NodeMarking
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

    def add_node_marking(self, node_marking):
        self.list_of_node_markings.append(node_marking)

    def to_dict(self):

        node_json = {
            Node.NODE_IDX: int(self.node_id),
            Node.VALENCY: int(self.valency),
            Node.REAL_VALENCY: int(self.real_valency),
            Node.IS_MELTED: self.is_melted,
            Node.FINGERS: Part.create_list_dict(self.list_of_fingers),
            Node.PADS: pad.Pad.create_list_dict(self.list_of_pads),
            Node.FINGER_BRIDGES: finger_bridge.FingerBridge.create_list_dict(self.list_of_fibridges),
            Node.NODE_MARKINGS: NodeMarking.create_list_dict(self.list_of_node_markings)
        }
        return node_json

    @staticmethod
    def create_list_dict(list_of_nodes: List['Node']):
        dict_list_nodes = list()
        for json_node in list_of_nodes:
            dict_node = json_node.to_dict()
            dict_list_nodes.append(dict_node)
        return dict_list_nodes

    @staticmethod
    def create_from_dict(json_obj, input_distance_units=units.Unit.millimeter):

        new_object = Node()
        new_object.input_distance_units = input_distance_units

        new_object.node_id = json_obj.get(Node.NODE_IDX, new_object.node_id)
        new_object.valency = json_obj.get(Node.VALENCY, new_object.valency)
        new_object.real_valency = json_obj.get(Node.REAL_VALENCY, new_object.real_valency)

        new_object.list_of_fingers = part_finger.Finger.create_list_from_dict(json_obj[Node.FINGERS])
        new_object.list_of_pads = pad.Pad.create_list_from_dict(json_obj[Node.PADS])
        new_object.list_of_fibridges = finger_bridge.FingerBridge.create_list_from_dict(json_obj[Node.FINGER_BRIDGES])
        new_object.list_of_node_markings = NodeMarking.create_list_from_dict(json_obj[Node.NODE_MARKINGS])

        return new_object

    @staticmethod
    def create_list_from_dict(dict_node_list):
        list_of_nodes = list()
        for dh in dict_node_list:
            h = Node.create_from_dict(dh)
            list_of_nodes.append(h)
        return list_of_nodes

