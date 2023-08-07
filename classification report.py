from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report

# Load your trained Keras model
model = load_model('path/to/your/model.keras')

# Specify the path to your validation data directory
validation_data_dir = 'path/to/validation_data_directory'

# Create an ImageDataGenerator for validation data
validation_datagen = ImageDataGenerator(rescale=1.0/255.0)  

# Generate batches of validation data
validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(300, 300),  
    batch_size=32,
    class_mode='categorical'  
)

# Generate predictions on validation data
y_pred_probs = model.predict_generator(validation_generator)

# Convert probabilities to class labels
import numpy as np
y_pred_labels = np.argmax(y_pred_probs, axis=1)

# Get true labels
y_true = validation_generator.labels

# Calculate classification report
report = classification_report(y_true, y_pred_labels)
print(report)




