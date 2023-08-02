import os
import keras
import numpy as np
import keras.utils
import keras.losses
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(300, 300, 3))

    base_model.trainable = False

    batch_size=2000
    epochs=20
    inputs = keras.Input(shape=(300, 300, 3))
    x = base_model(inputs, training=False)
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    predictions = tf.keras.layers.Dense(3, activation='softmax')(x)
    model = tf.keras.Model(inputs=inputs, outputs=predictions)
    loss_fn = keras.losses.CategoricalCrossentropy(from_logits=True)
    optimizer = keras.optimizers.Adam()
    model.compile(optimizer=optimizer, loss=loss_fn, metrics=['accuracy'])

checkpoint_callback = ModelCheckpoint('best_model.keras', monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)

#Train the model on your dataset with backup checkpoints.
checkpoint_dir = '/media/ryana/Trainingstore/'
os.makedirs(checkpoint_dir, exist_ok=True)

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
                                                    batch_size=32,
                                                    class_mode='categorical',
                                                    subset='training')

# Load validation images from the directory and apply preprocessing transformations.
validation_generator = train_datagen.flow_from_directory(train_data_dir,
                                                         target_size=(300, 300),
                                                         batch_size=32,
                                                         class_mode='categorical',
                                                         subset='validation')
try:
    model.fit( train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size,
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
model.save('categorical_classification_InceptionV3.keras')