import io
import json
from . import app_context
from . import attributes
from . import part_node
from . import part_beam
from . import part_bolt

from . import face
from . import json_strings as JS


def load_subface_json(file_path):
    with io.open(file_path, 'r', encoding='utf-8-sig') as f:
        json_doc = json.load(f)
        json_subface = json_doc.get(JS.SUBFACE, dict())
    return json_subface


def read_faces_json(json_subface):
    section = json_subface.get(JS.FACES, dict())
    face_list = face.Face.create_list_from_dict(section)
    return face_list


def read_beams_json(json_subface):
    section = json_subface.get(JS.BEAMS, dict())
    face_list = part_beam.Beam.create_list_from_dict(section)
    return face_list


def read_nodes_json(json_subface):
    section = json_subface.get(JS.NODES, dict())
    node_list = part_node.Node.create_list_from_dict(section)
    return node_list


def read_bolts_json(json_subface):
    section = json_subface.get(JS.BOLTS, dict())
    node_list = part_bolt.Bolt.create_list_from_dict(section)
    return node_list


def read_attributes_json(json_subface):
    section = json_subface.get(JS.ATTRIBUTES, dict())
    attrs = attributes.Attributes.create_from_dict(section)
    return attrs


def key_exists(json_doc, a_key):
    return a_key in json_doc.a_key