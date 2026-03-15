import numpy as np
import os
import sys
from compression.compression_filepath_labellist import compression_listpath
from label.tjaread_v3 import parse_tja_file #type:ignore
from split_song.splitv2 import process_audio
from compression.filling import filling_label,biggest_piece
from label.bk import break_str

folder = "oni"

def compression (song_number,label_list,file_type:str = "STFT" or "Mel" ):
    image_filename_list = []
    for numbers in range(1,biggest_piece()):
        image_filename_list.append(f"data/{file_type}_Image/song{song_number}/song{song_number}_{numbers}.jpg") 
    tfrecords_path = f'G:\\{file_type}_tfrecords/song{song_number}.tfrecords'
    compression_listpath(image_filename_list, label_list,tfrecords_path)
    image_filename_list.clear()



def labal_part(song_number)->list:
    label_list = parse_tja_file(f"data/{folder}/song{song_number}")
    label_list = break_str(label_list)
    filling_label_list = filling_label(label_list)
    return filling_label_list


def image_part(song_sumber)->np.array:
    input_audio = f"data/{folder}/song{song_sumber}" 
    folder_path = "data"
    process_audio(input_audio, folder_path)


if __name__ == "__main__":
    for song_sumber in range(41,len(os.listdir(f"data/{folder}/"))+1):# len(os.listdir(f"data/{folder}/"))+1
        print("song_sumber:",song_sumber)
        image_part(song_sumber)
        label_list = labal_part(song_sumber)
        compression(song_sumber,label_list,"STFT")
        compression(song_sumber,label_list,"Mel")


    # song_sumber = 31
    # print("song_sumber:",song_sumber)
    # image_part(song_sumber)
    # label_list = labal_part(song_sumber)
    # print(f"compression song{song_sumber}")
    # compression(song_sumber,label_list,"STFT")
    # compression(song_sumber,label_list,"Mel")
