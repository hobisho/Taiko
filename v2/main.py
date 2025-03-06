import os
import numpy as np
from compression.compression_file import compression_file
from label.tjaread import parse_tja_file #type:ignore
from split_song.splitv2 import process_audio
from compression.filling import filling_label,filling_image
from label.bk import break_str
from compression.Overlay import overlay_compression



def labal_part(song_number)->np.array:
    print(song_number)
    label_list = parse_tja_file(f"v2/data/level 6~7/song{song_number}")
    label_list = break_str(label_list)
    filling_label_array = filling_label(label_list)
    return filling_label_array


def image_part(song_sumber)->np.array:
    input_audio = f"v2/data/level 6~7/song{song_sumber}"  # 你的音檔
    song_output_folder = "v2/data/split_ogg"  # 儲存資料夾
    jpg_output_folder = f"v2/data/zip_testing_data"
    image_array = process_audio(input_audio, song_output_folder,jpg_output_folder)
    # filling_image_array = filling_image(image_array)
    # return filling_image_array

# if __name__ == "__main__":
#     tfrecords_filename = 'v2/data/taiko.tfrecords'
#     label_array_list = []
#     image_array_list = []
#     for i in range(1, len(os.listdir("v2/data/level 6~7/"))+1):
#         label_array_list.append(labal_part(i)) 
#         image_array_list.append(image_part(i))
#         compression_file(label_array_list,image_array_list,tfrecords_filename)


if __name__ == "__main__":
    tfrecords_filename = 'v2/data/taiko.tfrecords'
    # label_array = labal_part(3)
    image_array = image_part(5)
    # compression_file(label_array,image_array,tfrecords_filename)
    # overlay_compression(label_array,image_array,tfrecords_filename)