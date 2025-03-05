from   compression import compression
from decompression import decompression #type:ignore

if __name__ == '__main__':
    tfrecords_filename = 'v2/data/taiko.tfrecords'
    image_list, label_list = decompression(tfrecords_filename)
