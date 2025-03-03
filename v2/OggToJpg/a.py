import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from array_zip import comprassion  # type: ignore

def audiosegment_to_numpy(audio_segment):
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)
    samples = samples.astype(np.float32) / (2 ** (8 * audio_segment.sample_width - 1))
    return samples

def audio_to_spectrogram_array(audio):
    y = audiosegment_to_numpy(audio)
    sr = 48000
    
    # 計算梅爾頻譜
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    S_db = librosa.power_to_db(S, ref=np.max)
    
    # 轉換頻譜圖為 NumPy 陣列
    fig, ax = plt.subplots(figsize=(1, 1),dpi = 100)
    librosa.display.specshow(S_db, sr=sr, ax=ax)
    fig.canvas.draw()
    plt.axis("off")
    plt.margins(0,0)
    plt.tight_layout()
    
    # # 擷取圖像的像素數據作為矩陣輸出
    return S_db

# 使用示例
if __name__ == "__main__":
    audio = AudioSegment.from_file("level 6~7/DLC 22. Koisuru Fortune Cookie/Koisuru Fortune Cookie.ogg")
    spectrogram_image = audio_to_spectrogram_array(audio)
    plt.matshow(spectrogram_image, cmap='viridis')

    # 去除坐标轴
    plt.axis('off')

    # 保存为图片
    plt.savefig('matrix_image.png', bbox_inches='tight', pad_inches=0)

    # 显示图像
    plt.show()