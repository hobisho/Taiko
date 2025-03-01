from pydub import AudioSegment
import os
from readdata import TjaData

def process_audio(input_file, output_folder, segments):
    
    # 確保輸出資料夾存在
    ogg_file_path = None
    ja_data=TjaData(input_file)
    for file in os.listdir(input_file):
        if file.endswith(".ogg"):
            ogg_file_path = os.path.join(input_file, file)
            break
    os.makedirs(output_folder, exist_ok=True)
    
    # 載入音檔
    audio = AudioSegment.from_file(ogg_file_path)
    
    # 去除 offset
    trimmed_audio = audio[ja_data.Offset():]
    print(ja_data.Offset())
    
    for i, (start, end) in enumerate(segments):
        start_ms = start *1000
        end_ms = end *1000
        segment_audio = trimmed_audio[start_ms:end_ms]
        
        output_path = os.path.join(output_folder, f"segment_{i+1}.wav")
        segment_audio.export(output_path, format="wav")
        print(f"儲存片段 {i+1}: {output_path}")

# 測試用範例
if __name__ == "__main__":
    input_audio = "level 6~7/02. TT -Japanese ver.-"  # 你的音檔
    output_dir = "hi"  # 儲存資料夾
    split_segments = [(0, 5), (5, 10), (10, 15)]  # 以秒為單位的切割範圍
    
    process_audio(input_audio, output_dir, split_segments)
