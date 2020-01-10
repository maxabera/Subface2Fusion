__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from enum import Enum, unique

PI = 3.141592653589793238462643383279502884197169399375105820974944592307816406286


@unique
class Unit(Enum):
    millimeter = 1
    centimeter = 2
    decimeter = 3
    meter = 4
    inch = 5
    degree = 6
    radian = 7
    g_per_cm3 = 8
    kg_per_m3 = 9
    kilogram = 10
    gram = 11
    liter = 12

    @property
    def cm(self):
        return Unit.centimeter

    @property
    def mm(self):
        return Unit.millimeter

    @property
    def m(self):
        return Unit.meter

    @property
    def dm(self):
        return Unit.decimeter

    @property
    def kg(self):
        return Unit.kilogram

    @staticmethod
    def distance_array(list_of_values, source_unit, dest_unit):
        cvl = list()
        for v in list_of_values:
            a = Distance(v, source_unit)
            cv = a.convert_to(dest_unit)
            cvl.append(cv)

        return cvl

    @staticmethod
    def distance(value, source_unit, dest_unit):
        a = Distance(value, source_unit)
        cv = a.convert_to(dest_unit)
        return cv

    @staticmethod
    def angle(value, source_unit, dest_unit):
        a = Angle(value, source_unit)
        ca = a.convert_to(dest_unit)

    @staticmethod
    def matrix(list_of_values, source_units, dest_units):
        """
        transformation matrix conversion - only position will be converted
        :param list_of_values:
        :param source_units:
        :param dest_units:
        :return:
        """
        new_matrix = list()
        for row_i, row in enumerate(list_of_values):
            row_list = list()
            for col_i, v in enumerate(row):
                cell_cm = v
                if col_i == 3 and row_i < 3:
                    a = Distance(v, source_units)
                    cell_cm = a.convert_to(dest_units)
                row_list.append(cell_cm)
            new_matrix.append(row_list)
        return new_matrix

    @staticmethod
    def matrix_serialize(m, source_units, dest_units):
        """
        transformation matrix serialization into the array of 16 cells
        :param m:
        :param source_units:
        :param dest_units:
        :return:
        """
        # convert
        tm = list()
        for row_i, row in enumerate(m):
            for cell_i, cell in enumerate(row):
                cell_cm = cell
                if cell_i == 3 and row_i < 3:
                    # convert origin coordinates to centimeters
                    cell_dist = Distance(cell, source_units)
                    cell_cm = cell_dist.convert_to(dest_units)
                tm.append(cell_cm)
        return tm




def unit_to_str(unit):
    return unit.name

def unit_to_abbrev(unit):

    if unit == Unit.millimeter:
        return 'mm'
    elif unit == Unit.centimeter:
        return 'cm'
    elif unit == Unit.decimeter:
        return 'dm'
    elif unit == Unit.meter:
        return 'm'
    elif unit == Unit.kilogram:
        return 'kg'
    elif unit == Unit.gram:
        return 'g'

    return "units.unit_to_abbrev(): conversion not implemented"


def unit_to_abbrev_squared(unit):
    return "{}\u00B2".format(unit_to_abbrev(unit))

def str_to_unit(unit_as_string):
    if unit_as_string == 'mm':
        return Unit.millimeter
    elif unit_as_string == 'cm':
        return Unit.centimeter
    elif unit_as_string == 'dm':
        return Unit.decimeter
    elif unit_as_string == 'm':
        return Unit.meter
    elif unit_as_string == 'inch':
        return Unit.inch
    if unit_as_string == 'millimeter':
        return Unit.millimeter
    elif unit_as_string == 'centimeter':
        return Unit.centimeter
    elif unit_as_string == 'meter':
        return Unit.meter
    elif unit_as_string == 'meters':
        return Unit.meter
    elif unit_as_string == 'rad':
        return Unit.radian
    elif unit_as_string == 'deg':
        return Unit.degree
    elif unit_as_string == 'radian':
        return Unit.radian
    elif unit_as_string == 'degree':
        return Unit.degree
    elif unit_as_string == 'radians':
        return Unit.radian
    elif unit_as_string == 'degrees':
        return Unit.degree
    elif unit_as_string == 'g_per_cm3':
        return Unit.g_per_cm3
    elif unit_as_string == 'kg_per_m3':
        return Unit.kg_per_m3
    elif unit_as_string == 'kilogram':
        return Unit.kilogram
    elif unit_as_string == 'gram':
        return Unit.gram
    elif unit_as_string == 'kg':
        return Unit.kilogram
    elif unit_as_string == 'g':
        return Unit.gram
    else:
        return Unit.millimeter


