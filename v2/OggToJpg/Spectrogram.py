import os
import cv2
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



def audio_to_spectrogram(audio, folder_data, sr=44100, n_fft=1024, hop_length=512, n_mels=128):
    """
    輸入 audio
    1. 計算 STFT，並存成 STFT 圖片
    2. 直接計算 Mel Spectrogram
    3. 回傳 Mel Spectrogram (dB)
    folder_data = [folder_path, song_name, number(第幾張)]

    回傳:
        mel_db: Mel spectrogram 的 dB 矩陣
    """
    # 1. audio -> numpy
    y = audiosegment_to_numpy(audio)

    # 2. STFT（用來存圖）
    D = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    log_S = librosa.amplitude_to_db(D, ref=np.max)

    # 3. 存 STFT 圖
    save_STFT_fast(log_S, sr, folder_data)

    # 4. 直接做 Mel Spectrogram
    mel_S = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels
    )
    mel_db = librosa.power_to_db(mel_S, ref=np.max)

    save_Mel_fast(mel_db, sr, folder_data)


def save_Mel_fast(mel_db, sr, folder_data):
    Mel_output_dir = f"{folder_data[0]}/Mel_Image/{folder_data[1]}"
    os.makedirs(Mel_output_dir, exist_ok=True)

    mel_norm = mel_db - mel_db.min()
    if mel_norm.max() > 0:
        mel_norm = mel_norm / mel_norm.max()
    mel_img = (mel_norm * 255).astype(np.uint8)

    mel_img = cv2.applyColorMap(mel_img, cv2.COLORMAP_JET)
    mel_img = cv2.resize(mel_img, (5, 400), interpolation=cv2.INTER_AREA)

    save_path = f'{Mel_output_dir}/{folder_data[1]}_{folder_data[2]}.jpg'
    cv2.imwrite(save_path, mel_img)


def save_STFT_fast(STFT_db, sr, folder_data):
    STFT_output_dir = f"{folder_data[0]}/STFT_Image/{folder_data[1]}"
    os.makedirs(STFT_output_dir, exist_ok=True)

    STFT_norm = STFT_db - STFT_db.min()
    if STFT_norm.max() > 0:
        STFT_norm = STFT_norm / STFT_norm.max()
    STFT_img = (STFT_norm * 255).astype(np.uint8)

    STFT_img = cv2.applyColorMap(STFT_img, cv2.COLORMAP_JET)
    STFT_img = cv2.resize(STFT_img, (5, 400), interpolation=cv2.INTER_AREA)

    save_path = f'{STFT_output_dir}/{folder_data[1]}_{folder_data[2]}.jpg'
    cv2.imwrite(save_path, STFT_img)



def save_STFT_spectrogram(log_S, sr, folder_data):
    STFT_output_dir = f"{folder_data[0]}/STFT_Image/{folder_data[1]}"
    os.makedirs(STFT_output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(5, 400), dpi=1)
    librosa.display.specshow(
        log_S,
        sr=sr,
        x_axis='time',
        y_axis='log',
        cmap='jet'
    )
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    canvas = FigureCanvas(fig)
    canvas.draw()

    # width, height = fig.canvas.get_width_height()
    # image_array = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8).reshape(height, width, 3)

    plt.savefig(f'{STFT_output_dir}/{folder_data[1]}_{folder_data[2]}.jpg', bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close(fig)

    # return image_array



def save_Mel_spectrogram(mel_db, sr, folder_data):
    Mel_output_dir = f"{folder_data[0]}/Mel_Image/{folder_data[1]}"
    os.makedirs(Mel_output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(5, 400), dpi=1)
    librosa.display.specshow(
        mel_db,
        sr=sr,
        x_axis='time',
        y_axis='mel',
        cmap='jet'
    )
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(f'{Mel_output_dir}/{folder_data[1]}_{folder_data[2]}.jpg', bbox_inches='tight', pad_inches=0, transparent=False)
    plt.close(fig)



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
    audio = AudioSegment.from_file("data/oni/song13/song13.ogg")
    a= audio_to_spectrogram(audio,"Spectrogram_test_jpg")
    print(type(a))#[255 0 0 128]
    