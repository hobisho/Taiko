import tensorflow as tf
import numpy as np

# TFRecord 檔名
tfrecords_filename = 'dogs.tfrecords'

record_iterator = tf.python_io.tf_record_iterator(path=tfrecords_filename)

for string_record in record_iterator:
  # 建立 Example
  example = tf.train.Example()

  # 解析來自於 TFRecords 檔案的資料
  example.ParseFromString(string_record)

  # 取出 height 這個 Feature
  height = int(example.features.feature['height'].int64_list.value[0])

  # 取出 width 這個 Feature
  width = int(example.features.feature['width'].int64_list.value[0])

  # 取出 image_string 這個 Feature
  image_string = (example.features.feature['image_string'].bytes_list.value[0])

  # 取出 label 這個 Feature
  label = (example.features.feature['label'].float_list.value[0])

  image_1d = np.fromstring(image_string, dtype=np.uint8)
  image = image_1d.reshape((height, width, 3))