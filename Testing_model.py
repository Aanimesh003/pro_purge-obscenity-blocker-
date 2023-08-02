import keras
import numpy as np
from keras.preprocessing.image import load_img, img_to_array

# Load the model
model = keras.models.load_model("C:\\Users\\Animesh\\Downloads\\model_checkpoint_epoch.keras")

# Load the image
img = load_img("D:\project_dataset\check_script\image_19.jpg" , target_size=(300, 300))

# Convert the image to a numpy array
input_data = img_to_array(img)

# Normalize the pixel values
input_data /= 255.0

# Add a dimension to match the model's input shape
input_data = np.expand_dims(input_data, axis=0)

# Make a prediction
prediction = model.predict(input_data)

# Find the class with the highest probability
predicted_class = np.argmax(prediction)

print(predicted_class)

if predicted_class == 0:
    print("Unsafe")
if predicted_class == 1:
    print("Sexy")
if predicted_class == 2: