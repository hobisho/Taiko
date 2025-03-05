import numpy as np
from PIL import Image
from compression.compression_file import compression_file
from compression.decompression import decompression 


def  overlay_compression(tfrecords_filename:str,newadd_image_list:list, newadd_label_list:list):
    tfrecords_filename = 'v2/data/taiko.tfrecords'
    image_list, label_list = decompression(tfrecords_filename)
    
    image_list.append(newadd_image_list)
    label_list.append(newadd_label_list)
    
    compression_file(image_list, label_list, tfrecords_filename)
    

if __name__ == '__main__':
    tfrecords_filename =  'v2/data/taiko.tfrecords'
    image_path = "v2/data/zip_testing_data/song1/song1_3.jpg"
    image = Image.open(image_path)
    image = image.convert("RGB") 
    image_array = np.array(image)
    
    label = 1
    
    overlay_compression(tfrecords_filename,image_array, label)

