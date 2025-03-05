# from compression.compression_file import CompressionFile
from label.tjaread import parse_tja_file #type:ignore
from split_song.splitv2 import process_audio

def labal_part(song_number):
    parse_tja_file("v2/data/level 6~7/song{song_number}")
    

def image_part(song_sumber):
    input_audio = f"v2/data/level 6~7/song{song_sumber}"  # 你的音檔
    song_output_folder = "v2/data/split_ogg"  # 儲存資料夾
    jpg_output_folder = f"v2/data/zip_testing_data"
    image_array = process_audio(input_audio, song_output_folder,jpg_output_folder)
    print(image_array)

if __name__ == "__main__":
    image_part(2)