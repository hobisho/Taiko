from pydub import AudioSegment
import os

def split_audio(input_file, output_folder):
    # 讀取音檔
    audio = AudioSegment.from_file(input_file, format="mp3")
    print("hiiiiiiiiii")
    # 每0.5秒切割音檔
    chunk_length_ms = 500
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    # 確保輸出資料夾存在
    os.makedirs(output_folder, exist_ok=True)

    # 將切割後的音檔儲存到輸出資料夾，按順序編號
    for i, chunk in enumerate(chunks):
        output_file = os.path.join(output_folder, f"chunk_{i + 1}.wav")
        chunk.export(output_file, format="wav")


if __name__ == "__main__":
    input_file = "./song1.mp3"  # 輸入音檔路徑
    output_folder = "song1"      # 輸出資料夾路徑

    split_audio(input_file, output_folder)



