import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

def audio_to_spectrogram(audio_path, save_path="spectrogram.png"):
    # 設定圖像大小
    plt.figure(dpi=100) 
    
    # 讀取音訊
    y, sr = librosa.load(audio_path, sr=None)

    # 轉換為梅爾頻譜
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    S_db = librosa.power_to_db(S, ref=np.max)
    

    # 繪製頻譜圖
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="mel")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Mel Spectrogram")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.tight_layout()

    # 儲存圖片
    plt.savefig(save_path)
    plt.show()

# 使用示例
audio_to_spectrogram("level 6~7/02. TT -Japanese ver.-/TT -Japanese ver.-.ogg")