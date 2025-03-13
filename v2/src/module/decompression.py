import tensorflow as tf
import numpy as np


def _parse_function(proto):
    # 定義 TFRecord 格式
    feature_description = {
        'height': tf.io.FixedLenFeature([], tf.int64),
        'width': tf.io.FixedLenFeature([], tf.int64),
        'depth': tf.io.FixedLenFeature([], tf.int64),
        'image_string': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.float32),
    }
    return tf.io.parse_single_example(proto, feature_description)


def decompression(tfrecords_filename):
    # 建立 TFRecordDataset
    dataset = tf.data.TFRecordDataset(tfrecords_filename)

    # 解析 TFRecord
    parsed_dataset = dataset.map(_parse_function)

    # 逐筆讀取 TFRecord
    image_list = []
    label_list = []
    for record in parsed_dataset:
        height = int(record['height'].numpy())
        width = int(record['width'].numpy())
        depth = int(record['depth'].numpy())
        image_string = record['image_string'].numpy()
        label = int(record['label'].numpy())

        # 將 bytes 轉換回 NumPy 陣列
        image_1d = np.frombuffer(image_string, dtype=np.uint8)
        image = image_1d.reshape((height, width, depth))
        image_list.append(image)
        label_list.append(label)

    return image_list, label_list

def _parse_function(proto):
    # 定義 TFRecord 格式
    feature_description = {
        'height': tf.io.FixedLenFeature([], tf.int64),
        'width': tf.io.FixedLenFeature([], tf.int64),
        'depth': tf.io.FixedLenFeature([], tf.int64),
        'image_string': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64),
    }
    
    return tf.io.parse_single_example(proto, feature_description)


if __name__ == '__main__':
    tfrecords_filename = 'v2/data/tfrecords/song1.tfrecords'
    image_list, label_list = decompression(tfrecords_filename)
    image_array = np.array(image_list)
    label_array = np.array(label_list)
    print(image_list[980])
