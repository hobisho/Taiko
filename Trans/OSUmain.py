import numpy as np
from v2.compression.compression_filepath_labellist import compression_listpath
# from label.tjaread_v3 import parse_tja_file #type:ignore
from v2.split_song.splitv2 import process_audio
from v2.compression.filling import filling_label,biggest_piece
# from label.bk import break_str
from split_song.trans import main

folder = "oni"

def compression (song_sumber,label_list):
    image_filename_list = []
    for numbers in range(1,biggest_piece()):
        image_filename_list.append(f"Trans/data/zip_testing_data/song{song_sumber}/song{song_sumber}_{numbers}.jpg") 
        # print(numbers)
    # print(image_filename_list)
    tfrecords_filename = f'E:\\OUS_tfrecords/osusong{song_sumber}.tfrecords'
    compression_listpath(image_filename_list, label_list,tfrecords_filename)


def image_part(song_sumber)->np.array:
    input_audio = f"data/{folder}/song{song_sumber}" 
    folder_path = "data"
    process_audio(input_audio, folder_path)


if __name__ == "__main__":
    # for song_sumber in range(1,11):
    song_sumber = 1
    bpm,tick,offset,piece,label_list = main(f"eval/song{song_sumber}/song{song_sumber}.osu")
    label_list = filling_label(label_list)
    compression(song_sumber,label_list)
