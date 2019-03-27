#! /usr/bin/python3

import numpy as np
import cv2
import matplotlib.pyplot as plt
import keras
from keras.models import *
from keras.layers import *
from keras import optimizers
from keras.callbacks import *
from scipy.ndimage.filters import *

def fcn8(input_height, input_width, n_classes):
	input_img = Input(shape=(input_height, input_width, 1))
	activation = 'relu'
	
	#Block 1
	x = Conv2D(64, (3,3), activation=activation, padding='same', \
		name='block1_conv1', data_format='channels_last')\
		(input_img)
	x = Conv2D(64, (3,3), activation=activation, padding='same', \
		name='block1_conv2', data_format='channels_last')\
		(x)
	x = MaxPooling2D((2, 2), strides=(2,2), name='block1_pool', \
		data_format='channels_last')(x)

	#Block 2 
	x = Conv2D(128, (3,3), activation=activation, padding='same', \
		name='block2_conv1', data_format='channels_last')\
		(x)
	x = Conv2D(128, (3,3), activation=activation, padding='same', \
		name='block2_conv2', data_format='channels_last')\
		(x)
	x = MaxPooling2D((2, 2), strides=(2,2), name='block2_pool', \
		data_format='channels_last')(x)

	#Block 3
	x = Conv2D(256, (3,3), activation=activation, padding='same', \
		name='block3_conv1', data_format='channels_last')\
		(x)
	x = Conv2D(256, (3,3), activation=activation, padding='same', \
		name='block3_conv2', data_format='channels_last')\
		(x)
	x = Conv2D(256, (3,3), activation=activation, padding='same', \
		name='block3_conv3', data_format='channels_last')\
		(x)
	pool3 = MaxPooling2D((2, 2), strides=(2,2), name='block3_pool', \
		data_format='channels_last')(x)

	#Block 4
	x = Conv2D(512, (3,3), activation=activation, padding='same', \
		name='block4_conv1', data_format='channels_last')\
		(pool3)
	x = Conv2D(512, (3,3), activation=activation, padding='same', \
		name='block4_conv2', data_format='channels_last')\
		(x)
	x = Conv2D(512, (3,3), activation=activation, padding='same', \
		name='block4_conv3', data_format='channels_last')\
		(x)
	pool4 = MaxPooling2D((2, 2), strides=(2,2), name='block4_pool', \
		data_format='channels_last')(x)

	#Block 5
	x = Conv2D(512, (3,3), activation=activation, padding='same', \
		name='block5_conv1', data_format='channels_last')\
		(pool4)
	x = Conv2D(512, (3,3), activation=activation, padding='same', \
		name='block5_conv2', data_format='channels_last')\
		(x)
	x = Conv2D(512, (3,3), activation=activation, padding='same', \
		name='block5_conv3', data_format='channels_last')\
		(x)
	pool5 = MaxPooling2D((2, 2), strides=(2,2), name='block5_pool', \
		data_format='channels_last')(x)

	#Deconvolution pool5
	x = (Conv2D(4096, (16, 16), activation=activation, padding='same', \
		name='conv6', data_format='channels_last'))(pool5)

	x = (Conv2D(4096, (1,1), activation=activation, padding='same', \
		name='conv7', data_format='channels_last'))(x)

	pool5_deconv = (Conv2DTranspose(n_classes, kernel_size=(4, 4),\
		strides=(4, 4), use_bias=False, \
		data_format='channels_last'))(x)

	#Deconvolution pool4
	x = (Conv2D(n_classes, (1,1), activation=activation, padding='same', \
		name='pool4_filetered', data_format='channels_last'))(pool4)
	pool4_deconv = (Conv2DTranspose(n_classes, kernel_size=(2, 2),\
		strides=(2, 2), use_bias=False, \
		data_format='channels_last'))(x)

	#Layer Fusion
	pool3_filtered = (Conv2D(n_classes, (1,1), activation=activation, padding='same', \
		name='pool3_filetered', data_format='channels_last'))(pool3)
	x = Add(name='layer_fusion')([pool5_deconv, pool4_deconv, pool3_filtered])

	#8 Times Deconvolution and Softmax
	x = (Conv2DTranspose(n_classes, kernel_size=(8, 8), strides=(8, 8), \
		use_bias=False, data_format='channels_last'))(x)
	x = (Activation('softmax'))(x)

	return Model(input_img, x)

