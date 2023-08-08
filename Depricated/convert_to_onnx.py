import tensorflow as tf
import numpy as np
np.bool = np.bool_
import tf2onnx
import onnx
from keras.models import load_model

model = load_model("C:\\Users\\Animesh\\Downloads\\BEST_MODEL.keras")
input_shape = (300, 300, 3)
input_signature = [tf.TensorSpec(shape=(None,) + input_shape, dtype=tf.uint8)]
# Use from_function for tf functionsf
onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature, opset=13)
onnx.save(onnx_model,"D:\\pythontt\\onnx_model\\Model(8).onnx")
