from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Model, load_model, Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Input, Masking, TimeDistributed, LSTM, Conv1D
from tensorflow.keras.layers import GRU, Bidirectional, BatchNormalization, Reshape
from tensorflow.keras.optimizers import Adam



def model(input_shape):
	X_input = Input(shape = input_shape)
	
	
	X = Conv1D(196, kernel_size=15, strides=4)(X_input)                                 # CONV1D
	X = BatchNormalization()(X)                                 # Batch normalization
	X = Activation('relu')(X)                                 # ReLu activation
	X = Dropout(0.8)(X)                                 # dropout (use 0.8)

	X = GRU(units = 128, return_sequences = True)(X) # GRU (use 128 units and return the sequences)
	X = Dropout(0.8)(X)                                 # dropout (use 0.8)
	X = BatchNormalization()(X)                                 # Batch normalization
	
	X = GRU(units = 128, return_sequences = True)(X)   # GRU (use 128 units and return the sequences)
	X = Dropout(0.8)(X)                                 # dropout (use 0.8)
	X = BatchNormalization()(X)                                  # Batch normalization
	X = Dropout(0.8)(X)                                  # dropout (use 0.8)
	
	X = TimeDistributed(Dense(1, activation = "sigmoid"))(X) # time distributed  (sigmoid)

	
	model = Model(inputs = X_input, outputs = X)
	
	return model

# Tx = 5511 # The number of time steps input to the model from the spectrogram
# n_freq = 101

# model = model(input_shape = (Tx, n_freq))
# model.summary()
