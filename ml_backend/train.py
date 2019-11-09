from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
import os
from optparse import OptionParser



import audio_model
import generate_training_data as gtd
from td_utils import *



                             
def get_args():
	parser = OptionParser()
	parser.add_option('-b', '--batch-size', dest='batchsize', default=5,
				  type='int', help='batch size')
	
	parser.add_option('-l', '--learning-rate', dest='lr', default=1E-4,
				  type='float', help='learning rate')
	
	parser.add_option('-c', '--load', dest='load',
				  default='../models/tr_model.h5', help='load file model')

	parser.add_option('-d', '--data_location', dest='data_location',
				  default="./raw_data/activates", help='data_location')

	parser.add_option('-o', '--output_folder', dest='output_folder',
				  default="./", help='data_location')


	(options, args) = parser.parse_args()
	return options

if __name__ == '__main__':
	args = get_args()

	Tx = 5511 # The number of time steps input to the model from the spectrogram
	n_freq = 101

	output_model_path=os.path.join(args.output_folder,"tr_model.h5")
	
	activates, negatives, backgrounds = load_raw_audio(args.data_location)
	X, Y = gtd.generate_training_data(backgrounds, activates, negatives)

	model = audio_model.model(input_shape = (Tx, n_freq))
	model = load_model(args.load)

	opt = Adam(lr=args.lr, beta_1=0.9, beta_2=0.999, decay=0.01)
	model.compile(loss='binary_crossentropy', optimizer=opt, metrics=["accuracy"])	

	model.fit(X, Y, batch_size = args.batchsize, epochs=1)

	model.save(output_model_path)
