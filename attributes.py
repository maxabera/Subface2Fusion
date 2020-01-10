from . import units
from . import params


class Attributes:

    def __init__(self, ):
        self.finger_diameter = 20
        self.finger_length = 30  # finger default lenth
        self.beam_diameter = 10
        self.palm_basic_width = 5
        self.palm_basic_length = 0
        self.face_thickness = 5
        self.phalanx_diameter = 10.25
        self.model_name = "unknown_name"
        self.model_id = "unknown_id"
        self.import_distance_units = units.Unit.millimeter
        self.import_angle_units = units.Unit.degree

        self._json_attrs = None

    def set_json_source(self, json_data):
        self._json_attrs = json_data

    def to_dict(self):
        attr_json = {
            params.MODEL_NAME: self.model_name,
            params.MODEL_ID: self.model_id,
            params.DISTANCE_UNITS: self.import_distance_units,
            params.ANGLE_UNITS: self.import_distance_units,
            params.FINGER_DIAMETER: self.finger_diameter,
            params.FINGER_LENGTH: self.finger_length,
            params.BEAM_DIAMETER: self.beam_diameter,
            params.PAD_BASIC_WIDTH: self.palm_basic_width,
            params.PAD_BASIC_LENGTH: self.palm_basic_length,
            params.COAT: self.face_thickness,
            params.PHALANX_DIAMETER: self.phalanx_diameter
        }
        return attr_json


    @staticmethod
    def create_from_dict(json_attrs):

        attrs = Attributes()
        attrs._json_attrs = json_attrs
        attrs.model_id = json_attrs.get(params.MODEL_ID)
        attrs.model_name = json_attrs.get(params.MODEL_NAME)
        attrs.import_distance_units = units.str_to_unit(json_attrs.get(params.DISTANCE_UNITS, units.Unit.millimeter))
        attrs.import_angle_units = units.str_to_unit(json_attrs.get(params.ANGLE_UNITS, units.Unit.degree))
        attrs.finger_diameter = json_attrs.get(params.FINGER_DIAMETER, 20)
        attrs.finger_length = json_attrs.get(params.FINGER_LENGTH, 20)
        attrs.beam_diameter = json_attrs.get(params.BEAM_DIAMETER, 10)
        attrs.palm_basic_width = json_attrs.get(params.PAD_BASIC_WIDTH, 5)
        attrs.palm_basic_length = json_attrs.get(params.PAD_BASIC_LENGTH,10)
        attrs.face_thickness = json_attrs.get(params.COAT, 4)
        attrs.phalanx_diameter = json_attrs.get(params.PHALANX_DIAMETER, 10.25)

        return attrs



