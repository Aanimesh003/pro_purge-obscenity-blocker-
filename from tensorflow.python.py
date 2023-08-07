import tensorflow as tf
import tf2onnx
import onnx
from keras.models import load_model

model = load_model("C:\\Users\\Animesh\\Downloads\\categorical_classification_Xception.keras")

input_signature = [tf.TensorSpec([3, 3], tf.float32, name='x')]
# Use from_function for tf functions
onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature, opset=13)
onnx.save(onnx_model, "D:\\pythontt\\onnx_model\\model.onnx")
