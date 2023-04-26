from fastai.vision.all import *

# Now you can import the shared module
from shared import label_func

# Load the learner from the export.pkl file
learn = load_learner(Path('/opt/airflow/models/export.pkl'))

# Load the test image
test_img = PILImage.create('/opt/airflow/data/cat.jpg')

# Get the predicted class and confidence
pred_class, pred_idx, probs = learn.predict(test_img)

# Print the predicted class and confidence
print(f"***** CAT class: {pred_class}; Probability: {probs[pred_idx]:.04f}")

# Load the test image
dog_img = PILImage.create('/opt/airflow/data/dog.jpg')

# Get the predicted class and confidence
pred_class, pred_idx, probs = learn.predict(dog_img)

# Print the predicted class and confidence
print(f"*****DOG class: {pred_class}; Probability: {probs[pred_idx]:.04f}")
