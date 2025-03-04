import tensorflow as tf
import numpy as np

# TFRecord 檔名
tfrecords_filename = 'taiko.tfrecords'

# 建立 TFRecordDataset
dataset = tf.data.TFRecordDataset(tfrecords_filename)

# 定義 TFRecord 格式
feature_description = {
    'height': tf.io.FixedLenFeature([], tf.int64),
    'width': tf.io.FixedLenFeature([], tf.int64),
    'depth': tf.io.FixedLenFeature([], tf.int64),
    'image_string': tf.io.FixedLenFeature([], tf.string),
    'label': tf.io.FixedLenFeature([], tf.float32),
}

# 解析函式
def _parse_function(proto):
    return tf.io.parse_single_example(proto, feature_description)

# 解析 TFRecord
parsed_dataset = dataset.map(_parse_function)

# 逐筆讀取 TFRecord
for record in parsed_dataset:
    height = int(record['height'].numpy())
    width = int(record['width'].numpy())
    depth = int(record['depth'].numpy())
    image_string = record['image_string'].numpy()
    label = float(record['label'].numpy())

    # 將 bytes 轉換回 NumPy 陣列
    image_1d = np.frombuffer(image_string, dtype=np.uint8)
    image = image_1d.reshape((height, width, depth))

    print(f"讀取圖片: {height}x{width}，標籤: {label}，data{image}")

