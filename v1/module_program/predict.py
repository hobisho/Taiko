from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding, Dropout
from keras.layers import LSTM, SimpleRNN, GRU
import tensorflow as tf
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Activation, Flatten, Reshape, TimeDistributed
from keras.layers import Input,Conv3D,Conv2D, MaxPooling3D, ZeroPadding2D, ConvLSTM3D,  ConvLSTM2D
from keras.metrics import AUC
from decompression import main
from txt_main      import labal_array
from orange import taiko


X_train = main('./v1\module_program\BIG_ZIP')
# X_train = np.array(X_train[1])
X_train=X_train.reshape( X_train.shape[0], X_train.shape[1] ,X_train.shape[2] ,X_train.shape[3],3).astype("float32") #convlstm(,1,23,32,3)
X_train = X_train.astype('float32')/255
print(X_train.shape)
y_train = main('./v1/module_program/txt_zip')
# y_train = np.array(y_train[1])
print(y_train.shape)
y_train = y_train.reshape(y_train.shape[0],y_train.shape[1],y_train.shape[2])
# print(X_train)
d=0
r=0
b=0
n=0
t = 0
for i in y_train[:,]:
    for j in i:
        if j[0] == 1:
            d += 1
        elif j[1] == 1:
            r += 1
        # elif j[2] == 1:
        #     b += 1
        else:
            n += 1
        t += 1
print(t)
weight = np.array([t-d,t-r,t-n])/t
weight = list(weight)
print(weight)


model = load_model('v1/TaikoCLSTM.h5')
result = model.predict(X_train[0:])

weight_array = np.array([1 , 10.6 , 13.432458 , 0.6])#4.56 [1 , 10.5333 , 13.432458 , 0.6
t=0
one=0
two=0
th=0
while t<912:
	j = result[0][t]
	k = j * weight_array
	k = k.tolist()
	# if (k[1]>0.33):
	# 	out = 1
	# else:
	maxs = np.where(k==np.max(k))
	a = maxs[0]
	a = a.tolist()
	out = a[0]
	one = one + k[0]
	two = two + k[1]
	th = th + k[2]
	print(out,end = "")
	if (t%16==15):
		print(",")
	# print(np.max(k))
	t=t+1

# print(result)
print(one/two)
print(one/th)




	# maxs=np.where(k==np.max(k))
	# # print(type(maxs))
	# a = maxs[0]
	# a = a.tolist()
	# if len(maxs[0])>1:
	# 	if (a[len(maxs[0])-1]==3)&(len(maxs[0])>2):
	# 		o = a[len(maxs[0])-2]
	# 	else:
	# 		o = a[len(maxs[0])-1]
	# o = a[0]
	# print(o,",",end = "")

	
# 	t=t+1
