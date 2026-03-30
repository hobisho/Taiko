import cv2
import numpy as np

def create_black_image(width, height, filename="v2/data/white_image.jpg"):
    # 創建全黑影像 (RGB 格式)
    black_image = np.ones((height, width, 3), dtype=np.uint8)*255
    
    # 儲存影像 (確保為 RGB 格式)
    black_image = cv2.cvtColor(black_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(filename, black_image)
    print(f"已儲存全白影像: {filename} ({width}x{height})")

def create_blue_image(width, height, filename="v2/data/nosong.jpg"):
    # 建立全藍影像 (BGR 格式)
    blue_image = np.zeros((height, width, 3), dtype=np.uint8)
    blue_image[:, :] = (255, 0, 0)  # B=255, G=0, R=0

    # 儲存影像
    cv2.imwrite(filename, blue_image)

    print(f"已儲存全藍影像: {filename} ({width}x{height})")


if __name__ == "__main__":
    width = 60
    height = 128
    create_black_image(width, height)
    create_blue_image(width, height)
