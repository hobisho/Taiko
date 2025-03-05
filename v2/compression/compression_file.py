import tensorflow as tf
import numpy as np
import imageio

# 二進位資料
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

# 整數資料
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

# 浮點數資料
def _float32_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))
    

def compression_file(image_list, label):
    # TFRecord 檔名
    tfrecords_filename = 'v2/data/taiko.tfrecords'

    # 建立 TFRecordWriter
    with tf.io.TFRecordWriter(tfrecords_filename) as writer:
        # 取得圖片尺寸
        height, width, depth = image_list.shape

        # 轉換為 bytes
        image_string = image_list.tobytes()

        # 建立 TFRecord Example
        example = tf.train.Example(features=tf.train.Features(feature={
            'height': _int64_feature(height),
            'width': _int64_feature(width),
            'depth': _int64_feature(depth),
            'image_string': _bytes_feature(image_string),
            'label': _float32_feature([label])
        }))

        writer.write(example.SerializeToString())

    print(f"TFRecord '{tfrecords_filename}' 建立完成！")


if __name__ == '__main__':
    image_filename = "v2/data/zip_testing_data\TT -Japanese ver.-_1_7.png"
    image_list = imageio.imread(image_filename)
    my_np_array = np.array(image_list)
    height, width, depth = my_np_array.shape
    print(height, width, depth)
    label = 1
    compression_file(my_np_array, label)

