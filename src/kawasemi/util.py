from . import models

def load_model(filename):
    return models.Statute(filename)
