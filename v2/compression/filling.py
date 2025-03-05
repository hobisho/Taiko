from split_song.readdata import TjaData
import numpy as np
from PIL import Image
import os


def biggest_piece():
    a=[]
    biggest=0
    for i in range(1, len(os.listdir("v2/data/level 6~7/"))+1):
        path_name = f'v2/data/level 6~7/song{i}'
        a=TjaData(path_name)
        if (max (biggest,a.Piece())!=biggest):
            biggest = a.Piece()
            # biggest_path_name = path_name
    return biggest
#1760piece
#song16


def filling_label(label_list)->np.array:
    biggest = biggest_piece()
    while (len(label_list)<biggest):
        label_list.append(-1)
    label_array = np.array(label_list)
    return label_array


def filling_image(image_list)->np.array:
    print(type(image_list))
    biggest = biggest_piece()
    image_array = np.array(image_list)
    w,h,z =image_array[0].shape
    filling_array = np.ones((w,h,z))*(-1)
    while (len(image_list)<biggest):
        image_list.append(filling_array)
    image_array = np.array(image_list)
    return image_array

if __name__ == '__main__':
    image_path = "v2/data/zip_testing_data/song1/song1_1.jpg"
    image = Image.open(image_path)
    image = image.convert("RGB") 
    image_matrix = np.array(image)
    
    image_path_1 = "v2/data/zip_testing_data/song1/song1_2.jpg"
    image_1 = Image.open(image_path_1)
    image_1 = image_1.convert("RGB") 
    image_matrix_1 = np.array(image_1)
    
    a = []
    a.append(image_matrix)
    a.append(image_matrix_1)
    
    filling_image(a)
    print(a[3])
    # filling_label([0])
