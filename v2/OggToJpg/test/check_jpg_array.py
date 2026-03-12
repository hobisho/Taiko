from PIL import Image
import numpy as np

# 讀取圖片
image = Image.open("m.png")  # 替換成你的圖片路徑

# 轉換為 NumPy 陣列
image_array = np.array(image)

# 顯示陣列形狀
print(image_array)  # (高度, 寬度, 色彩通道)
