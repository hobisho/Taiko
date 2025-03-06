import cv2
import numpy as np

def create_black_image(width, height, filename="v2/data/white_image.png"):
    # 創建全黑影像 (RGB 格式)
    black_image = np.ones((height, width, 3), dtype=np.uint8)*255
    
    # 儲存影像 (確保為 RGB 格式)
    black_image = cv2.cvtColor(black_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(filename, black_image)
    print(f"已儲存全黑影像: {filename} ({width}x{height})")

if __name__ == "__main__":
    width = 600
    height = 400
    create_black_image(width, height)
