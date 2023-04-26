import sys

from fastai.vision.all import *
from fastai.text.all import *

# Now you can import the shared module
from shared import label_func

images_path = Path('/home/airflow/.fastai/data/oxford-iiit-pet/images')
data_set_path = Path('/opt/airflow/models')

files = get_image_files(images_path)[:50]

# Setup convolutional neural network (cnn)
dls = ImageDataLoaders.from_name_func(
    data_set_path, files, valid_pct=0.2, seed=42,
    label_func=label_func, item_tfms=Resize(224),
)
learn = vision_learner(dls, resnet34, metrics=error_rate)

# Train the model
learn.fine_tune(1)

# Save the model
learn.export()