def unet(input_height, input_width, n_classes):
    inputs = Input(shape=(input_height, input_width, 1))
    
    conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', data_format='channels_last')(inputs)
    conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv1)
    pool1 = MaxPooling2D(strides=(2,2))(conv1)

    conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', data_format='channels_last')(pool1)
    conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv2)
    pool2 = MaxPooling2D(strides=(2, 2))(conv2)

    conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', data_format='channels_last')(pool2)
    conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv3)
    pool3 = MaxPooling2D(strides=(2, 2))(conv3)

    conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', data_format='channels_last')(pool3)
    conv4 = Conv2D(512, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv4)
    drop4 = Dropout(0.5)(conv4)
    pool4 = MaxPooling2D(strides=(2, 2))(drop4)

    conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', data_format='channels_last')(pool4)
    conv5 = Conv2D(1024, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv5)
    drop5 = Dropout(0.5)(conv5)

    up6 = Conv2D(512, 2, activation = 'relu', padding = 'same', data_format='channels_last')(UpSampling2D(size = (2,2))(drop5))
    merge6 = Add(name='layer_fusion1')([drop4, up6])
    conv6 = Conv2D(512, 3, activation = 'relu', padding = 'same', data_format='channels_last')(merge6)
    conv6 = Conv2D(512, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv6)

    up7 = Conv2D(256, 2, activation = 'relu', padding = 'same', data_format='channels_last')(UpSampling2D(size = (2,2))(conv6))
    merge7 = Add(name='layer_fusion2')([conv3, up7])
    conv7 = Conv2D(256, 3, activation = 'relu', padding = 'same', data_format='channels_last')(merge7)
    conv7 = Conv2D(256, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv7)

    up8 = Conv2D(128, 2, activation = 'relu', padding = 'same', data_format='channels_last')(UpSampling2D(size = (2,2))(conv7))
    merge8 = Add(name='layer_fusion3')([conv2, up8])
    conv8 = Conv2D(128, 3, activation = 'relu', padding = 'same', data_format='channels_last')(merge8)
    conv8 = Conv2D(128, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv8)

    up9 = Conv2D(64, 2, activation = 'relu', padding = 'same', data_format='channels_last')(UpSampling2D(size = (2,2))(conv8))
    merge9 = Add(name='layer_fusion4')([conv1, up9])
    conv9 = Conv2D(64, 3, activation = 'relu', padding = 'same', data_format='channels_last')(merge9)
    conv9 = Conv2D(64, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv9)
    conv9 = Conv2D(n_classes, 3, activation = 'relu', padding = 'same', data_format='channels_last')(conv9)

    output = (Activation('softmax'))(conv9)
    return Model(inputs, output)

def load_training():
	x_temp = []
	x_train = []
	y_train = []
	base_frames = '../data/avg_frames/'
	base_masks = '../data/masks/'
	samples = os.listdir(base_frames)
	n_classes = 2
	for sample in samples:	
		x_img = np.load(base_frames + sample).astype(int)
		sample_instance = np.zeros((x_img.shape[0], x_img.shape[1], 1))
		sample_instance[:, :, 0] = x_img
		x_train.append(sample_instance)
		y_img = np.load(base_masks + sample).astype(int)
		mask = np.zeros((y_img.shape[0], y_img.shape[1], n_classes))
		for i in range(n_classes):
			mask[:, :, i] = (y_img == i).astype(int)
		y_train.append(mask)
	x_train = np.array(x_train)
	y_train = np.array(y_train)
	return x_train, y_train

x_train, y_train = load_training()
#model = unet(512, 512, 2)
model = fcn8(512, 512, 2)
model.summary()
sgd = optimizers.SGD(lr=0.01, decay=5**(-4), momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, \
		metrics=['accuracy'])
model_path = '../models/Current_Best.h5'
callbacks=[ModelCheckpoint(filepath=model_path, \
		monitor='val_loss', save_best_only=True)]
model.fit(x_train, y_train, batch_size=1, epochs=20, validation_split=0.1, callbacks=callbacks)
model.save('../models/Full.h5')
