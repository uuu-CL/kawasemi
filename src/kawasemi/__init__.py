from . import util

def load(name):
    """load files.

    Parameters
    ----------
    name : str
      a law name.

    Returns
    -------
    kawasemi.models.Statute
      Statute object.

"""
    util.lawNum_to_lawID('明治二十九年法律第八十九号')
    return util.load_model(name)
