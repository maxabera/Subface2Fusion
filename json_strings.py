NODE_SOLUTIONS = "node_solutions"
VERSION = "version"
NODE_DATABASE = "node_db"
SOLUTION_ID = "solution_id"
USED_IN = "used_in"
PATTERN = "pattern"
VALENCY = "valency"
POINTS_INSIDE = "points_inside"
CHAIN = "chain"
MODEL_NAME = 'model_name'
MODEL_ID = 'model_id'
VERTEX_ID = 'vidx'
TIME_TO_SOLVE = 'time_to_solve'
SECONDS_TO_SOLVE = 'seconds_to_solve'
SHIFT = 'shift'
IS_REVERSED = 'is_reversed'
SOLVER = 'solver'
HEADER = 'header'
NODES = 'nodes'
INFLATE_TYPE = 'inflate_type'

# export mesh
# export inflate
# export offset

# import/export point_cloud
SUBFACE = 'subface'
ATTRIBUTES = 'attributes'
POINT_CLOUD = 'point_cloud'
NUMBER_OF_POINTS = 'number_of_points'
NUMBER = 'number'
POINT_LIST = 'point_list'
ID = 'id'
FACE_ID = 'face_id'
FACES = 'faces'
FACE = 'face'
COORDINATES = 'coordinates'
VERTICES = 'vertices'
VERTEX = 'vertex'
INDICES = 'indices'
MESH = 'mesh'
MESH_DATA = 'mesh_data'
POINTS = 'points'
POLYGONS = 'polygons'
POLYGON = 'polygon'
POLYPOINTS = 'polypoints'
POLYPOINTS_GROUNDED = 'polypoints_grounded'
POLYPOINTS_ORIGINAL = 'polypoints_original'
POLYGON_GROUNDED = 'polygon_grounded'
POLYGONS_ORIGINAL = 'polygons_original'
THICKNESS = 'thickness'
HOLE = 'hole'
HOLES = 'holes'
HOLE_POSITION = 'hole_position'
NUMBER_OF_HOLES = 'number_of_holes'
DIAMETER = 'diameter'
NUMBER_OF_FINGERS = 'number_of_fingers'
FINGERS = 'fingers'
FINGER = 'finger'
FINGER_BRIDGE = 'finger_bridge'
FINGER_BRIDGES = 'finger_bridges'
FINGER_BACK_YARD = 'finger_back_yard'
FINGER_ROD_ENCORE = 'finger_rod_encore'
PAD = 'pad'
PADS = 'pads'
NUMBER_OF_PADS = 'number_od_pads'
INNER_DIAMETER = 'inner_diameter'
OUTSIDE_DIAMETER = 'outside_diameter'

BOLTS = 'bolts'
INDEX = 'index'
SEQUENCE_NUMBER = 'sequence_number'
BOLT_SQN_FACE = 'bolt_sqn_face'  # bolt sequence number within face
BOLT_SQN_COPLFACE = 'bolt_sqn_coplface'  # bolt sequence number within coplanar main face
BOLT_SQN_NODE = 'bolt_sqn_node'  # bolt sequence number within node


BEAMS = 'beams'
NODE_IDX = 'node_idx'
NODE_IDX0 = 'node_idx0'
NODE_IDX1 = 'node_idx1'
MIDDLE_VECTOR = 'middle_vector'
HEIDX0 = 'heidx0'
HEIDX1 = 'heidx1'
VIDX = 'vidx'
VIDX0 = 'vidx0'
VIDX1 = 'vidx1'
BEAM_START = 'beam_start'
BEAM_END = 'beam_end'
BEAM_CART_POS = 'beam_cart_pos'
FACE_ANGLE = 'face_angle'  # angle of connecting faces
FIDX = 'fidx'   # face id
FIDX0 = 'fidx0'
FIDX1 = 'fidx1'
COPLANAR_FIDX = 'coplanar_fidx'
COPLANAR_FIDXS = 'coplanar_fidxs'
FIIDX = 'fiidx' # finger id
FIIDX0 = 'fiidx0'
FIIDX1 = 'fiidx1'
FIISQN = 'fiisqn'
FIISQN0 = 'fiisqn0'
FIISQN1 = 'fiisqn1'
FIILEN = 'fiilen'
FIILEN0 = 'fiilen1'
FIILEN1 = 'fiilen0'
INC_FIIDX = 'fiidx_inc'
OUT_FIIDX = 'fiidx_out'

LENGTH = "length"
EFFECTIVE_LENGTH = "effective_length"

OFFSET = 'offset'
OFFSET0 = 'offset0'
OFFSET1 = 'offset1'
XBASE = 'x_base'
XBASE0 = 'x_base0'
XBASE1 = 'x_base1'

IS_IGNORED = 'is_ignored'
IS_MELTED = 'is_melted'
POSITION = 'position'
INC_HEIDX = 'inc_heidx' # index of incoming half edge
OUT_HEIDX = 'out_heidx'  # index of outgoing hal fedge
INC_DELTA = 'inc_delta' #
OUT_DELTA = 'out_delta'  #

START_POINT = 'start_point'
END_POINT = 'end_point'

DIRECTION = 'direction'
HORIZONTAL_DIRECTION = 'horizontal_direction'
FACE_NORMAL = 'face_normal'
FACE_NORMAL0 = 'face_normal0'
FACE_NORMAL1 = 'face_normal1'

BOLT_TRUNK_DIAMETER = 'bolt_trunk_diameter'
BOLT_TAIL_DIAMETER = 'bolt_tail_diameter'
BOLT_METRIC_DIAMETER = 'bolt_metric_diameter'

BOLT_LENGTH = 'bolt_length'
BOLT_IS_INSIDE = 'bolt_is_inside'
BOLT_DISTANCE_TO_NEXT = 'bolt_distance_to_next'  #distance to following bolt within same face
IS_ACTIVE = 'is_active'

TRANSFORMATION = 'transformation'
TRANSFORMATION_MATRIX = 'transformation_matrix'
MATRIX = 'matrix'
ORIGIN = 'origin'

UNIT = 'unit'
UNITS = 'units'
DISTANCE_UNITS = 'distance_units'
ANGLE_UNITS = 'angle_units'
DENSITY_UNITS = 'density_units'
WEIGHT_UNITS = 'weight_units'
RADIANS = 'radians'
DEGREES = 'degrees'

CENTIMETER ='centimeter'
METER ='meter'
MILLIMETER ='millimeter'
INCH = 'inch'
G_PER_CM3 = 'g_per_cm3'  # g * cm**-3  gram per qubic centimeter
KG_PER_CM3 = 'kg_per_m3'  # kg * m**-3  kilgram per qubic meter

FONT_NAME = 'font_name'
FONT_SIZE_MM = 'font_size_mm'
FONT_SIZE = 'font_size'
POSITIVE_HEIGHT = 'positive_height'
NEGATIVE_DEPTH = 'negative_depth'

BUMP_HEIGHT = 'bump_height'
BUMP_WIDTH = 'bump_width'
BUMP_DELTA = 'bump_delta'
BUMP_TYPE = 'bump_type'
BUMP_SIMPLE = 'bump_simple'
BUMP_BOLT_DIN912 = 'bump_bolt_din912'
BUMO_BOLT_DIN965 = 'bump_bolt_din965'
BOLT_Z = 'bolt_z'

