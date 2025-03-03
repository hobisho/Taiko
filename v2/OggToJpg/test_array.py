import cv2
import numpy as np
from PIL import Image

def image_to_matrix(image_path, grayscale=False):
    # 讀取圖片
    image = Image.open(image_path)

    # 轉換為灰階（如果需要）
    if grayscale:
        image = image.convert("L")  # 轉換為灰階模式（L）

    # 轉換為 NumPy 陣列
    image_matrix = np.array(image)

    return image_matrix

# 測試用
if __name__ == "__main__":
    image_path = "spectrogram.png"  # 請確保有這張圖片
    matrix = image_to_matrix(image_path)  # 轉換為灰階
    print("圖片矩陣形狀:", matrix.shape)
    print(matrix)  # 顯示部分像素值
