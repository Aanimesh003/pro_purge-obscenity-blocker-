import os
from tensorflow.keras.models import Model
from keras import backend as K
from tensorflow.keras.callbacks import ModelCheckpoint
from keras.models import load_model
from PIL import ImageFile

def save_model_and_weights(model):
# Save the entire model (architecture + weights).
   model_path = ('/media/ryana/Trainingstore/BestXception.keras')
   model.save(model_path)
   print("Model saved at epoch . Path:",model_path)

model = load_model("/media/ryana/Trainingstore/BEST_MODEL")
save_model_and_weights(model)
print("Saved")