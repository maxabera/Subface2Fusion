__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

def common_name(preffix, main, suffix, num, digits):

    """
    ppp_mmm000_sss
    """

    s = ""
    if len(preffix)>0:
        s += "{}_".format(preffix)

    if len(main)>0:
        s += "{}_".format(main)

    s += "{}_{}_{}".format(preffix, main, suffix)