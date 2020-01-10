from . import json_strings as JS
from typing import List

class FingerBridge:

    def __init__(self):

        # core data
        self.node_id = -1  # node id
        self.seq_num = -1   # finger_bridge sequence number within node
        self.fiidx = -1    # outgoing finger id
        self.start = [0, 0, 0]  # start postion of the finger
        self.end = [0, 0, 20]   # end of the finger
        self.diameter = 10  # inner diameter

    def name(self):
        return "fib_{:03d}_{:02d}".format(self.node_id, self.seq_num)

    def part_num(self):
        return "FB{:04d}_{:03d}_{:02d}".format(self.fiidx, self.node_id, self.seq_num)

    def to_dict(self):

        finger_json = {
            JS.NODE_IDX: int(self.node_id),
            JS.SEQUENCE_NUMBER: int(self.seq_num),
            JS.FIIDX: int(self.fiidx),
            JS.START_POINT: self.start,
            JS.END_POINT: self.end,
            JS.DIAMETER: self.diameter
        }

        return finger_json

    @staticmethod
    def create_list_dict(list_of_fingers: List['FingerBridge']):
        dict_list_fingers = list()
        for h in list_of_fingers:
            dict_hole = h.to_dict()
            dict_list_fingers.append(dict_hole)
        return dict_list_fingers

    @staticmethod
    def create_from_dict(json_finger):
        f = FingerBridge()
        tm_zero = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]

        f.node_id = json_finger.get(JS.NODE_IDX, -1)
        f.sq_num = json_finger.get(JS.SEQUENCE_NUMBER, -1)
        f.fiidx = json_finger.get(JS.FIIDX, -1)
        f.start = json_finger.get(JS.START_POINT, [0, 0, 0])
        f.end = json_finger.get(JS.END_POINT, [0, 0, 10])
        f.diameter = json_finger.get(JS.DIAMETER, -1)

        return f


    @staticmethod
    def create_list_from_dict(dict_fibridge_list):
        list_of_fibridges = list()
        for dh in dict_fibridge_list:
            h = FingerBridge.create_from_dict(dh)
            list_of_fibridges.append(h)
        return list_of_fibridges