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


def audio_to_spectrogram(audio, save_path="spectrogram.png"):
    
    # 1. 讀取音訊並計算 Spectrogram
    y = audiosegment_to_numpy(audio)
    sr = 48000

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
    image_array = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8).reshape(height, width, 4)

    plt.savefig('m.png', bbox_inches='tight', pad_inches=0)
    # plt.show()
    plt.close(fig)  # 關閉圖表，釋放記憶體
    return image_array

# 使用示例
if __name__ == "__main__":
    audio = AudioSegment.from_file("level 6~7/DLC 22. Koisuru Fortune Cookie/Koisuru Fortune Cookie.ogg")
    print(audio_to_spectrogram(audio))