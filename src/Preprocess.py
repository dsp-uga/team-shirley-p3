#! /usr/bin/python3

import json
import os
import numpy as np
import cv2

def unzip_dirs():
	base = '../../data/'
	dirs = os.listdir(base)
	for dir_name in dirs:
		os.system('unzip ' + base + dir_name + ' -d ' + base)

def avg_frames():
	base = '../../data/'
	dirs = os.listdir(base)
	for dir_name in dirs:
		frames = os.listdir(base + dir_name + '/images/')
		first_frame = cv2.imread(base + dir_name + '/images/' + frames[0])
		height = first_frame.shape[0]
		width = first_frame.shape[1]
		output = np.zeros((height, width))	
		for frame in frames:
			temp_frame = cv2.imread(base + dir_name + '/images/' + frame)
			for i in range(height):
				for j in range(width):
					output[i][j] += temp_frame[i][j][0] / len(frames)
		np.save('../data/avg_frames/' + dir_name +  '.npy', output)

def create_masks():
	base = '../../data/'
	dirs = os.listdir(base)
	for dir_name in dirs:
		mask = np.zeros((512, 512))
		regions = json.load(open(base + dir_name + '/regions/regions.json'))
		for region in regions:
			for pair in region['coordinates']:
				mask[pair[0]][pair[1]] = 1
		np.save('../data/masks/' + dir_name + '.npy', mask)

#unzip_dirs()
#avg_frames()
create_masks()
