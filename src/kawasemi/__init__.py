from . import util

def load(name):
    """load files.

    Parameters
    ----------
    name : str
      A law name.

    Returns
    -------
    kawasemi.models.Statute
      Statute object.

"""
    
    return util.load_model(name)
