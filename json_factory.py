__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

from . import json_strings as JS
from typing import List
from . import part_hole
from . import face

import logging


def create_json_from_polypoints(poly_points):
    """
    convert polypoints to json document
    :param poly_points: list of [[],[],[]]
    :return: json dictionary
    """

    json_poly_points = {
        JS.NUMBER_OF_POINTS: len(poly_points),
        JS.POLYPOINTS: poly_points
    }

    return json_poly_points


def create_polypoints_from_json(json_polypoints):
    logger = logging.getLogger(__name__ + "." + create_polypoints_from_json.__name__)

    json_poly_points = json_polypoints.get([JS.POLYGON], None)
    assert (json_poly_points is not None), "'{}' object not found in JSON".format(JS.POLYGON)

    polypoints = json_poly_points.get([JS.POLYPOINTS], None)
    assert (polypoints is not None), "'{}' object not found in JSON".format(JS.POINTS)

    n = json_poly_points.get([JS.NUMBER_OF_POINTS], 0)
    if n != len(polypoints):
        logger.error("number of points don't match: {} vs {}".format(n, len(polypoints)))

    return polypoints


