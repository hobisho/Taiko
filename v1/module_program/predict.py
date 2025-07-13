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


def to_binary(chart):
    # 0: 無敲擊, 1/2: 有敲擊
    return [int(x > 0) for x in chart]

def direct_comparison(x, y):
    return np.mean(np.array(x) == np.array(y))

def onset_comparison(human, ai, tolerance=1):
    human_bin = to_binary(human)
    ai_bin = to_binary(ai)
    hit_count = 0
    total_count = 0
    L = len(human_bin)
    for i in range(L):
        if human_bin[i] == 1:
            total_count += 1
            match = False
            for j in range(max(0, i-tolerance), min(L, i+tolerance+1)):
                if ai_bin[j] == 1:
                    match = True
                    break
            if match:
                hit_count += 1
    return hit_count / total_count if total_count > 0 else 0


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


model = load_model('v1/V1TaikoCLSTM.h5')
result = model.predict(X_train[0:])
all_ochuman= 0
all_dcrand = 0
all_dchuman = 0

ll= [0, 1, 2, 3, 5, 6]  # 假設有7首歌

for baba in ll:
	h = result.reshape(8, 1084, 4)  # 將結果重塑為 (1, 1084, 4) 的形狀
	probabilities = h[baba]  # 取出第二到第四個類別的機率

	print("=====",probabilities.shape,result.shape)

	k = []
	p = 0
	evg = [0, 0, 0, 0]

	# 計算前num_frame的平均
	for i in range(500):
		a = probabilities[i]
		for j in range(4):
			evg[j] += a[j]
			
	evg = [v / 500 for v in evg]

	# 決策
	for i in range(1084):
		a = probabilities[i]
		if a[1] > evg[1]:
			print(0, end="")
			k.append(0)
			p += 1
		elif a[2] > evg[2]:
			print(1, end="")
			k.append(1)
			p += 1
		elif a[3] > evg[3]:
			print(2, end="")
			k.append(2)
			p += 1
		else:	
			print(3, end="")
			k.append(3)
			p += 1
		if i % 16 == 15:
			print(",")
	print(k)

	y_train = main('./v1/module_program/txt_zip')
	y_train = y_train.reshape(y_train.shape[0],y_train.shape[1],y_train.shape[2])
	y_train = y_train[:7,]

	label = np.argmax(y_train[baba], axis=1)

	# 去除等於3的
	human_chart = label[label != 3]

	human_chart.tolist()  # 將 NumPy 陣列轉換為列表

	print(len(k))

	k = k[:len(human_chart)]  # 確保 k 的長度與 human_chart 相同


	# 你的 k 是AI生成的譜面
	ai_chart = k  # 你的 AI output (0/1/2 list)
	# 讓兩個長度一樣，避免IndexError
	min_len = min(len(human_chart), len(ai_chart))
	human_chart = human_chart[:min_len]
	ai_chart = ai_chart[:min_len]

	# 指標計算
	np.random.seed(42)
	random_chart = np.random.choice([0, 1, 2], size=len(ai_chart))
	dcrand = direct_comparison(to_binary(ai_chart), to_binary(random_chart))
	dchuman = direct_comparison(to_binary(ai_chart), to_binary(human_chart))
	ochuman = onset_comparison(human_chart, ai_chart, tolerance=1)
    
	if ochuman > 0.96:
		best = baba
		best_ochuman = ochuman
		best_dcrand = dcrand
		best_dchuman = dchuman

	all_dcrand = all_dcrand + dcrand
	all_dchuman = all_dchuman + dchuman
	all_ochuman = all_ochuman + ochuman

	print(f"DCRand  (與亂數一致率)      : {dcrand:.4f}")
	print(f"DCHuman (與人類準確率)      : {dchuman:.4f}")
	print(f"OCHuman (寬容onset準確率)   : {ochuman:.4f}")
    

evg_dcrand = all_dcrand / len(ll)
evg_dchuman = all_dchuman / len(ll)
evg_ochuman = all_ochuman / len(ll)
print(f"平均 DCRand  (與亂數一致率)      : {evg_dcrand:.4f}")
print(f"平均 DCHuman (與人類準確率)      : {evg_dchuman:.4f}")
print(f"平均 OCHuman (寬容onset準確率)   : {evg_ochuman:.4f}")
print(f"最佳 DCRand  (與亂數一致率)      : {best_dcrand:.4f}")
print(f"最佳 DCHuman (與人類準確率)      : {best_dchuman:.4f}")
print(f"最佳 OCHuman (寬容onset準確率)   : {best_ochuman:.4f}")
