__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from . import vector
import adsk
import adsk.core
from . import matrix

def move_bodies(new_comp, bodies_collection, move_vec):
    if vector.is_zero(move_vec):
        return bodies_collection
    move_vector = adsk.core.Vector3D.create(move_vec[0], move_vec[1], move_vec[2])
    move_matrix = adsk.core.Matrix3D.create()
    move_matrix.translation = move_vector
    move_feats = new_comp.features.moveFeatures
    move_feature_input = move_feats.createInput(bodies_collection, move_matrix)
    move_feats.add(move_feature_input)
    return bodies_collection

def transform_bodies(new_comp, bodies_collection, transf_matrix):

    if matrix.is_zero(transf_matrix):
        return bodies_collection

    tm_serialized = matrix.serialize(transf_matrix)
    move_matrix = adsk.core.Matrix3D.create()
    move_matrix.setWithArray(tm_serialized)
    move_feats = new_comp.features.moveFeatures
    move_feature_input = move_feats.createInput(bodies_collection, move_matrix)
    move_feats.add(move_feature_input)


def translate(new_comp, obj_collection, translation_matrix):
    if not matrix.is_zero(translation_matrix):
        transform = adsk.core.Matrix3D.create()
        tm_serialized = matrix.serialize(translation_matrix)
        transform.setWithArray(tm_serialized)
        moveFeats = new_comp.features.moveFeatures
        moveFeatureInput = moveFeats.createInput(obj_collection, transform)
        moveFeats.add(moveFeatureInput)
    return obj_collection

def append_to_collection(bodies_collection, target_collection):
    for i in range(bodies_collection.count):
        target_collection.add(bodies_collection.item(i))
    return target_collection

class FusionPart:

    def __init__(self):

        self.positive_bodies = None
        self.negative_bodies = None

    def build_object(self, new_comp):

        if self.positive_bodies is None:
            self.positive_bodies = self.create_positive_bodies(new_comp)

        if self.negative_bodies is None:
            self.negative_bodies = self.create_negative_bodies(new_comp)

        return self.positive_bodies

    def create_positive_bodies(self, new_comp):
        return adsk.core.ObjectCollection.create()

    def create_negative_bodies(self, new_comp):
        return adsk.core.ObjectCollection.create()


