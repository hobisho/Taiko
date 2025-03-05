import tensorflow as tf
import imageio
import os

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
def compression_list(image_filename_list, label_list):
    # TFRecord 檔名
    tfrecords_filename = 'v2/data/taiko.tfrecords'

    # 建立 TFRecordWriter
    with tf.io.TFRecordWriter(tfrecords_filename) as writer:
        for image_filename, label in zip(image_filename_list, label_list):
            if not os.path.exists(image_filename):
                print(f"檔案 {image_filename} 不存在，跳過")
                continue

            # 讀取圖片
            image = imageio.imread(image_filename)

            # 取得圖片尺寸
            height, width, depth = image.shape

            # 轉換為 bytes
            image_string = image.tobytes()

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
    image_filename_list = []
    label_list = []
    for numbers in range(1,10):
        image_filename_list.append(f"zip_testing_data\TT -Japanese ver.-_{numbers}_7.png") 
        label_list.append(1)
    compression_list(image_filename_list, label_list)

