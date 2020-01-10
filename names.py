

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