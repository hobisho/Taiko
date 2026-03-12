import numpy as np
import os
import sys
from compression.compression_filepath_labellist import compression_listpath
from label.tjaread_v3 import parse_tja_file #type:ignore
from split_song.splitv2 import process_audio
from compression.filling import filling_label,biggest_piece
from label.bk import break_str

folder = "oni"

def compression (song_number,label_list):
    image_filename_list = []
    for numbers in range(1,biggest_piece()):
        image_filename_list.append(f"v2/data/zip_testing_data/song{song_number}/song{song_number}_{numbers}.jpg") 
    # print(dir(image_filename_list))
    tfrecords_filename = f'G:\\tfrecords/song{song_number}.tfrecords'
    compression_listpath(image_filename_list, label_list,tfrecords_filename)


def labal_part(song_number)->list:
    label_list = parse_tja_file(f"v2/data/{folder}/song{song_number}")
    label_list = break_str(label_list)
    filling_label_list = filling_label(label_list)
    return filling_label_list


def image_part(song_sumber)->np.array:
    input_audio = f"v2/data/{folder}/song{song_sumber}"  # 你的音檔
    song_output_folder = "v2/data/split_ogg"  # 儲存資料夾
    jpg_output_folder = f"v2/data/zip_testing_data"
    process_audio(input_audio, song_output_folder,jpg_output_folder)


if __name__ == "__main__":
    for song_sumber in range(31,71):# len(os.listdir(f"v2/data/{folder}/"))+1
        print("song_sumber:",song_sumber)
        image_part(song_sumber)
        label_list = labal_part(song_sumber)
        print(f"compression song{song_sumber}")
        compression(song_sumber,label_list)

    # song_sumber = 31
    # # image_part(song_sumber)
    # label_list = labal_part(song_sumber)
    # compression(song_sumber,label_list)
