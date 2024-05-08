import tensorflow as tf
import os
import numpy as np
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Conv2D, Conv2DTranspose, Add
from tensorflow.keras.layers import BatchNormalization # type: ignore
from keras.preprocessing.image import  img_to_array
import matplotlib.pyplot as plt
from PIL import Image as PILImage


def build_deblur_cnn(input_shape=(256, 256, 3)):
    inputs = Input(shape=input_shape)

    # Initial layers
    x = Conv2D(64, (5,5), activation='relu', padding='same')(inputs)
    x = BatchNormalization()(x)

    # First block with dilated convolution
    x1 = Conv2D(128, (3,3), activation='relu', padding='same', dilation_rate=2)(x)
    x1 = BatchNormalization()(x1)

    # Depth, downsample
    x = Conv2D(128, (3,3), activation='relu', padding='same', strides=(2,2))(x1)
    x = Conv2D(256, (3,3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)

    # Upsample, refine
    x = Conv2DTranspose(128, (3,3), strides=(2,2), padding='same', activation='relu')(x)
    x = Conv2D(64, (3,3), activation='relu', padding='same')(x)

    # Adjust the channel dimensions of x1 before adding
    x1_resized = Conv2D(64, (1,1), activation='relu', padding='same')(x1)  # Use 1x1 conv to adjust channels

    # Implementing the residual connection
    x = Add()([x, x1_resized])  # Adding the adjusted layer

    # Output layer
    outputs = Conv2D(3, (3,3), activation='sigmoid', padding='same')(x)

    model = Model(inputs=inputs, outputs=outputs)

    return model


def load_modeel():
    # Load your model
    #model = build_deblur_cnn()
    #model.compile(optimizer='adam', loss='mean_squared_error')

    model = tf.keras.models.load_model('./Models/deblur_model_11.h5')
    
    
    return model

def preprocess_image(image_url):
    # Preprocess the image as required by your model
    # For example, resize the image to the required input size and normalize pixel values
    target_size=(256,256)
    img = PILImage.open(image_url)
    
    img = img.resize(target_size)
    
    img_array = img_to_array(img)
    img_array = img_array / 255.0
    img_input = np.expand_dims(img_array, axis=0)
    
    return img_input
