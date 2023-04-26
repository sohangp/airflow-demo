from fastai.vision.all import *
from pathlib import Path


def get_pet_detector_training_data():
    print("Downloading data set...")

    # Get the images from Oxford-IIIT Pet Dataset and untar.
    path = untar_data(URLs.PETS)/'images'

    print("Finished downloading data set to path: ", str(path))
    return path
