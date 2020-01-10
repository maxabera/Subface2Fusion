__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

NONE = 'none'
SUBFACE = 'subface'
VERBOSE = 'verbose'
DEBUGLEVEL = 'debuglevel'
OUTPUTDIR = 'outputdir'
INPUTDIR = 'inputdir'
DATADIR = 'datadir'
DXFDIR = 'dxfdir'
STLDIR = 'stldir'
SCADDIR = 'scaddir'
PROJECT_CONFIG_NAME = 'project_config_name'

# file extensions
EXT_MESH = 'ext_mesh'
EXT_OFFSET_FRAME = 'ext_offset_frame'
EXT_OFFSET_COAT = 'ext_offset_coat'
EXT_OFFSET_SLEEVE = 'ext_offset_sleeve'
EXT_CAT_FRAME = 'ext_cat_frame'
EXT_CAT_COAT = 'ext_cat_coat'
EXT_CAT_SLEEVE = 'ext_cat_sleeve'

FLAG_PRODUCTION = 'flag_production'

DXF_FLIPPED_H = 'dxf_flipped_horizontally'
DXF_FLIPPED_V = 'dxf_flipped_vertically'
DXF_LABEL_MIRRORED = 'dxf_label_mirrored'
DXF_SHOW_LABELS = 'dxf_show_labels'
DXF_LABEL_NUMBER_ONLY = 'dxf_label_number_only'
DXF_SHOW_BOLTS = 'dxf_show_bolts'

SOLUTIONS_DB = 'solutions_db'
SHIFT = 'shift'
IS_REVERSED = 'reversed'
TEMPLATEDIR = 'templatedir'
INPUT_FILE_NO_EXT = 'input_file_no_ext'
INPUT_FILE_MODEL = 'input_file_model'
LOGFILE = 'logfile'
OUTPUT_FORMAT = 'output_format'
OPENSCAD_PATH = 'path'
TEST = 'test'
GEN_COMMENTS = 'gen_comments'
FIRST_JOINT = 'first_joint'
LAST_JOINT = 'last_joint'
SPIRAL_CELL_SIZE = 'spiral_cell_size'
BEAM_DIAMETER = 'beam_diameter'
BEAM_FACES = 'beam_faces'
PHALANX_DIAMETER = 'phalanx_diameter'
PHALANX_FACES = 'phalanx_faces'

BRIDGE_DIAMETER = 'bridge_diameter'
BRIDGE_FACES = 'bridge_faces'

CREATE_BRIDGES = 'create_bridges'
COAT = 'coat'
COAT_GAP = 'coat_gap'
COAT_DENSITY = 'coat_density'

FINGER_DIAMETER = 'finger_diameter'
FINGER_LENGTH = 'finger_length'
FINGER_FACES = 'finger_faces'
FINGER_GAP = 'finger_gap'
UNSPECIFIED = 'unspecified'
BRUTE_FORCE = 'brute_force'
UNIVERSAL = 'universal'
HAND = 'by hand'
MODEL_NAME = 'model_name'
MODEL_SCALE = 'model_scale'
PAD_BASIC_LENGTH = 'pad_basic_length'
PAD_BASIC_WIDTH = 'pad_basic_width'
RECALCULATE_VERTICES = 'recalculate_vertices'
NUM_OF_VERTICES = 'num_of_vertices'
NUM_OF_TRIANGLES = 'num_of_triangles'
NUM_OF_EDGES = 'num_of_edges'
FIRST_TRIANGLE = 'first_triangle'
LAST_TRIANGLE = 'last_triangle'
APPAREL = 'apparel'
AUTO_ELIMINATE_BEAMS = 'eliminate_beams'
NUM_OF_LABEL_COLS = 'num_of_label_cols'
EDGE_DIAMETER = 'edge_diameter'
POINT_VIEW_DIAMETER = 'point_view_diameter'
BEAM_OFFSET='beam_offset'
SCAD_INCLUDE = 'scad_include'
SCAD_INCLUDE_VERSION = 'scad_include_version'
EXECUTED_COMMAND = 'executed_command'
POINT_NDIGITS = 'point_ndigits'
VERSION = 'version'
MARKING_NODE_HEIGHT = 'node_marking_height'
MARKING_NODE_DIAMETER = 'node_marking_diameter'
MANIFOLD_DELTA = 'manifold_delta'
MIN_PLANAR_ANGLE = 'minimal_planar_angle'
REDUCE_CLOSE_BEAMS = 'reduce_close_beams'

EXTRA_FACE_ATTRIBUTES = 'extra_face_attributes'
FACE_ID = 'face_id'
FACE_THICKNESS = 'face_thickness'
FACE_SLEEVE = 'face_sleeve'

INJECT_FRAME = 'FRAME'
INJECT_COAT = 'COAT'

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


# YAML model manipulation
MODEL_TRANSLATE = 'model_translate'

# Physical Parts identification
COUNT_START_FACE = 'count_start_face'
COUNT_START_NODE = 'count_start_node'
MODEL_ID = 'model_id'

