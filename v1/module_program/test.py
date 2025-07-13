from decompression import main
from time import perf_counter, sleep

import numpy as np


y_train = main('./v1/module_program/txt_zip')
y_train = y_train.reshape(y_train.shape[0],y_train.shape[1],y_train.shape[2])
y_train = y_train[:7,]

label = np.argmax(y_train[6], axis=1)

# 去除等於3的
filtered_label = label[label != 3]

filtered_label.tolist()  # 將 NumPy 陣列轉換為列表

print(filtered_label,filtered_label.shape)



