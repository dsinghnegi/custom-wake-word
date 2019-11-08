from pydub import AudioSegment
import numpy as np
from ml_backend.td_utils import *
# import matplotlib.plt as plt
from keras.models import load_model
import tensorflow as tf


MODEL_PATH='./models/tr_model.h5'

class wake_word(object):
	"""docstring for wake_word"""
	def __init__(self):
		super(wake_word, self).__init__()
		self.model_path = MODEL_PATH
	
	def preprocess_audio(self,filename):
		# Trim or pad audio segment to 10000ms
		padding = AudioSegment.silent(duration=10000)
		segment = AudioSegment.from_wav(filename)[:10000]
		segment = padding.overlay(segment)
		# Set frame rate to 44100
		segment = segment.set_frame_rate(44100)
		# Export as wav
		segment.export(filename, format='wav')

	def detect_triggerword(self,filename):
		self.model = load_model(self.model_path)
		self.preprocess_audio(filename)
		# plt.subplot(2, 1, 1)

		x = graph_spectrogram(filename)
		# the spectogram outputs (freqs, Tx) and we want (Tx, freqs) to input into the model
		x  = x.swapaxes(0,1)
		x = np.expand_dims(x, axis=0)
		# global graph
		# with graph.as_default():
		predictions = self.model.predict(x)
		print(predictions)
		
		del self.model
		# plt.subplot(2, 1, 2)
		# plt.plot(predictions[0,:,0])
		# plt.ylabel('probability')
		# plt.show()
		return predictions

