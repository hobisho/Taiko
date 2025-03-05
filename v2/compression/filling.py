from split_song.readdata import TjaData
import numpy as np
from PIL import Image


def biggest_piece():
    a=[]
    biggest=0
    for i in range(1,67):
        path_name = f'v2/data/level 6~7/song{i}'
        a=TjaData(path_name)
        if (max (biggest,a.Piece())!=biggest):
            biggest = a.Piece()
            # biggest_path_name = path_name
    return biggest

def filling_label(label_list):
    biggest = biggest_piece()
    label_array = np.array(label_list)
    while (len(label_array)<biggest):
        label_array.append(4)
    return label_array


def filling_image(image_list):
    biggest = biggest_piece()
    w,h,z,n =image_list.shape
    filling_array = np.zeros((w,h,z))
    filling_list = list(filling_array)
    while (len(image_list)<biggest):
        image_list.append(filling_list)
    return image_list

if __name__ == '__main__':
    image_path = "spectrogram.png"
    image = Image.open(image_path)
    image = image.convert("RGB") 
    image_matrix = np.array(image)
    filling_image(image_matrix)
    # filling_label([0])
