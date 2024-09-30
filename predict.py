import numpy as np
import os
import sys
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import tensorflow as tf

# Hide GPU from visible devices
tf.config.set_visible_devices([], 'GPU')
img_rows = None
img_cols = None
digits_in_img = 5
model = None
np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})

def predict(file_name):
    
    # load model
    if os.path.isfile('model/cnn_model.h5'):
        model = models.load_model('model/cnn_model.h5')
    else:
        print('No trained model found.')
        exit(-1)
    img = load_img(file_name, color_mode='grayscale')
    img_array = img_to_array(img)
    img_rows, img_cols, _ = img_array.shape
    x_list = list()
    for i in range(digits_in_img):
        step = img_cols // digits_in_img
        x_list.append(img_array[:, i * step:(i + 1) * step] / 255)

    varification_code = list()
    np_x_list=np.array(x_list)
    model_result=model.predict(np_x_list,verbose=0)
    result=np.argmax(model_result,axis=1)
    code=''
    for i in result:
        code+=str(i)
    return code



#this is for predict a single file that user selected
def main():
    # Hide GPU from visible devices
    tf.config.set_visible_devices([], 'GPU')
    img_rows = None
    img_cols = None
    digits_in_img = 5
    model = None
    np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})

    def split_digits_in_img(img_array):
        x_list = list()
        for i in range(digits_in_img):
            step = img_cols // digits_in_img
            x_list.append(img_array[:, i * step:(i + 1) * step] / 255)
        return x_list

    # load model
    if os.path.isfile('model/cnn_model.h5'):
        model = models.load_model('model/cnn_model.h5')
    else:
        print('No trained model found.')
        exit(-1)

    # load img to predict
    if len(sys.argv) > 1:
        img_filename = sys.argv[1]
    else:
        img_filename = input('Varification code img filename: ')
    img = load_img(img_filename, color_mode='grayscale')
    img_array = img_to_array(img)
    img_rows, img_cols, _ = img_array.shape
    x_list = split_digits_in_img(img_array)

    # predict
    varification_code = list()
    np_x_list=np.array(x_list)
    model_result=model.predict(np_x_list,verbose=0)
    result=np.argmax(model_result,axis=1)

    print('Predicted varification code:', result)
    code=''
    for i in result:
        code+=str(i)
    print(code)

if __name__ == '__main__':
    main()
