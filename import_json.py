import units


class ImportJson:

    def __init__(self, data_json):


        self.import_distance_units = units.Unit.millimeter
        self.import_angle_units = units.Unit.degree

        self._json_attrs = None

    def attr_to_cm(self, param):
        value = units.Distance(self._json_attrs.get(param), self.import_distance_units)
        return value

    def attr_to_deg(self, param):
        value = units.Angle(self._json_attrs.get(param), self.import_angle_units)
        return value
