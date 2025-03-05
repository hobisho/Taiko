import imageio
import numpy as np
from compression_file import compression_file
from decompression import decompression #type:ignore


def  overlay_compression(tfrecords_filename:str,newadd_image_list:list, newadd_label_list:list):
    tfrecords_filename = 'v2/data/taiko.tfrecords'
    image_list, label_list = decompression(tfrecords_filename)
    image_list
    compression_file(image_list, label_list)
    
    
if __name__ == '__main__':
    tfrecords_filename =  'v2/data/taiko.tfrecords'
    image_filename = "v2/data/zip_testing_data\TT -Japanese ver.-_1_7.png"
    image_list = imageio.imread(image_filename)
    my_np_array = np.array(image_list)
    height, width, depth = my_np_array.shape
    print(height, width, depth)
    label = 1
    overlay_compression(tfrecords_filename,image_list, label)

