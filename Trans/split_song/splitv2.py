from pydub import AudioSegment
import os 
from tqdm import tqdm
from split_song.readdata import TjaData 
from split_song.song_sec import count_sec # type: ignore
from split_song.Spectrogram import audio_to_spectrogram # type: ignore
from split_song.trans import main


def process_audio(input_file, song_output_folder,jpg_output_folder)->list:
    ogg_file_path = None
    
    # 確保輸入資料夾存在
    for file in os.listdir(input_file):
        if file.endswith(".mp3"):
            file_name = os.path.splitext(file)[0]
            ogg_file_path = os.path.join(input_file, file)
            break

    print(file_name)

    bpm,tick,offset,piece,hit = main(f"{input_file}/{file_name}.osu")
    
    # print(f"============================================ spliting {file_name} ============================================\n")
    os.makedirs(f"{song_output_folder}/{file_name}", exist_ok=True)
    
    # 載入音檔
    audio = AudioSegment.from_file(ogg_file_path)
    # 去除 offset
    # trimmed_audio = audio[offset:]
    start = offset
    time_per_footage = count_sec(bpm,duration=len(audio),take_off=offset, piece=piece)
    # print(tja_data.Bpm(),len(audio),offset, tja_data.Piece())
    print(time_per_footage)
    
    jpg_output_dir = f"{jpg_output_folder}/{file_name}"
    os.makedirs(jpg_output_dir, exist_ok=True)
    for i in tqdm(range(len(time_per_footage))):
        end = start + time_per_footage[i]*1000
        # print(end,start)
        split_audio = audio[start:end]
        # print(end)
        
        # 儲存片段
        output_path = os.path.join(f"{song_output_folder}/{file_name}", f"{file_name}_{i+1}.ogg")
        split_audio.export(output_path, format="ogg")

        start = end
        audio_to_spectrogram(split_audio,f"{jpg_output_dir}/{file_name}_{i+1}")
    print("split end")
    # return image

# 測試用範例
if __name__ == "__main__":
    for i in range(1, 11):
        input_audio = f".\eval\song{i}"
    # input_audio = ".\eval\song2"  # 你的音檔
        song_output_folder = "Trans/data/split_ogg"  # 儲存資料夾
        jpg_output_folder = f"Trans/data/zip_testing_data"
        process_audio(input_audio, song_output_folder,jpg_output_folder)
    
