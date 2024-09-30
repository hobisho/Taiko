from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding, Dropout
from keras.layers import LSTM, SimpleRNN, GRU
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Activation, Flatten, Reshape, TimeDistributed
from keras.layers import Input,Conv3D,Conv2D, MaxPooling2D, ZeroPadding2D, ConvLSTM3D,  ConvLSTM2D
from keras.metrics import AUC
from decompression import main
import numpy as np




X_train = main('./tensorflow/module/BIG_ZIP')
X_train=X_train.reshape(X_train.shape[0], X_train.shape[1] ,X_train.shape[2] ,X_train.shape[3],3).astype("float32")/255 #convlstm(,1,23,32,3)
X_train = X_train[:7,]

print(X_train.shape)

y_train = main('./tensorflow/module/txt_zip')
y_train = y_train.reshape(y_train.shape[0],y_train.shape[1],y_train.shape[2])
y_train = y_train[:7,]

print(y_train.shape)

d = 0
r = 0
b = 0
n = 0
t = 0
for i in y_train[:,]:
    for j in i:
        if j[0] == 1:
            d += 1
        elif j[1] == 1:
            r += 1
        elif j[2] == 1:
            b += 1
        else:
            n += 1
        t += 1
print(t)
weight = np.array([t-d,t-r,t-b,t-n])/t
weight = list(weight)
print(weight)

# print(X_train)
# print(y_train)

# song_name = "song 1"
# path='./tensorflow/module/BIG_ZIP'
# X_train = decompression(path + "/" + song_name + ".tfrecords","take")
# X_train= np.array(X_train)
# X_train=X_train.reshape(1, X_train.shape[0] ,X_train.shape[1] ,X_train.shape[2],3).astype("float32") #convlstm(,1,23,32,3)
# X_train = X_train.astype('float32')/255
# print(X_train.shape)
# y_train = labal_array()
# print(y_train.shape)
# y_train = y_train.reshape(1,y_train.shape[0],y_train.shape[1])




network = Sequential()
network.add(
    TimeDistributed(
        Conv2D(
            32, 
            (3,3),
            padding = 'same', 
            strides = 1
        ),
        input_shape = (X_train.shape[1], 23, 32, 3)
    ))

network.add(TimeDistributed(MaxPooling2D((2,2))))
network.add(TimeDistributed(Conv2D(32, (3,3),
                padding='same', strides = 1)))
network.add(TimeDistributed(Flatten()))
network.add(TimeDistributed(Dense(256,activation="relu")))
network.add(LSTM(64,return_sequences='True'))
network.add(Dense(4, activation = 'softmax'))

network.compile( optimizer = 'adam', loss = 'binary_crossentropy',
	             metrics = [AUC()] ,loss_weights = weight) 
print( network.summary() )

network.fit(X_train, y_train, epochs= 15, batch_size=X_train.shape[1])

network.save('TaikoCLSTM.h5')
