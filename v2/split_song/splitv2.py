from pydub import AudioSegment
import os 
from tqdm import tqdm
# from Spectrogram import audio_to_spectrogram # type: ignore
from readdata import TjaData # type: ignore
from song_sec import count_sec # type: ignore


def process_audio(input_file, output_folder):
            
    ogg_file_path = None
    tja_data=TjaData(input_file)
    offset = tja_data.Offset() *1000
    
    # 確保輸出資料夾存在
    for file in os.listdir(input_file):
        if file.endswith(".ogg"):
            file_name = os.path.splitext(file)[0]
            ogg_file_path = os.path.join(input_file, file)
            break
    print(f"============================================ spliting {file_name} ============================================\n")
    os.makedirs(f"{output_dir}/{file_name}", exist_ok=True)
    
    # 載入音檔
    audio = AudioSegment.from_file(ogg_file_path)
    # 去除 offset
    trimmed_audio = audio[offset:]
    start = offset
    piece = tja_data.Piece()
    time_per_footage = count_sec(tja_data.Bpm(),duration=len(audio),take_off=offset, piece=piece)
    
    for i in tqdm(range(len(time_per_footage))):
        end = start + time_per_footage[i]*1000
        # print(end,start)
        split_audio = trimmed_audio[start:end]
        # 儲存片段
        output_path = os.path.join(f"{output_dir}/{file_name}", f"{file_name}_{i+1}.ogg")
        split_audio.export(output_path, format="ogg")
        # # print(f"儲存片段 {i+1}: {output_path}")
        start = end
        # audio_to_spectrogram(split_audio)
        return split_audio

# 測試用範例
if __name__ == "__main__":
    input_audio = "level 6~7/3_song"  # 你的音檔
    output_dir = "split_ogg"  # 儲存資料夾
    process_audio(input_audio, output_dir)
    
