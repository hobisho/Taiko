import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# 1. 讀取音訊並計算 Spectrogram
y, sr = librosa.load('hi/TT -Japanese ver.-_15_7.ogg')  # 讀取音檔
D = np.abs(librosa.stft(y))  # 計算短時傅立葉變換 (STFT)
log_S = librosa.amplitude_to_db(D, ref=np.max)  # 轉換為 dB Scale

# 2. 建立 Matplotlib Figure
fig, ax = plt.subplots(figsize=(6, 4))  # 設定大小
librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='log', cmap='jet')
ax.axis('off')  # 隱藏軸線
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # 去除邊框

# 3. 轉換成 RGB 陣列
canvas = FigureCanvas(fig)
canvas.draw()

# 4. 提取 NumPy 陣列
width, height = fig.canvas.get_width_height()
image_array = np.frombuffer(canvas.tostring_argb(), dtype=np.uint8).reshape(height, width, 4)

plt.savefig('m.png', bbox_inches='tight', pad_inches=0)
plt.show()
plt.close(fig)  # 關閉圖表，釋放記憶體

# 檢查結果

print(image_array)  # (高度, 寬度, 3) -> RGB 格式
