import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from array_zip import comprassion # type: ignore

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
    # # 讀取音訊
    # audio = AudioSegment.from_file(audio_path)
    # 去除 offset
    y = audiosegment_to_numpy(audio)
    sr =48000

    # 轉換為梅爾頻譜
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    S_db = librosa.power_to_db(S, ref=np.max)
    
    # 繪製頻譜圖
    plt.figure(figsize=(1, 1),dpi=100)
    plt.axis("off")
    plt.margins(0,0)
    librosa.display.specshow(S_db, y_axis="log")
    plt.tight_layout()

    # 儲存圖片
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0)
    fig.canvas.draw()
    
    # 擷取圖像的像素數據作為矩陣輸出
    spectrogram_image = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close(fig)
    # plt.show()
    return spectrogram_image

# 使用示例
if __name__ == "__main__":
    audio = AudioSegment.from_file("level 6~7/DLC 22. Koisuru Fortune Cookie/Koisuru Fortune Cookie.ogg")
    print(audio_to_spectrogram(audio))