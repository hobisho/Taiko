import os, sys, torch, numpy as np, cv2
import torch.nn.functional as F

sys.path.append(os.path.join(os.path.dirname(__file__), 'module'))
from module.decompression import decompression
from train import CNNFeatureExtractor, CNNTransformerModel

# 定義圖片縮放函式（與 train.py 保持一致）
def resize_images(images, new_width, new_height):
    resized_list = []
    for img in images:
        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        resized_list.append(resized)
    return np.array(resized_list)

# -------------------------------
# 1. 載入 checkpoint 與建立模型
# -------------------------------
# 取得目前程式檔案所在的目錄（如果在互動模式下執行，則可改用 os.getcwd()）
base_dir = os.path.dirname(os.path.abspath(__file__))
# 設定目標資料夾路徑：當前檔案所在目錄下的 "src/models"
models_dir = os.path.join(base_dir, "models")
checkpoint_path = os.path.join(models_dir, "checkpoint_best_0319.pth")
if not os.path.exists(checkpoint_path):
    raise FileNotFoundError(f"Checkpoint not found at {checkpoint_path}")

# 假設在 CPU 上進行推論，如需使用 GPU，可將 map_location 改為 torch.device('cuda')
checkpoint = torch.load(checkpoint_path, map_location=torch.device('cuda'))

# 從 checkpoint 中讀取必要參數
emabaedding_dim = checkpoint["embedding_dim"]
num_heads = checkpoint["num_heads"]
num_layers = checkpoint["num_layers"]
seq_length = checkpoint["seq_length"]
target_H = checkpoint["target_H"]
target_W = checkpoint["target_W"]
num_classes = checkpoint["num_classes"]

# 建立模型並載入權重
model = CNNTransformerModel(embedding_dim=emabaedding_dim, num_heads=num_heads, num_layers=num_layers,
                              num_classes=num_classes, seq_length=seq_length)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()
print("模型載入完成。")

# -------------------------------
# 2. 從 tfrecords 讀取資料並前處理
# -------------------------------
# 使用 inferance.py 中的 decompression 讀取 tfrecords 資料
tfrecords_filename = 'E://tfrecords/song1.tfrecords'
image_list, label_list = decompression(tfrecords_filename)
image_array = np.array(image_list)
print("原始圖片 shape:", image_array.shape)

# 若原始圖片尺寸非 train 中設定的 target_H 與 target_W，則需縮放
if image_array.shape[1] != target_H or image_array.shape[2] != target_W:
    image_array = resize_images(image_array, new_width=target_W, new_height=target_H)
    print("縮放後圖片 shape:", image_array.shape)

# 檢查圖片 shape：期望形狀為 (seq_length, target_H, target_W, 3)
if image_array.shape[0] != seq_length:
    raise ValueError(f"圖片數量 {image_array.shape[0]} 與預期的 seq_length {seq_length} 不符")

# 增加 batch 維度：變成 (B, seq_length, target_H, target_W, 3)
input_tensor = torch.FloatTensor(image_array).unsqueeze(0)

# -------------------------------
# 3. 進行推論
# -------------------------------
with torch.no_grad():
    outputs = model(input_tensor)  # 輸出 shape: (B, seq_length, num_classes)
    print("模型輸出:", outputs)
    # one-hot 編碼轉換為類別
    # predicted_labels = torch.argmax(F.softmax(outputs, dim=2), dim=2)
    probabilities = F.softmax(outputs, dim=2)  # shape: (B, seq_length, num_classes)

    # 第三和第四的機率相加
    combined = probabilities[:, :, 2] + probabilities[:, :, 3]

    # 排除原第三與第四的機率
    pre_combine = probabilities[:, :, :2]       # 取前兩個
    post_combine = probabilities[:, :, 4:]      # 跳過第三、第四之後剩下的

    # 新的機率陣列 (第三個位置為合併後機率)
    new_probabilities = torch.cat([
        pre_combine,
        combined.unsqueeze(dim=2),
        post_combine
    ], dim=2)

    new_probabilities = torch.zeros_like(outputs)
    new_probabilities.scatter_(-1, outputs.argmax(dim=-1, keepdim=True), 1)

# print("推論完成。")
# print("預測結果 shape:", predicted_labels.shape)
print("預測結果 (每張圖片的類別):")
for i in range(300):
    print(new_probabilities[0, i])
# # print(predicted_labels)
