from pydub import AudioSegment
import os 
from tqdm import tqdm
import sys
from split_song.readdata import TjaData 
from split_song.song_sec import count_sec # type: ignore
# sys.path.append(r"v2/OggToJpg")
from OggToJpg.Spectrogram import audio_to_spectrogram # type: ignore


def process_audio(input_audio, folder_path)->list:
    ogg_file_path = None
    tja_data=TjaData(input_audio)
    offset = tja_data.Offset() *1000
    
    # 確保輸出資料夾存在
    for file in os.listdir(input_audio):
        if file.endswith(".ogg"):
            file_name = os.path.splitext(file)[0]
            ogg_file_path = os.path.join(input_audio, file)
            break
    
    
    # print(f"============================================ spliting {file_name} ============================================\n")
    os.makedirs(f"{folder_path}/Split_ogg/{file_name}", exist_ok=True)
    
    # 載入音檔
    audio = AudioSegment.from_file(ogg_file_path)
    # 去除 offset
    # trimmed_audio = audio[offset:]
    start = offset
    time_per_footage = count_sec(tja_data.Bpm(),duration=len(audio),take_off=offset, piece=tja_data.Piece())
    # print(tja_data.Bpm(),len(audio),offset, tja_data.Piece())

    overlapping_time = round(time_per_footage[0] * 0.075, 3) * 1000
    for i in tqdm(range(len(time_per_footage))): 
        end = start + time_per_footage[i]*1000  # 轉換為毫秒
        split_audio = audio[start - overlapping_time:end + overlapping_time]
        
        # 儲存片段
        output_path = os.path.join(f"{folder_path}/Split_ogg/{file_name}", f"{file_name}_{i+1}.ogg")
        split_audio.export(output_path, format="ogg")

        start = end
        audio_to_spectrogram(split_audio, [folder_path, file_name, i+1])
    print("split end")
    # return image

# 測試用範例
if __name__ == "__main__":
    input_audio = "v2/data/oni/song13"  # 你的音檔
    folder_path = "data"
    process_audio(input_audio, folder_path)
    
