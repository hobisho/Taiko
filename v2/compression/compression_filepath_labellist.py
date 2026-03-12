import tensorflow as tf
import imageio
import os
import numpy as np
import sys
sys.path.append(r"v2/label")
from numbertolist import numbertolist

# 二進位資料
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

# 整數資料
def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

# 浮點數資料
def _float32_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

# 圖片檔案名稱列表
def compression_listpath(image_filename_list:list, label_list:list,tfrecords_filename:str ='v2/data/taiko.tfrecords'):

    # 建立 TFRecordWriter
    with tf.io.TFRecordWriter(tfrecords_filename) as writer:
        for image_filename, label in zip(image_filename_list, label_list):
            if not os.path.exists(image_filename):
                # print(f"檔案 {image_filename} 不存在，跳過")
                image_filename = "v2/data/white_image.jpg"
            # 讀取圖片
            image = imageio.imread(image_filename)
            label_array = np.array(numbertolist(label),dtype=np.uint8)

            # 取得圖片尺寸
            height, width, depth = image.shape

            # 轉換為 bytes
            image_string = image.tobytes()
            label_string = label_array.tobytes()

            # 建立 TFRecord Example
            example = tf.train.Example(features=tf.train.Features(feature={
                'height': _int64_feature(height),
                'width': _int64_feature(width),
                'depth': _int64_feature(depth),
                'image_string': _bytes_feature(image_string),
                'label_string': _bytes_feature(label_string)
            }))

            writer.write(example.SerializeToString())

    print(f"TFRecord '{tfrecords_filename}' 建立完成！")
    

if __name__ == '__main__':
    image_filename_list = []
    label_list = []
    for numbers in range(1,1000):
        image_filename_list.append(f"v2/data/zip_testing_data/song1/song1_{numbers}.jpg") 
        label_list.append(1)
    compression_listpath(image_filename_list, label_list)