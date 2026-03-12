import os
import numpy as np
from PIL import Image
import librosa
import librosa.display
import matplotlib.pyplot as plt


def image_to_spectrogram_array(img, normalize=True):
    """
    將輸入圖片轉成 2D 頻譜矩陣
    支援:
        - numpy array
        - PIL Image
        - 圖片路徑字串

    回傳:
        spec: shape = (freq_bins, time_frames)
    """
    if isinstance(img, str):
        img = Image.open(img)

    if isinstance(img, Image.Image):
        img = np.array(img)

    # 若是 RGB / RGBA，轉灰階
    if img.ndim == 3:
        img = img[..., :3]
        img = np.mean(img, axis=2)

    spec = img.astype(np.float32)

    if normalize:
        spec_min = spec.min()
        spec_max = spec.max()
        if spec_max > spec_min:
            spec = (spec - spec_min) / (spec_max - spec_min)

    return spec


def apply_mel_filterbank_to_spectrogram_image(
    spec_img,
    sr=44100,
    n_fft=None,
    n_mels=128,
    fmin=0,
    fmax=None,
    power_to_db=True
):
    """
    將一張 spectrogram 圖片視為 linear spectrogram，
    套用 Mel filter bank 後得到 mel spectrogram。

    參數:
        spec_img: 圖片 / numpy array / 圖片路徑
        sr: 採樣率
        n_fft: 對應 STFT 的 n_fft，若為 None，會根據頻率 bin 數反推
        n_mels: mel bins 數量
        fmin, fmax: mel filter 範圍
        power_to_db: 是否轉 dB

    回傳:
        mel_spec: shape = (n_mels, time_frames)
    """
    spec = image_to_spectrogram_array(spec_img, normalize=True)

    # 假設輸入圖的 shape = (freq_bins, time_frames)
    freq_bins, time_frames = spec.shape

    # 如果不知道 n_fft，可由 freq_bins 反推：
    # STFT spectrogram 的頻率維度通常是 (n_fft // 2 + 1)
    if n_fft is None:
        n_fft = (freq_bins - 1) * 2

    # 建立 mel filter bank
    mel_filter = librosa.filters.mel(
        sr=sr,
        n_fft=n_fft,
        n_mels=n_mels,
        fmin=fmin,
        fmax=fmax
    )  # shape = (n_mels, freq_bins)

    # 若 freq_bins 和 mel_filter 的第二維不一致，做裁切或補齊
    mel_freq_bins = mel_filter.shape[1]

    if freq_bins > mel_freq_bins:
        spec = spec[:mel_freq_bins, :]
    elif freq_bins < mel_freq_bins:
        pad_rows = mel_freq_bins - freq_bins
        spec = np.pad(spec, ((0, pad_rows), (0, 0)), mode='constant')

    # 套用 mel filter bank
    mel_spec = np.dot(mel_filter, spec)

    # 避免 log 時出現 0
    mel_spec = np.maximum(mel_spec, 1e-10)

    if power_to_db:
        mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

    return mel_spec


def save_mel_spectrogram_image(
    mel_spec,
    save_path,
    sr=22050,
    hop_length=512,
    cmap='magma',
    show_axis=False,
    dpi=100
):
    """
    將 mel spectrogram 矩陣存成圖片
    """
    plt.figure(figsize=(4, 4))

    librosa.display.specshow(
        mel_spec,
        sr=sr,
        hop_length=hop_length,
        x_axis='time' if show_axis else None,
        y_axis='mel' if show_axis else None,
        cmap=cmap
    )

    if not show_axis:
        plt.axis('off')

    plt.tight_layout(pad=0)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()


def spectrogram_image_list_to_mel_image_list(
    spectrogram_img_list,
    output_dir,
    sr=44100,
    n_fft=None,
    n_mels=128,
    fmin=0,
    fmax=None,
    hop_length=512,
    cmap='magma',
    show_axis=False,
    dpi=100,
    prefix='mel'
):
    """
    輸入一首歌的 spectrogram 圖片 list
    輸出 mel spectrogram 圖片 list

    參數:
        spectrogram_img_list: list
            每個元素可以是:
            - 圖片路徑
            - numpy array
            - PIL image
        output_dir: 輸出資料夾

    回傳:
        output_paths: mel 圖片路徑 list
    """
    os.makedirs(output_dir, exist_ok=True)
    output_paths = []

    for i, spec_img in enumerate(spectrogram_img_list):
        mel_spec = apply_mel_filterbank_to_spectrogram_image(
            spec_img=spec_img,
            sr=sr,
            n_fft=n_fft,
            n_mels=n_mels,
            fmin=fmin,
            fmax=fmax,
            power_to_db=True
        )

        save_path = os.path.join(output_dir, f"{prefix}_{i:04d}.png")

        save_mel_spectrogram_image(
            mel_spec=mel_spec,
            save_path=save_path,
            sr=sr,
            hop_length=hop_length,
            cmap=cmap,
            show_axis=show_axis,
            dpi=dpi
        )

        output_paths.append(save_path)

    return output_paths