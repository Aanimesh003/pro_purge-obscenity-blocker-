import os
import numpy as np
import keras.utils
import keras.losses
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications import Xception
from keras import backend as K
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    base_model = Xception(weights='imagenet', include_top=False, input_shape=(300, 300, 3))

    base_model.trainable = False
    Batch_size=400
    epochs=25
    inputs = keras.Input(shape=(300, 300, 3))
    x = base_model(inputs, training=False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    predictions = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    model = tf.keras.Model(inputs=inputs, outputs=predictions)
    loss_fn = keras.losses.BinaryCrossentropy(from_logits=True)
    optimizer = keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss=loss_fn, metrics=['accuracy'])

#Train the model on your dataset with backup checkpoints.
checkpoint_dir = '/media/ryana/Trainingstore/'
os.makedirs(checkpoint_dir, exist_ok=True)

best_model_checkpoint_dir = '/media/ryana/Trainingstore/BEST_MODEL.keras'
#os.makedirs(best_model_checkpoint_dir, exist_ok=True)

checkpoint_callback = ModelCheckpoint(best_model_checkpoint_dir, monitor='val_accuracy', save_best_only=True, mode='max')

def save_model_and_weights(model):
      # Save the entire model (architecture + weights).
   model_path = os.path.join(checkpoint_dir, f'model_checkpoint_epoch.keras')
   model.save(model_path)
   print("Model saved at epoch . Path:",model_path)


train_data_dir = '/media/ryana/Trainingstore/Dataset/training/'
train_datagen = ImageDataGenerator(rescale=1.0/255.0,  # Rescale pixel values to [0, 1].
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   validation_split=0.2)  # Split data into training and validation sets.

# Load training images from the directory and apply preprocessing transformations.
train_generator = train_datagen.flow_from_directory(train_data_dir,
                                                    target_size=(300, 300),
                                                    batch_size=Batch_size,
                                                    class_mode='binary',
                                                    subset='training')

# Load validation images from the directory and apply preprocessing transformations.
validation_generator = train_datagen.flow_from_directory(train_data_dir,
                                                         target_size=(300, 300),
                                                         batch_size=Batch_size,
                                                         class_mode='binary',
                                                         subset='validation')
try:
    print("Training New Model")
    model.fit( train_generator,
    steps_per_epoch=train_generator.samples // Batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // Batch_size,
    epochs=epochs,
    callbacks=[checkpoint_callback])
    save_model_and_weights(model)

except Exception as e:
    # In case of any unexpected issue during training, save the current model and weights before exiting.
   save_model_and_weights(model)
   print(f"Training was interrupted with error: {e}")
   print("The current model and weights have been saved.")

# Step 8: Load the latest saved model and weights if training was interrupted.
#latest_epoch = 10  # Replace this with the epoch number of the latest saved model.
#latest_model_path = os.path.join(checkpoint_dir, f'model_checkpoint_epoch_{latest_epoch}.h5')
#model = tf.keras.models.load_model(latest_model_path)

# Step 9: Save the trained model for later use.
"""""
model.save('/media/ryana/Trainingstore/categorical_classification_Xception.keras')
print("MODEL SAVED ?")


with strategy.scope():
    print("Training Retrived_Model")
    new_model = load_model("/media/ryana/Trainingstore/BEST_MODEL")
    new_model.fit(train_generator,
    steps_per_epoch=train_generator.samples // Batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // Batch_size,
    epochs=epochs,
    callbacks=[checkpoint_callback])
    
    new_model.save('final_model.keras')
    """