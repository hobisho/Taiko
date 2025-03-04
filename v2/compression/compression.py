import tensorflow as tf
from skimage import io

# 二進位資料
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

# 整數資料
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

# 浮點數資料
def _float32_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

# 圖片檔案名稱
image_filename_list = ['dog-0.jpg', 'dog-1.jpg', 'dog-2.jpg'];

# 標示資料
label_list = [1.0, 1.2, 0.6]

# TFRecord 檔名
tfrecords_filename = 'taiko.tfrecords'

# 建立 TFRecordWriter
writer = tf.python_io.TFRecordWriter(tfrecords_filename)

for image_filename, label in zip(image_filename_list, label_list):
    # 圖取圖檔
    image = io.imread(image_filename)

    # 取得圖檔尺寸資訊
    height, width, depth = image.shape

    # 序列化資料
    image_string = image.tostring()

    # 建立包含多個 Features 的 Example
    example = tf.train.Example(features=tf.train.Features(feature={
        'height': _int64_feature(height),
        'width': _int64_feature(width),
        'image_string': _bytes_feature(image_string),
        'label': _float32_feature([label])}))

    writer.write(example.SerializeToString())

# 關閉 TFRecordWriter
writer.close()