class Distance:

    def __init__(self, value, unit):
        self._orig_value = value
        self._orig_unit = unit

    def convert_to(self, dest_unit):
        if dest_unit == Unit.millimeter:
            return self.mm
        if dest_unit == Unit.centimeter:
            return self.cm
        if dest_unit == Unit.decimeter:
            return self.dm
        if dest_unit == Unit.meter:
            return self.m

    @property
    def mm(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value * 10.0
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value * 100.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value * 1000.0
        elif self._orig_unit == Unit.inch:
            return self._orig_value * 25.4

        else:  # in strange case, return the same value
            return self._orig_value

    @property
    def cm(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value / 10.0
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value * 10.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value * 100.0
        elif self._orig_unit == Unit.inch:
            return (self._orig_value * 25.4) / 10.0
        else:  # in strange case, return the same value
            return self._orig_value

    @property
    def dm(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value / 100.0
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value / 10
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value
        elif self._orig_unit == Unit.meter:
            return self._orig_value * 10.0
        elif self._orig_unit == Unit.inch:
            return (self._orig_value * 25.4) / 100.0
        else:  # in strange case, return the same value
            return self._orig_value

    @property
    def m(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value / 1000.0
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value / 100.0
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value / 10.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value
        elif self._orig_unit == Unit.inch:
            return (self._orig_value * 25.4) / 1000

        else:  # in strange case, return the same value
            return self._orig_value

class Angle:

    def __init__(self, value, unit):
        self._orig_value = value
        self._orig_unit = unit

    @property
    def rad(self):
        if self._orig_unit == Unit.radian:
            return self._orig_value
        elif self._orig_unit == Unit.degree:
            return (self._orig_value * PI) / 180.0
        else:
            return self._orig_value

    @property
    def deg(self):
        if self._orig_unit == Unit.radian:
            return (self._orig_value * 180.0) / PI
        elif self._orig_unit == Unit.degree:
            return self._orig_value
        else:
            return self._orig_value


    def convert_to(self, dest_unit):
        if dest_unit == Unit.radian:
            return self.rad
        if dest_unit == Unit.deg:
            return self.deg
        return self._orig_value

class Area:

    def __init__(self, value, unit):
        self._orig_value = value
        self._orig_unit = unit

    @property
    def mm_sq(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value * 100.0
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value * 10000.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value * 1000000.0
        elif self._orig_unit == Unit.inch:
            return self._orig_value * 25.4*25.4

        else:  # in strange case, return the same value
            return self._orig_value

    @property
    def cm_sq(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value / 100.0
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value * 100.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value * 10000.0
        elif self._orig_unit == Unit.inch:
            return (self._orig_value * 25.4*25.4) / 100.0

        else:  # in strange case, return the same value
            return self._orig_value

    @property
    def dm_sq(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value / 10000
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value / 100.0
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value
        elif self._orig_unit == Unit.meter:
            return self._orig_value * 100
        else:  # in strange case, return the same value
            return self._orig_value


    @property
    def m(self):
        return self.m_sq

    @property
    def m_sq(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value / 1000000.0
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value / 10000.0
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value / 100.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value
        elif self._orig_unit == Unit.inch:
            return (self._orig_value * 25.4*25.4) / 1000000

        else:  # in strange case, return the same value
            return self._orig_value

class Volume:

    def __init__(self, value, unit):
        self._orig_value = value
        self._orig_unit = unit


    @property
    def mm3(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value * 1000.0
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value * 1000000.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value * 1000000000.0
        elif self._orig_unit == Unit.inch:
            return self._orig_value * 25.4*25.4

        else:  # in strange case, return the same value
            return self._orig_value

    @property
    def cm3(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value / 1000.0
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value * 1000.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value * 1000000.0
        elif self._orig_unit == Unit.inch:
            return (self._orig_value * 25.4*25.4) / 100.0

        else:  # in strange case, return the same value
            return self._orig_value

    @property
    def m3(self):
        if self._orig_unit == Unit.millimeter:
            return self._orig_value / 1000000000.0
        elif self._orig_unit == Unit.centimeter:
            return self._orig_value / 1000000.0
        elif self._orig_unit == Unit.decimeter:
            return self._orig_value / 1000.0
        elif self._orig_unit == Unit.meter:
            return self._orig_value
        elif self._orig_unit == Unit.inch:
            return (self._orig_value * 25.4*25.4*25.4) / 100000000

        else:  # in strange case, return the same value
            return self._orig_value



class Density:

    def __init__(self, value, unit):
        self._orig_value = value
        self._orig_unit = unit

    @property
    def g_per_cm3(self):
        if self._orig_unit == Unit.g_per_cm3:
            return self._orig_value
        elif self._orig_unit == Unit.kg_per_m3:
            return self._orig_value/1000
        else:
            return self._orig_value

    @property
    def kg_per_m3(self):
        if self._orig_unit == Unit.g_per_cm3:
            return self._orig_value * 1000
        elif self._orig_unit == Unit.kg_per_m3:
            return self._orig_value
        else:
            return self._orig_value


class Weight:

    def __init__(self, value, unit):
        self._orig_value = value
        self._orig_unit = unit

    @property
    def g(self):
        return self.gram

    @property
    def kg(self):
        return self.kilogram

    @property
    def gram(self):
        if self._orig_unit == Unit.gram:
            return self._orig_value
        elif self._orig_unit == Unit.kilogram:
            return self._orig_value/1000
        else:
            return self._orig_value

    @property
    def kilogram(self):
        if self._orig_unit == Unit.gram:
            return self._orig_value * 1000
        elif self._orig_unit == Unit.kilogram:
            return self._orig_value
        else:
            return self._orig_value



def distance_array(list_of_values, source_unit, dest_unit):
    cvl = list()
    for v in list_of_values:
        a = Distance(v, source_unit)
        cv = a.convert_to(dest_unit)
        cvl.append(cv)

    return cvl

def distance(value, source_unit, dest_unit):
    a = Distance(value, source_unit)
    cv = a.convert_to(dest_unit)
    return cv

def angle(value, source_unit, dest_unit):
    a = Angle(value, source_unit)
    ca = a.convert_to(dest_unit)



def matrix(list_of_values, source_units, dest_units):
    new_matrix = list()
    for row_i, row in enumerate(list_of_values):
        row_list = list()
        for col_i, v in enumerate(row):
            cell_cm = v
            if col_i == 3 and row_i < 3:
                a = Distance(v, source_units)
                cell_cm = a.convert_to(dest_units)
            row_list.append(cell_cm)
        new_matrix.append(row_list)
    return new_matrix


def matrix_serialize(m, source_units, dest_units):
    # convert
    tm = list()
    for row_i, row in enumerate(m):
        for cell_i, cell in enumerate(row):
            cell_cm = cell
            if cell_i == 3 and row_i < 3:
                # convert origin coordinates to centimeters
                cell_dist = Distance(cell, source_units)
                cell_cm = cell_dist.convert_to(dest_units)
            tm.append(cell_cm)
    return tm