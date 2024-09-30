import tensorflow as tf
import matplotlib.pyplot as plt
import os 
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'




def _parse_image_function(example_proto):
    return tf.io.parse_single_example(example_proto, image_feature_description)

def decompression():
    raw_image_dataset = tf.data.TFRecordDataset('./tensorflow/txt/aexample.tfrecords')
    global image_feature_description 
    image_feature_description= { "image_raw": tf.io.FixedLenFeature([], tf.string) }
    for features in raw_image_dataset:
        image_features = _parse_image_function(features)
        image_raw = image_features['image_raw']
        image_array = tf.image.decode_jpeg(image_raw)
    a = image_array.numpy()
    print(a)
decompression()