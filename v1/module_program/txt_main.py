from orange import taiko
import os 
import numpy as np
from array_zip_model import comprassion
import tensorflow as tf

global labal
labal =[]

def add(list):
  long=len(list)
  add=1084-long
  t = 0
  if add>0:
    while t<add:
        list.append(4)
        t=t+1
  return list

def txt_main(name):
    song = taiko('./tensorflow/hi/' + name )
    a = [int(c) for c in "".join(song.sheets[0].noteList)]
    print(len(a))
    a = add(a)
    times = len(a)
    time = 0
    while time<1084:
        if a[time] == 0:
            labal.append([1,0,0])
        elif a[time] == 1:
            labal.append([0,1,0])
        elif a[time] == 2:
            labal.append([0,1,0])
        else:
            labal.append([0,0,1])
        time=time + 1


def labal_array(song):
    txt_main(song + ".tja")
    # for file in allFileList:
    #     if os.path.isdir(os.path.join(input_Path,file)):
    #         print("I'm a directory: " + file)
    #     else:
    #         print(file)
    #         txt_main("song 50.tja")
    labal_array = np.array(labal).astype(dtype="int32").tolist()
    # labal_array = np.array(labal_array)
    return labal_array

if __name__ == '__main__':
    song = "song 66"
    a = labal_array(song)
    print(a)
    print(len(a))
    # 假设 'parsed_tensor' 是您的int32类型解析的张量
    a = tf.cast(a, tf.uint8)
    comprassion(a,song + "_txt",'./tensorflow/module/3txt_zip')
