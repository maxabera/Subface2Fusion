__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from . import app_context as apc
from . import color_constants as color
import adsk
import adsk.core

library_name='Fusion 360 Appearance Library'


def aluminum_glossy_blue_appearance(rgb_color: color.Color):
    lib = apc.app.materialLibraries.itemByName(library_name)
    lib_appear = lib.appearances.itemByName('Aluminum - Anodized Glossy (Blue)')
    # material_name = "Alluminum - Glossy ({})".format(color.get_name(rgb_color))
    # new_appear = apc.design.appearances.addByCopy(lib_appear, material_name)
    # colorProp = adsk.core.ColorProperty.cast(new_appear.appearanceProperties.itemByName('Color'))
    # colorProp.value = adsk.core.Color.create(rgb_color.red, rgb_color.green, rgb_color.blue, 1)
    return lib_appear

def aluminum_glossy_appearance(rgb_color: color.Color):
    lib = apc.app.materialLibraries.itemByName(library_name)
    lib_appear = lib.appearances.itemByName('Aluminum - Anodized Glossy (Blue)')
    material_name = "Alluminum - Glossy ({})".format(color.get_name(rgb_color))
    new_appear = apc.design.appearances.addByCopy(lib_appear, material_name)
    colorProp = adsk.core.ColorProperty.cast(new_appear.appearanceProperties.itemByName('Color'))
    colorProp.value = adsk.core.Color.create(rgb_color.red, rgb_color.green, rgb_color.blue, 1)
    return new_appear


def aluminum_rough_appearance(rgb_color: color.Color):
    lib = apc.app.materialLibraries.itemByName(library_name)
    lib_appear = lib.appearances.itemByName('Aluminum - Satin')
    material_name = "Aluminum - Satin ({})".format(color.get_name(rgb_color))
    new_appear = apc.design.appearances.addByCopy(lib_appear, material_name)
    colorProp = adsk.core.ColorProperty.cast(new_appear.appearanceProperties.itemByName('Color'))
    colorProp.value = adsk.core.Color.create(rgb_color.red, rgb_color.green, rgb_color.blue, 1)
    return new_appear


def plastic_abs_appearance(rgb_color: color.Color):
    lib = apc.app.materialLibraries.itemByName(library_name)
    lib_appear = lib.appearances.itemByName('ABS (White)')
    material_name = "Plastic ABS ({})".format(color.get_name(rgb_color))
    new_appear = apc.design.appearances.addByCopy(lib_appear, material_name)
    colorProp = adsk.core.ColorProperty.cast(new_appear.appearanceProperties.itemByName('Color'))
    colorProp.value = adsk.core.Color.create(rgb_color.red, rgb_color.green, rgb_color.blue, 1)
    return new_appear
