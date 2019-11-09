import numpy as np
from pydub import AudioSegment
import random
import sys
import io
import os
import glob
import IPython
from td_utils import *


Tx = 5511 # The number of time steps input to the model from the spectrogram
n_freq = 101 # Number of frequencies input to the model at each time step of the spectrogram
Ty = 1375 # The number of time steps in the output of our model

def get_random_time_segment(segment_ms):
	"""
	Gets a random time segment of duration segment_ms in a 10,000 ms audio clip.
	
	Arguments:
	segment_ms -- the duration of the audio clip in ms ("ms" stands for "milliseconds")
	
	Returns:
	segment_time -- a tuple of (segment_start, segment_end) in ms
	"""
	
	segment_start = np.random.randint(low=0, high=10000-segment_ms)   # Make sure segment doesn't run past the 10sec background 
	segment_end = segment_start + segment_ms - 1
	
	return (segment_start, segment_end)


def is_overlapping(segment_time, previous_segments):
	"""
	Checks if the time of a segment overlaps with the times of existing segments.
	
	Arguments:
	segment_time -- a tuple of (segment_start, segment_end) for the new segment
	previous_segments -- a list of tuples of (segment_start, segment_end) for the existing segments
	
	Returns:
	True if the time segment overlaps with any of the existing segments, False otherwise
	"""
	
	segment_start, segment_end = segment_time
   
	overlap = False
	
	for previous_start, previous_end in previous_segments:
		if segment_start <= previous_end and segment_end >= previous_start:
			overlap = True
   
	return overlap



def insert_audio_clip(background, audio_clip, previous_segments):
	"""
	Insert a new audio segment over the background noise at a random time step, ensuring that the 
	audio segment does not overlap with existing segments.
	
	Arguments:
	background -- a 10 second background audio recording.  
	audio_clip -- the audio clip to be inserted/overlaid. 
	previous_segments -- times where audio segments have already been placed
	
	Returns:
	new_background -- the updated background audio
	"""
	
	segment_ms = len(audio_clip)
	
	segment_time = get_random_time_segment(segment_ms)
	
	while is_overlapping(segment_time, previous_segments):
		segment_time = get_random_time_segment(segment_ms)

	previous_segments.append(segment_time)
	new_background = background.overlay(audio_clip, position = segment_time[0])
	
	return new_background, segment_time


def insert_ones(y, segment_end_ms):
	"""
	Update the label vector y. The labels of the 50 output steps strictly after the end of the segment 
	should be set to 1. By strictly we mean that the label of segment_end_y should be 0 while, the
	50 followinf labels should be ones.
	
	
	Arguments:
	y -- numpy array of shape (1, Ty), the labels of the training example
	segment_end_ms -- the end time of the segment in ms
	
	Returns:
	y -- updated labels
	"""
	
	segment_end_y = int(segment_end_ms * Ty / 10000.0)
	
	for i in range(segment_end_y + 1, segment_end_y + 51):
		if i < Ty:
			y[0, i] = 1
	
	return y


def create_training_example(background, activates, negatives):
	"""
	Creates a training example with a given background, activates, and negatives.
	
	Arguments:
	background -- a 10 second background audio recording
	activates -- a list of audio segments of the word "activate"
	negatives -- a list of audio segments of random words that are not "activate"
	
	Returns:
	x -- the spectrogram of the training example
	y -- the label at each time step of the spectrogram
	"""
	
	# Set the random seed
	np.random.seed(18)
	
	# Make background quieter
	background = background - 20

	y = np.zeros((1, Ty))

	previous_segments = []
	number_of_activates = np.random.randint(0, 5)
	random_indices = np.random.randint(len(activates), size=number_of_activates)
	random_activates = [activates[i] for i in random_indices]
	
	for random_activate in random_activates:
		background, segment_time = insert_audio_clip(background, random_activate, previous_segments)
		segment_start, segment_end = segment_time
		y = insert_ones(y, segment_end_ms=segment_end)
	number_of_negatives = np.random.randint(0, 3)
	random_indices = np.random.randint(len(negatives), size=number_of_negatives)
	random_negatives = [negatives[i] for i in random_indices]

	for random_negative in random_negatives:
		background, _ = insert_audio_clip(background, random_negative, previous_segments)

	# Standardize the volume of the audio clip 
	background = match_target_amplitude(background, -20.0)

	# Export new training example 
	file_handle = background.export("train" + ".wav", format="wav")
	print("File (train.wav) was saved in your directory.")
	
	# Get and plot spectrogram of the new recording (background with superposition of positive and negatives)
	x = graph_spectrogram("train.wav")
	
	return x, y



def generate_training_data(backgrounds, activates, negatives):
	X=[]
	Y=[]
	for bkg in backgrounds:
		x,y=create_training_example(bkg, activates, negatives)
		X.append(x.T)
		Y.append(y.T)
	return np.array(X),np.array(Y)







