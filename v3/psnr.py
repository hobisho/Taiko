import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

img1 = cv2.imread(r"data\Mel_Image\song1\song1_1.png")

if img1 is None:
    raise ValueError("圖片讀取失敗，請檢查路徑")

re_img2 = cv2.resize(img1, (3,400))
re_img2 = cv2.resize(re_img2, (60,400))

# 灰階
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(re_img2, cv2.COLOR_BGR2GRAY)

# MSE
mse = np.mean((gray1.astype(np.float64) - gray2.astype(np.float64)) ** 2)

# PSNR
psnr = cv2.PSNR(img1, re_img2)

# SSIM
score, diff = ssim(gray1, gray2, full=True)

print("re_img2 shape:", re_img2.shape)

print("MSE:", mse)
print("PSNR:", psnr)
print("SSIM:", score)