# keywords 3d object yaml file
VERTICES = 'vertices'
VERTEX_ID = 'id'
VERTEX = 'vertex'
TRIANGLES = 'triangles'
ALIGN = 'align'
PLANE = 'plane'
BEAMS_TO_IGNORE = 'beams_to_ignore'
BEAMS_FORCED = 'forced_beams'
DRESSED = 'dressed'
NAKED = 'naked'
FRAGMENT = 'fragment'
HEADER = 'header'
POLYGONS = 'polygons'
POLYGON = 'polygon'
FACES_OF_NODES = 'faces_of_nodes'
MODEL = 'model'
MESH = 'mesh'
ENVELOPE = 'envelope'
NODES = 'nodes'
NODE = 'node'
FRAGMENT_TYPE = 'fragment_type'
FRAGMENT_FILE = 'fragment_file'
NODE_ID = 'node_id'
NODE_FINGERS = 'node_fingers'
NODE_PADS = 'node_pads'
NODE_BRIDGES = 'node_bridges'
FINGER_ID = 'finger_id'
FINGER_SEQUENCE_NUMBER = 'finger_sequence_number'
FINGER_SQN0 = 'finger_sequence_number0'
FINGER_SQN1 = 'finger_sequence_number1'
FINGER_HALFEDGE = 'finger_halfedge'
FINGER_HALFEDGE_ID = 'finger_halfedge_id'
FINGER_OFFSET = 'finger_offset'
FINGER_BACK_YARD_POINT_ID = 'finger_back_yard_point_id'
FINGER_BACK_YARD = 'finger_back_yard'
FINGER_ROD_ENCORE = 'finger_rod_encore'
FINGER_POSITION = 'finger_position'

# BOLTS
BOLTS = 'bolts'
FACE_BOLTS_GEN = 'face_bolts_generate'  # generate bolts
FACE_BOLT_DIAMETER = 'face_bolt_diameter'  # diameter of the bolt trunk which, hole in the face
FACE_BOLT_TRUNK_DIAMETER = 'face_bolt_trunk_diameter'  # diameter of the bolt trunk which, hole in the face
FACE_BOLT_TAIL_DIAMETER = 'face_bolt_trunk_diameter'  # diameter of the bolt trunk which, hole in the pad
                            # lower part of bolt. Diameter of the part screw will penetrate.
FACE_BOLT_MARGIN = 'face_bolt_margin'  # minimum distance from the bolt center to the edge
FACE_BOLT_MIN_DISTANCE = 'face_bolt_min_distance'  # minimal distance between 2 bolts in one face

FACE_NODE_PAD_WIDTH = 'face_node_pad_width' # width of the pad facing with particular face

FACE_BOLT_DISTANCE_CLIP = 'face_bolt_distance_clip'  # float, clip distance of bolts on one triangle face (three bolts)
                            # 0 == no clipping  10 == distace will be whole centimeters

FACE_BOLT_LENGTH = 'face_bolt_length' # length of the bolts hole from measured from exterior surface

FACE_DXF_SHOW_BOLTS = 'face_dxf_show_bolts'  # show bolts for this face (independend of global setting)

FINGERS = 'fingers'
PALMS = 'palms'
FACES = 'faces'
ATTRIBUTES = 'attributes'

COORDINATES = 'coordinates'
NODE_IDX = 'node_idx'
NODE_IDX0 = 'node_idx0'
NODE_IDX1 = 'node_idx1'
VIDX = 'vidx'  # vertex index
VIDX0 = 'vidx0'
VIDX1 = 'vidx1'
FIDX = 'fidx'   # face id
FIDX0 = 'fidx0'
FIDX1 = 'fidx1'
FIIDX = 'fiidx' # finger id
FIIDX0 = 'fiidx0'
FIIDX1 = 'fiidx1'
FIISQN = 'fiisqn'
FIISQN0 = 'fiisqn0'
FIISQN1 = 'fiisqn1'
FIILEN = 'fiilen'
FIILEN0 = 'fiilen1'
FIILEN1 = 'fiilen0'
OFFSET = 'offset'
OFFSET0 = 'offset0'
OFFSET1 = 'offset1'
XBASE = 'x_base'
POSITION = 'position'
DIRECTION = 'direction'
NORMAL_VECTOR = 'normal_vector'

EIDX = 'eidx'  # edge id
HEIDX = 'heidx'  # half edge id
HEIDX0 = 'heidx0'
HEIDX1 = 'heidx1'
TRANSFORMATION_MATRIX = "transformation_matrix"
BEAMS = 'beams'
JSON = 'json'

END = 'end'
START = 'start'

END_POSITION = 'end_position'
START_POSITION = 'start_position'

BEAM_START = 'beam_start'
BEAM_START_X = 'beam_start_x'
BEAM_START_Y = 'beam_start_y'
BEAM_START_Z = 'beam_start_z'

BEAM_END = 'beam_end'
BEAM_END_X = 'beam_end_x'
BEAM_END_Y = 'beam_end_y'
BEAM_END_Z = 'beam_end_z'

BEAM_SORT_STYLE = "beam_sort_style"
BEAM_SORT_ZIG_ZAG = "zig_zag"

ANGLE = 'angle'

NUT_PAD = 'nut_pad'
NUT_PAD_SIZE = 'nut_pad_size'

# ACTIONS
ACTIONS = 'actions'
DESIGN_BOLT_PADS = 'design_bolt_pads'
OPTIMIZE_COPLANAR_EDGES = 'optimize_coplanar_edges'

class PropertyItem:

    def __init__(self, section: str, name: str, descr: str = "", default_value=None ):
        self.section = section
        self.name = name
        self.descr = descr
        self.value = default_value

    def get_int(self):
        return int(self.value)

    def get_str(self):
        return self.value

    def get_float(self):
        return float(self.value)

    def get_array_int(self):
        vals = self.value.split(',')
        arr = list()
        for v in vals:
            try:
                av = int(v)
                arr.append(av)
            except ValueError:
                pass
        return arr
