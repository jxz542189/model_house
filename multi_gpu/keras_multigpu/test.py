from keras import backend as K
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print("gpus",K.tensorflow_backend._get_available_gpus())