import tensorflow as tf
import os
import numpy as np
from array_zip_model import comprassion
from keras import backend as K #转换为张量
from time import process_time, sleep


def _parse_image_function(example_proto,image_feature_description):
    features = tf.io.parse_single_example(example_proto, image_feature_description)
    features["array"] = tf.io.parse_tensor(features["array"], "uint8")
    return features

def decompression(file_path,hii = ""):
    raw_image_dataset = tf.data.TFRecordDataset(file_path)#'./tensorflow/song_to_wav/training filder/All_zip/' +file
    image_feature_description = {"array": tf.io.FixedLenFeature([], tf.string)}
    for features in raw_image_dataset:
        parsed_features = _parse_image_function(features,image_feature_description)
    a = parsed_features.get("array")
    if hii=="takeout":
      a = np.array(a)
    return a

def main(path):
  train = []
  input_Path = path
  allFileList = os.listdir(input_Path)
  t=1
  for file in allFileList:
    if os.path.isdir(os.path.join(input_Path,file)):
      print("I'm a directory: " + file)
    else:
      print(t)
      print(file)
      file_path = path + "/" + file
      # print("\n\n\n\n",file_path,"\n\n\n\n")
      list = decompression(file_path)
      list = np.array(list)
      train.append(list)
      # print(list[0])
      t=t+1
  array = np.array(train,dtype = int)
  return array


def add(list):
  list = list.tolist()
  long=len(list)
  add=1084-long
  add_array=np.zeros((23,32,3),dtype=int)
  add_list = add_array.tolist()
  t = 0
  if add>0:
    while t<add:
        list.append(add_list)
        t=t+1
  elif add<0:
     print("error")
     return
  return list

if __name__ == '__main__':
  start = process_time()
  global mix
  mix = False #是否要混合
  song =False
  song_name = "song 59"#50、57、58、59、60、61、63、66
  if mix:
    path='./tensorflow/song_to_wav/training filder' + "/" + song_name + "/" + "zip_filder"#'./tensorflow/song_to_wav/training filder/All_zip'
    a = main(path)
    a = add(a)
    print(len(a))
    end = process_time()
    a = tf.cast(a, tf.uint8)
    comprassion(a,song_name,'./tensorflow/module/BIG_ZIP')
  else:
    if song:
      path='./tensorflow/module/BIG_ZIP'#'./tensorflow/song_to_wav/training filder/All_zip' # './tensorflow/song_to_wav/training filder' + "/" + song_name,"zip_filder"
      a = decompression(path + "/" + song_name + ".tfrecords","takeout")
    else:
      path='./tensorflow/module/3txt_zip'#'./tensorflow/song_to_wav/training filder/All_zip' # './tensorflow/song_to_wav/training filder' + "/" + song_name,"zip_filder"
      a = decompression(path + "/" + song_name + "_txt.tfrecords","takeout")
    print(a)
    print(len(a))
    end = process_time()
  
  print(end - start)

  