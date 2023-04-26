from fastai.vision.all import *
from flask import Flask, request, jsonify

# Now you can import the shared module
from shared import label_func

app = Flask(__name__)

learn_inf = load_learner('/Users/sohan/Sohan/workspace/airflow-demo/models/export.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    img_file = request.files['image']
    img = PILImage.create(img_file)
    pred, _, _ = learn_inf.predict(img)
    return jsonify({'prediction': str(pred)})

if __name__ == '__main__':
    app.run(debug=True)