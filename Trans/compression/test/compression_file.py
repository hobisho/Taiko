import tensorflow as tf
import imageio
import numpy as np
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
def compression_file(image_array_list:list, label_list:list,tfrecords_filename:str ='v2/data/taiko.tfrecords'):
    # 建立 TFRecordWriter
    with tf.io.TFRecordWriter(tfrecords_filename) as writer:
        for image_array, label in zip(image_array_list, label_list):
            # 取得圖片尺寸
            time, height, width, depth = image_array.shape
            # 轉換為 bytes
            image_string = image_array.tobytes()
            # print(label)
            label_string = label.tobytes()
            # print(label_string)

            # 建立 TFRecord Example
            example = tf.train.Example(features=tf.train.Features(feature={
                'height': _int64_feature(height),
                'width': _int64_feature(width),
                'depth': _int64_feature(depth),
                'time': _int64_feature(time),
                'image_string': _bytes_feature(image_string),
                'label_string': _bytes_feature(label_string)
            }))

            writer.write(example.SerializeToString())

    print(f"TFRecord '{tfrecords_filename}' 建立完成！")
    

if __name__ == '__main__':
    image_filename = "v2/data/zip_testing_data/song1/song1_1.jpg"
    image_list = imageio.imread(image_filename)
    my_np_array = np.array(image_list)
    my_np_array.tolist()
    
    image_filename1 = "v2/data/zip_testing_data/song1/song1_2.jpg"
    image_list1 = imageio.imread(image_filename1)
    my_np_array1 = np.array(image_list1)
    my_np_array1.tolist()
    
    image_filename2 = "v2/data/zip_testing_data/song1/song1_1.jpg"
    image_list2 = imageio.imread(image_filename2)
    my_np_array2 = np.array(image_list2)
    my_np_array2.tolist()
    
    image_filename3 = "v2/data/zip_testing_data/song1/song1_2.jpg"
    image_list3 = imageio.imread(image_filename3)
    my_np_array3 = np.array(image_list3)
    my_np_array3.tolist()
    
    a=[]
    a.append(my_np_array)
    a.append(my_np_array1)
    a=np.array(a)
    
    b=[]
    b.append(my_np_array2)
    b.append(my_np_array3)
    b=np.array(b)
    
    # print(a.shape)
    k=[a,b]

    label = [1,2]
    label=np.array(label)
    
    label1 = [4,3]
    label1=np.array(label1)
    
    la=[label,label1]
    print(label1.shape)
    
    compression_file(k, la)

