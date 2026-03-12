import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def audiosegment_to_numpy(audio_segment):
    # 取得音訊的聲道數、取樣寬度、幀數
    samples = np.array(audio_segment.get_array_of_samples())

    # 如果是立體聲（雙聲道），則需 reshape 為 (2, N) 並取平均轉單聲道
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)  # 轉換為單聲道

    # 標準化到 [-1, 1] 範圍
    samples = samples.astype(np.float32) / (2 ** (8 * audio_segment.sample_width - 1))

    return samples


def audio_to_spectrogram(audio,name="A")->list:
    
    # 1. 讀取音訊並計算 Spectrogram
    y = audiosegment_to_numpy(audio)
    sr = 44100

    # 2.傅立葉轉換
    D = np.abs(librosa.stft(y))  # 計算短時傅立葉變換 (STFT)
    log_S = librosa.amplitude_to_db(D, ref=np.max)  # 轉換為 dB Scale

    # 3. 建立 Matplotlib Figure
    fig, ax = plt.subplots(figsize=(6, 4))  # 設定大小
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='log', cmap='jet')
    ax.axis('off')  # 隱藏軸線
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # 去除邊框

    # 4. 轉換成 RGB 陣列
    canvas = FigureCanvas(fig)
    canvas.draw()

    # 5. 提取 NumPy 陣列
    width, height = fig.canvas.get_width_height()
    np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8).reshape(height, width, 3)
    # image_array = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8).reshape(height, width, 3)

    plt.savefig(f'{name}.jpg', bbox_inches='tight', pad_inches=0,transparent=False)
    # plt.show()
    plt.close(fig)  # 關閉圖表，釋放記憶體
    # image_rgb = image_array.convert("RGB")# 移除透明通道
    return
    # return image_array.tolist()

# 使用示例
if __name__ == "__main__":
    # # read entire folder
    # song_name = "song1"
    # folder_path = f"v2/data/split_ogg/{song_name}"
    # output_dir = f"v2/data/zip_testing_data/{song_name}"
    # os.makedirs(output_dir, exist_ok=True)
    # for filename in os.listdir(folder_path):
    #     file_path = os.path.join(folder_path, filename)
        
    #     # 讀取音檔
    #     audio = AudioSegment.from_file(file_path)
        
    #     # 移除副檔名，作為 spectrogram 的名稱
    #     name = os.path.splitext(filename)[0]
        
    #     # 轉換成 Spectrogram
    #     audio_to_spectrogram(audio, output_dir+"/"+name)  # 假設這個函式已經定義

    # read one file
    audio = AudioSegment.from_file("v2/data/oni/song13/song13.ogg")
    a= audio_to_spectrogram(audio,"Spectrogram_test_jpg")
    print(type(a))#[255 0 0 128]
    