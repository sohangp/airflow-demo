from fastai.vision.all import *

# Now you can import the shared module
from pet_detector.shared import label_func

def validate_success():
    # Load the learner from the export.pkl file
    learn = load_learner(Path('/opt/airflow/models/export.pkl'))

    # Load the test image
    test_img = PILImage.create('/opt/airflow/data/cat.jpg')

    # Get the predicted class and confidence
    success_output = learn.predict(test_img)

    # Print the predicted class and confidence
    print("CAT: ", str(success_output))

    # Load the test image
    dog_img = PILImage.create('/opt/airflow/data/dog.jpg')

    # Get the predicted class and confidence
    failure_output = learn.predict(dog_img)

    # Print the predicted class and confidence
    print("DOG: ", str(failure_output))
