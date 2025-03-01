from pydub import AudioSegment
import os
from readdata import TjaData
from song_sec import count_sec

def process_audio(input_file, output_folder, piece):
    #設定
    ogg_file_path = None
    ja_data=TjaData(input_file)
    offset = ja_data.Offset() *1000
    
    # 確保輸出資料夾存在
    for file in os.listdir(input_file):
        if file.endswith(".ogg"):
            file_name = os.path.splitext(file)[0]
            ogg_file_path = os.path.join(input_file, file)
            break
    
    os.makedirs(output_folder, exist_ok=True)
    
    # 載入音檔
    audio = AudioSegment.from_file(ogg_file_path)
    # 去除 offset
    trimmed_audio = audio[offset:]
    start = offset
    time_per_footage = count_sec(ja_data.Bpm(),duration=len(audio),take_off=offset,piece=piece)
    print(offset)
    print(len(audio))
    print(len(time_per_footage))
    
    # for i in range(piece):
    #     end = start + time_per_footage[i]
    #     print(end,start)
        # split_audio = trimmed_audio[start:end]
        # # 儲存片段
        # output_path = os.path.join(output_folder, f"{file_name}_{i+1}_{ja_data.Level()}.ogg")
        # split_audio.export(output_path, format="ogg")
        # print(f"儲存片段 {i+1}: {output_path}")
        # start = end

# 測試用範例
if __name__ == "__main__":
    input_audio = "level 6~7/02. TT -Japanese ver.-"  # 你的音檔
    output_dir = "hi"  # 儲存資料夾
    piece = 10
    process_audio(input_audio, output_dir, piece)
