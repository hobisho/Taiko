import os
import numpy as np
from compression.compression_filepath import compression_listpath
from label.tjaread import parse_tja_file #type:ignore
from split_song.splitv2 import process_audio
from compression.filling import filling_label,biggest_piece
from label.bk import break_str

def compression (song_sumber,label_list):
    image_filename_list = []
    for numbers in range(1,biggest_piece()):
        image_filename_list.append(f"v2/data/zip_testing_data/song{song_sumber}/song{song_sumber}_{numbers}.jpg") 
    tfrecords_filename = f'v2/data/tfrecords/song{song_sumber}.tfrecords'
    compression_listpath(image_filename_list, label_list,tfrecords_filename)


def labal_part(song_number)->np.array:
    label_list = parse_tja_file(f"v2/data/level 6~7/song{song_number}")
    label_list = break_str(label_list)
    filling_label_list = filling_label(label_list)
    return filling_label_list


def image_part(song_sumber)->np.array:
    input_audio = f"v2/data/level 6~7/song{song_sumber}"  # 你的音檔
    song_output_folder = "v2/data/split_ogg"  # 儲存資料夾
    jpg_output_folder = f"v2/data/zip_testing_data"
    process_audio(input_audio, song_output_folder,jpg_output_folder)


if __name__ == "__main__":
    song_sumber = 2
    # image_part(song_sumber)
    label_array = labal_part(song_sumber)
    compression(song_sumber,label_array)
    # labal_part(5)
    # compression_file(label_array,image_array,tfrecords_filename)
    # overlay_compression(label_array,image_array,tfrecords_filename)