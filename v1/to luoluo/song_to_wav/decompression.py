import tensorflow as tf
import os

def _parse_image_function(example_proto,image_feature_description):
    features = tf.io.parse_single_example(example_proto, image_feature_description)
    features["array"] = tf.io.parse_tensor(features["array"], "uint8")
    return features

def decompression(file):
    raw_image_dataset = tf.data.TFRecordDataset('./tensorflow/song_to_wav/training filder/All_zip/' + file)
    image_feature_description = {"array": tf.io.FixedLenFeature([], tf.string)}
    for features in raw_image_dataset:
        parsed_features = _parse_image_function(features,image_feature_description)
    a = parsed_features.get("array")
    array = a.numpy()
    return array

input_Path = './tensorflow/song_to_wav/training filder/All_zip'
allFileList = os.listdir(input_Path)
for file in allFileList:
      if os.path.isdir(os.path.join(input_Path,file)):
        print("I'm a directory: " + file)
      else:
        array = decompression(file)
        print(array)