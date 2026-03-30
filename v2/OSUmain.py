import numpy as np
from compression.compression_filepath_labellist import compression_listpath
# from label.tjaread_v3 import parse_tja_file #type:ignore
from Trans.splitosu import process_audio
from compression.filling import filling_label,biggest_piece
# from label.bk import break_str
from Trans.transTja import main

folder = "eval"

def compression (song_number,label_list):
    image_filename_list = []
    for numbers in range(1,biggest_piece()+1):
        image_filename_list.append(f"data/osu_Image/song{song_number}/song{song_number}_{numbers}.jpg") 
    tfrecords_filename = f'G:\\Osu_tfrecords/song{song_sumber}.tfrecords'
    compression_listpath(image_filename_list, label_list,tfrecords_filename)
    image_filename_list.clear()

def image_part(song_sumber,bpm,offset,piece)->np.array:
    input_audio = f"data/{folder}/song{song_sumber}" 
    folder_path = "data"
    process_audio(input_audio, folder_path,bpm, offset, piece, folder_name="Osu")


if __name__ == "__main__":
    for song_sumber in range(2,11):
        bpm,_,offset,piece,label_list = main(f"data/eval/song{song_sumber}/song{song_sumber}.osu")
        # image_part(song_sumber,bpm,offset,piece)
        label_list = filling_label(label_list)
        compression(song_sumber,label_list)
