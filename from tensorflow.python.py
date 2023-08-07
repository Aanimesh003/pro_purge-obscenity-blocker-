import tensorflow as tf
import numpy as np
np.bool = np.bool_
import tf2onnx
import onnx
from keras.models import load_model

model = load_model("C:\\Users\\ryana\\Downloads\\categorical_classification_Xception.keras")

input_signature = [tf.TensorSpec([300, 300], tf.float32, name='x')]
# Use from_function for tf functions
onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature, opset=13)
onnx.save(onnx_model, "C:\\Users\\ryana\\Downloads\\categorical_classification_Xception.onnx")
