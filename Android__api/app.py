from flask import Flask,request,jsonify
import numpy as np
import base64

import onnxruntime as ort
import numpy as np

model_path = "C:\Users\Lenovo\OneDrive\Pictures\BEST_model.onnx"
session = ort.InferenceSession(model_path)

def predict(input_data):
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    input_data = input_data.astype(np.float16)
    output = session.run([output_name], {input_name: input_data})
    return output[0]

app = Flask(__name__)


if __name__ == '_main_':
    app.run()


@app.route('/predict', methods=['POST'])
def make_prediction():
    image_data = request.form.files('image')
    image_bytes = base64.b64decode(image_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    input_data = image_array.astype(np.float16) / 255.0  # Normalize the image
    predictions = predict(input_data)
    return jsonify(predictions.tolist())
















