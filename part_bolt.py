__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from .part import Part
from . import units
from .units import Unit
from . import matrix

from enum import Enum
from typing import List


class BoltType(Enum):

    #  BOLT TYPE
    FACE_EDGE = 'face_edge'
    FACE_NODE = 'face_node'
    BEAM_FINGER = 'beam_finger'

    @staticmethod
    def from_string(value):
        return BoltType[value]


class Bolt(Part):

    # indices
    NODE_IDX = 'node_id'
    FIDX = 'fidx'
    COPL_FIDX = 'coplanar_fidx'
    BOLT_IN_FACE_IDX = 'bolt_in_face_idx'
    BOLT_IN_NODE_IDX = 'bolt_in_node_idx'
    BOLT_IN_COPLANAR_FACE_IDX = 'bolt_in_coplanar_face_idx'
    INC_HEIDX = 'inc_heidx'  # index of incoming halfedge
    OUT_HEIDX = 'out_heidx'  # index of outgoing halfedge
    BOLT_ID = 'bolt_id'

    FACE_POSITION = 'face_position'
    METRIC_DIA = 'metric_diameter'
    METRIC_LENGTH = 'metric_length'
    DIRECTION = 'direction'
    X_BASE = 'x_base'
    BOLT_DIN = 'bolt_din'
    TRUNK_DIAMETR = 'trunk_diameter'
    TAIL_DIAMETER = 'tail_diameter'
    TRANSFORMATION_MATRIX = 'transformation_matrix'

    THICKNESS_WALL = 'thickness_wall'
    THICKNESS_PAD = 'thickness_wall'
    THICKNESS_NUT = 'thickness_nut'

    TYPE = 'type'
    DISTANCE_TO_NEXT = 'bolt_distance_to_next'  # distance to following bolt within same face

    INC_DELTA = 'inc_delta'
    OUT_DELTA = 'out_delta'

    IS_ACTIVE = 'is_active'
    IS_INSIDE = 'is_inside'

    def __init__(self):
        super().__init__()

        # indices 9
        self.node_id = -1
        self.fidx = -1
        self.copl_fidx = -1
        self.sqn_face = -1
        self.sqn_node = -1
        self.sqn_coplanar_face = -1
        self.sqn_bolts = -1
        self.inc_heidx = -1
        self.out_heidx = -1

        # type 1
        self.bolt_type = BoltType.FACE_NODE

        # position and direction 7
        self._face_pos = [0, 0, 0]   # position on the inner side of the face
        self._direction = [0, 0, 1]  # vector of the main axis (usualy face normal)
        self._x_base = [1, 0, 0]     # usually paralel with middle between edges
        self._tm = matrix.identity(4)
        self._dist_to_next = -1 # distance to next bolt within a face
        self._inc_delta = 0
        self._out_delta = 0

        # metrics 3
        self._metric_diameter = 3
        self._metric_length = 20
        self.din_id = 'DIN987'

        # length 3
        self._th_wall = 4   # thickness of the wall
        self._th_pad = 5    # thickness of the mounting pad
        self._th_nut = 2    # thickness of the nut 0 if not used

        # hole dimensions 2
        self._trunk_diameter = 3.25  # diameter of the hole on the face
        self._tail_diameter = 2.75   # diameter of the hole on the mounting pad (connector)

        # FLAGS 2
        self.is_inside = True
        self.is_active = True



    @property
    def position_at_face(self):
        return self.point_3d(self._face_pos)

    @property
    def direction(self):
        return self.vector(self._direction)

    @property
    def x_base(self):
        return self.vector(self._x_base)

    @property
    def metric_diameter(self):
        return self.distance(self._metric_diameter)

    @property
    def metric_length(self):
        return self.distance(self._metric_length)

    @property
    def trunk_diameter(self):
        return self.distance(self._trunk_diameter)

    @property
    def tail_diameter(self):
        return self.distance(self._tail_diameter)

    @property
    def inc_delta(self):
        return self.distance(self._inc_delta)

    @property
    def out_delta(self):
        return self.distance(self._out_delta)

    @property
    def th_nut(self):
        return self.distance(self._th_nut)

    @property
    def th_pad(self):
        return self.distance(self._th_pad)

    @property
    def th_wall(self):
        return self.distance(self._th_wall)

    @property
    def t_matrix(self):
        return self.matrix(self._tm)

    @property
    def min_length(self):
        return self.th_wall + self.th_pad + self.th_nut

    def set_trunk_diameter(self, diameter, input_unit=Unit.millimeter):
        self._trunk_diameter = self.set_distance(diameter, input_unit)

    def set_tail_diameter(self, diameter, input_unit=Unit.millimeter):
        self._tail_diameter = self.set_distance(diameter, input_unit)

    def set_metric_diameter(self, diameter, input_unit=Unit.millimeter):
        self._metric_diameter = self.set_distance(diameter, input_unit)

    def set_metric_length(self, diameter, input_unit=Unit.millimeter):
        self._metric_length = self.set_distance(diameter, input_unit)

    def set_position_at_face(self, position3d, input_unit=Unit.millimeter):
        self._face_pos = self.set_point3d(position3d, input_unit)

    def set_direction(self, direction3d, input_unit=Unit.millimeter):
        self._direction = self.set_vector(direction3d, input_unit)

    def set_xbase(self, direction3d, input_unit=Unit.millimeter):
        self._x_base = self.set_vector(direction3d, input_unit)

    def set_dist_to_next(self, dist, input_unit=Unit.millimeter):
        self._dist_to_next = self.set_distance(dist, input_unit)

    def set_inc_delta(self, dist, input_unit=Unit.millimeter):
        self._inc_delta = self.set_distance(dist, input_unit)

    def set_out_delta(self, dist, input_unit=Unit.millimeter):
        self._out_delta = self.set_distance(dist, input_unit)

    def set_t_matrix(self, tm, input_unit=Unit.millimeter):
        self._tm = self.set_matrix(tm, input_unit)

    def set_th_wall(self, thickness, input_unit=Unit.millimeter):
        self._th_wall = self.set_distance(thickness, input_unit)

    def set_th_nut(self, thickness, input_unit=Unit.millimeter):
        self._th_nut = self.set_distance(thickness, input_unit)

    def set_th_pad(self, thickness, input_unit=Unit.millimeter):
        self._th_pad = self.set_distance(thickness, input_unit)

    def to_dict(self):

        finger_json = {

            # indices 9
            Bolt.NODE_IDX: int(self.node_id),
            Bolt.FIDX: self.fidx,
            Bolt.COPL_FIDX: self.copl_fidx,
            Bolt.BOLT_IN_NODE_IDX: self.sqn_node,
            Bolt.BOLT_IN_FACE_IDX: self.sqn_face,
            Bolt.BOLT_IN_COPLANAR_FACE_IDX: self.sqn_coplanar_face,
            Bolt.BOLT_ID: self.sqn_bolts,
            Bolt.INC_HEIDX: self.inc_heidx,
            Bolt.OUT_HEIDX: self.out_heidx,

            Bolt.TYPE: str(self.bolt_type.name),

            # position and direction 7
            Bolt.FACE_POSITION: self.position_at_face,
            Bolt.DIRECTION: self.direction,
            Bolt.X_BASE: self.x_base,
            Bolt.TRANSFORMATION_MATRIX: self.t_matrix,
            Bolt.DISTANCE_TO_NEXT: self._dist_to_next,
            Bolt.INC_DELTA: self.inc_delta,
            Bolt.OUT_DELTA: self.out_delta,

            # metrics 3
            Bolt.METRIC_DIA: self.metric_diameter,
            Bolt.METRIC_LENGTH: self.metric_length,
            Bolt.BOLT_DIN: self.din_id,

            # length
            Bolt.THICKNESS_NUT: self.th_nut,
            Bolt.THICKNESS_PAD: self.th_pad,
            Bolt.THICKNESS_WALL: self.th_wall,

            # hole dimensions 2
            Bolt.TRUNK_DIAMETR: self.trunk_diameter,
            Bolt.TAIL_DIAMETER: self.tail_diameter,

            # flags 2
            Bolt.IS_ACTIVE: self.is_active,
            Bolt.IS_INSIDE: self.is_inside
        }

        return finger_json

    @staticmethod
    def create_list_from_dict(dict_object_list):
        list_of_objects = list()
        for dh in dict_object_list:
            h = Bolt.create_from_dict(dh)
            list_of_objects.append(h)
        return list_of_objects

    @staticmethod
    def create_from_dict(json_obj, distance_units=Unit.millimeter):

        new_object = Bolt()

        # indices 9
        new_object.node_id = json_obj.get(Bolt.NODE_IDX, new_object.node_id)
        new_object.fidx = json_obj.get(Bolt.FIDX, new_object.fidx)
        new_object.copl_fidx = json_obj.get(Bolt.COPL_FIDX, new_object.copl_fidx)
        new_object.sqn_node = json_obj.get(Bolt.BOLT_IN_NODE_IDX, new_object.sqn_node)
        new_object.sqn_face = json_obj.get(Bolt.BOLT_IN_FACE_IDX, new_object.sqn_face)
        new_object.sqn_coplanar_face = json_obj.get(Bolt.BOLT_IN_COPLANAR_FACE_IDX, new_object.sqn_coplanar_face)
        new_object.sqn_bolts = json_obj.get(Bolt.BOLT_ID, new_object.sqn_bolts)
        new_object.inc_heidx = json_obj.get(Bolt.INC_DELTA, new_object.inc_heidx)
        new_object.out_heidx = json_obj.get(Bolt.OUT_DELTA, new_object.out_heidx)

        tmp = BoltType[json_obj.get(Bolt.TYPE, new_object.bolt_type.name)]
        if tmp is not None:
            new_object.bolt_type = tmp
        # else default from __init__

        # position and direction 7
        new_object.set_position_at_face(json_obj.get(Bolt.FACE_POSITION, new_object._face_pos), distance_units)
        new_object.set_direction(json_obj.get(Bolt.DIRECTION, new_object._direction), distance_units)
        new_object.set_xbase(json_obj.get(Bolt.X_BASE, new_object._x_base), distance_units)
        new_object.set_dist_to_next(json_obj.get(Bolt.DISTANCE_TO_NEXT, new_object._dist_to_next), distance_units)
        new_object.set_t_matrix(json_obj.get(Bolt.TRANSFORMATION_MATRIX, new_object._tm), distance_units)
        new_object.set_inc_delta(json_obj.get(Bolt.INC_DELTA, new_object._out_delta), distance_units)
        new_object.set_out_delta(json_obj.get(Bolt.OUT_DELTA, new_object._inc_delta), distance_units)

        # metrics 3
        new_object.set_metric_diameter(json_obj.get(Bolt.METRIC_DIA, new_object._metric_diameter), distance_units)
        new_object.set_metric_length(json_obj.get(Bolt.METRIC_LENGTH, new_object._metric_length), distance_units)
        new_object.din_id = json_obj.get(Bolt.BOLT_DIN, new_object.din_id)

        # length 3
        new_object.set_th_nut(json_obj.get(Bolt.THICKNESS_NUT, new_object._th_nut), distance_units)
        new_object.set_th_wall(json_obj.get(Bolt.THICKNESS_WALL, new_object.th_wall), distance_units)
        new_object.set_th_pad(json_obj.get(Bolt.THICKNESS_PAD, new_object._th_pad), distance_units)

        # hole 2
        new_object._tail_diameter = json_obj.get(Bolt.TAIL_DIAMETER, new_object._tail_diameter)
        new_object._trunk_diameter = json_obj.get(Bolt.TRUNK_DIAMETR, new_object._trunk_diameter)
        new_object._metric_diameter = json_obj.get(Bolt.METRIC_DIA, new_object._metric_diameter)

        # flags 2
        new_object.is_inside = json_obj.get(Bolt.IS_INSIDE, new_object.is_inside)
        new_object.is_active = json_obj.get(Bolt.IS_ACTIVE, new_object.is_active)

        return new_object
