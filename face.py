from . import json_strings as JS
from . import part_hole
from . import matrix
from . import json_factory

from typing import List

class Face:

    def __init__(self):

        # core data
        self.fidx = -1
        self.coplanar_to = list()
        self.grounded_polypoints = None   # polygon transformed to XY plane
        self.orig_nv = None   # normal vector of original polygon
        self.transformation_matrix = None  # transformation matrix
        self.holes = list()   # grounded positions of the bolt holes with diameters [hole_n] = (3d_position, diameter, vidx, seq_number)
        self.thickness = 1


    def to_dict(self):
        face_json = {
            JS.FIDX: self.fidx,
            JS.COPLANAR_FIDXS: self.coplanar_to,
            JS.THICKNESS: self.thickness,
            JS.NUMBER_OF_POINTS: len(self.grounded_polypoints),
            JS.POLYPOINTS: self.grounded_polypoints,
            JS.NUMBER_OF_HOLES: len(self.holes),
            JS.HOLES: part_hole.Hole.create_list_dict(self.holes),
            JS.TRANSFORMATION_MATRIX: self.transformation_matrix
        }
        return face_json

    @staticmethod
    def create_list_dict(list_of_faces: List['Face']):
        dict_list_faces = list()
        for h in list_of_faces:
            dict_hole = h.to_dict()
            dict_list_faces.append(dict_hole)
        return dict_list_faces

    @staticmethod
    def create_from_dict(json_face):
        f = Face()
        f.grounded_polypoints = json_face.get(JS.POLYPOINTS, list())
        f.transformation_matrix = json_face.get(JS.TRANSFORMATION_MATRIX, matrix.identity(4))
        f.holes = part_hole.Hole.create_list_from_dict(json_face[JS.HOLES])
        f.thickness = json_face.get(JS.THICKNESS, 1)
        f.fidx = json_face.get(JS.FIDX, -1)
        f.coplanar_to = json_face.get(JS.COPLANAR_FIDXS, list())
        return f


    @staticmethod
    def create_list_from_dict(dict_face_list):
        list_of_faces = list()
        for dh in dict_face_list:
            h = Face.create_from_dict(dh)
            list_of_faces.append(h)
        return list_of_faces
