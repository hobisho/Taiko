import sys, os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from module.decompression import decompression

if __name__ == '__main__':
    tfrecords_filename = 'v2/data/song1.tfrecords'
    image_list, label_list = decompression(tfrecords_filename)
    image_array = np.array(image_list)
    label_array = np.array(label_list)
    print(image_list[980])