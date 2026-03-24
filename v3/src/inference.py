import os, sys, torch, numpy as np, cv2
import torch.nn.functional as F

sys.path.append(os.path.join(os.path.dirname(__file__), 'module'))
from module.decompression import decompression
from train import CNNFeatureExtractor, CNNTransformerModel

sys.path.append(os.path.join(os.path.dirname(__file__), '../label')) # 假設結構是 v2/src, v2/label
from label.tjaread_v3 import parse_tja_file #type:ignore
song_code = '5'  # 根據你的實際情況修改


# 定義圖片縮放函式（與 train.py 保持一致）
def resize_images(images, new_width, new_height):
    resized_list = []
    for img in images:
        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        resized_list.append(resized)
    return np.array(resized_list)

def to_binary(chart):
    # 0: 無敲擊, 1/2: 有敲擊
    return [int(x > 0) for x in chart]

def direct_comparison(x, y):
    return np.mean(np.array(x) == np.array(y))

def onset_comparison(human, ai, tolerance=1):
    human_bin = to_binary(human)
    ai_bin = to_binary(ai)
    hit_count = 0
    total_count = 0
    L = len(human_bin)
    for i in range(L):
        if human_bin[i] == 1:
            total_count += 1
            match = False
            for j in range(max(0, i-tolerance), min(L, i+tolerance+1)):
                if ai_bin[j] == 1:
                    match = True
                    break
            if match:
                hit_count += 1
    return hit_count / total_count if total_count > 0 else 0

# -------------------------------
# 1. 載入 checkpoint 與建立模型
# -------------------------------
# 取得目前程式檔案所在的目錄（如果在互動模式下執行，則可改用 os.getcwd()）
base_dir = os.path.dirname(os.path.abspath(__file__))
# 設定目標資料夾路徑：當前檔案所在目錄下的 "src/models"
models_dir = os.path.join(base_dir, "models")
checkpoint_path = os.path.join(models_dir, "20260318/checkpoint.pth")
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
print("target_H:", target_H)
print("target_W:", target_W)
num_classes = checkpoint["num_classes"]

# 建立模型並載入權重
model = CNNTransformerModel(embedding_dim=emabaedding_dim, num_heads=num_heads, num_layers=num_layers,
                              num_classes=num_classes, seq_length=seq_length)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()
print("模型載入完成。")

all_ochuman= 0
all_dcrand = 0
all_dchuman = 0
all_hipspace = 0
best = -1
best_ochuman = -1
best_dcrand = -1
best_dchuman = -1
best_song = None
error = []
for iii in range(1,11):
# -------------------------------
# 2. 從 tfrecords 讀取資料並前處理
# -------------------------------
# 使用 inferance.py 中的 decompression 讀取 tfrecords 資料
    tfrecords_filename = f"G://Osu_tfrecords/song{iii}.tfrecords"
    image_list, label_list = decompression(tfrecords_filename)
    image_array = np.array(image_list)
    print("原始圖片 shape:", image_array.shape)

    # 若原始圖片尺寸非 train 中設定的 target_H 與 target_W，則需縮放
    if image_array.shape[1] != target_H or image_array.shape[2] != target_W:
        #show image
        cv2.imshow("Original Image", image_array[0])  # 顯示第一張圖片
        image_array = resize_images(image_array, new_width=target_W, new_height=target_H)
        print("縮放後圖片 shape:", image_array.shape)

    # 檢查圖片 shape：期望形狀為 (seq_length, target_H, target_W, 3)
    if image_array.shape[0] != seq_length:
        raise ValueError(f"{iii}圖片數量 {image_array.shape[0]} 與預期的 seq_length {seq_length} 不符")

    # 增加 batch 維度：變成 (B, seq_length, target_H, target_W, 3)
    input_tensor = torch.FloatTensor(image_array).unsqueeze(0)

    # -------------------------------
    # 3. 進行推論
    # -------------------------------
    with torch.no_grad():
        probabilities = model(input_tensor)  # 輸出 shape: (B, seq_length, num_classes)
        # print("模型輸出:", outputs)
        # # one-hot 編碼轉換為類別
        # # predicted_labels = torch.argmax(F.softmax(outputs, dim=2), dim=2)
        # probabilities = F.softmax(outputs, dim=2)  # shape: (B, seq_length, num_classes)
        # print("機率:", probabilities)

        # 第三和第四的機率相加
        # combined = probabilities[:, :, 2] + probabilities[:, :, 3]

        # # 排除原第三與第四的機率
        # pre_combine = probabilities[:, :, :2]       # 取前兩個
        # post_combine = probabilities[:, :, 4:]      # 跳過第三、第四之後剩下的

        # # 新的機率陣列 (第三個位置為合併後機率)
        # new_probabilities = torch.cat([
        #     pre_combine,
        #     combined.unsqueeze(dim=2),
        #     post_combine
        # ], dim=2)

        # new_probabilities = torch.zeros_like(outputs)
        # new_probabilities.scatter_(-1, outputs.argmax(dim=-1, keepdim=True), 1)

    # print("推論完成。")
    # print("預測結果 shape:", predicted_labels.shape)
    # print("預測結果 (每張圖片的類別):")
    k=[]
    p=0
    evg = [0,0,0,0]

    for i in range(500):
        a = probabilities[0, i]
        a = a.tolist()
        for j in range(4):
            evg[j] += a[j]
    for j in range(4):
            evg[j] = evg[j]/500
    for i in range(probabilities.shape[1]):
        a = probabilities[0, i]
        a = a.tolist()
        if a[2] > evg[2]:
            print(1,end="")
            k.append(1)
            p=p+1
        elif a[3] > evg[3]:
            print(2,end="")
            p=p+1
            k.append(2)
        else:
            print(0,end="")
            k.append(0)
            p=p+1
        if ((i%48)==47):
            print(",")
    k.append(0)



    # 設定tja檔資料夾路徑
    bars = parse_tja_file(f"./data/oni/song{iii}")
    # print("原始譜面 (每小節16個字):")
    # for a in range(len(bars)):
    #     print(bars[a], end=",\n")

    # 展平成一維list（0/1/2）
    human_chart = [int(c) for bar in bars for c in bar]

    # 你的 k 是AI生成的譜面
    ai_chart = k  # 你的 AI output (0/1/2 list)
    # 讓兩個長度一樣，避免IndexError
    min_len = min(len(human_chart), len(ai_chart))
    human_chart = human_chart[:min_len]
    ai_chart = ai_chart[:min_len]

    def hipspace_comparison(ai_chart_binary, human_chart_binary):
        # 根據論文定義，使用包含 8 個時間點的滑動視窗來衡量模式 [1]
        window_size = 8
        
        # 如果譜面長度不足以形成一個完整的模式，則回傳 0
        if len(human_chart_binary) < window_size:
            return 0.0
            
        # 使用集合 (set) 來過濾並儲存獨特的排列模式
        ai_patterns = set()
        human_patterns = set()
        
        # 擷取 AI 譜面中所有出現過的獨特模式
        for i in range(len(ai_chart_binary) - window_size + 1):
            ai_patterns.add(tuple(ai_chart_binary[i : i + window_size]))
            
        # 擷取人類譜面中所有出現過的獨特模式
        for i in range(len(human_chart_binary) - window_size + 1):
            human_patterns.add(tuple(human_chart_binary[i : i + window_size]))
            
        # 避免除以零的錯誤
        if len(human_patterns) == 0:
            return 0.0
            
        # 取得模型與人類的模式交集 [1]
        intersection = ai_patterns.intersection(human_patterns)
        
        # 計算 HI P-Space 分數：將交集大小與人類總模式數量進行對比 [1]
        score = len(intersection) / len(human_patterns)
        
        return score

    # 指標計算
    np.random.seed(5)
    random_chart = np.random.choice([0, 1, 2], size=len(ai_chart))
    dcrand = direct_comparison(to_binary(ai_chart), to_binary(random_chart))
    dchuman = direct_comparison(to_binary(ai_chart), to_binary(human_chart))
    ochuman = onset_comparison(human_chart, ai_chart, tolerance=1)
    hipspace = hipspace_comparison(to_binary(ai_chart), to_binary(human_chart))
    if dchuman > best_ochuman:
        best = iii
        best_ochuman = dchuman
        best_dcrand = dcrand
        best_dchuman = dchuman
        best_song = iii

    all_dcrand = all_dcrand + dcrand
    all_dchuman = all_dchuman + dchuman
    all_ochuman = all_ochuman + ochuman
    all_hipspace = all_hipspace + hipspace

    print(f"DCRand  (與亂數一致率)      : {dcrand:.4f}")
    print(f"DCHuman (與人類準確率)      : {dchuman:.4f}")
    print(f"OCHuman (寬容onset準確率)   : {ochuman:.4f}")
    print(f"HI P-Space (模式相似度)     : {hipspace:.4f}")

    evg_dcrand = all_dcrand / (10-len(error))
    evg_dchuman = all_dchuman / (10-len(error))
    evg_ochuman = all_ochuman / (10-len(error))
    evg_hipspace = all_hipspace / (10-len(error))

print(f"平均 DCRand  (與亂數一致率)      : {evg_dcrand:.4f}")
print(f"平均 DCHuman (與人類準確率)      : {evg_dchuman:.4f}")
print(f"平均 OCHuman (寬容onset準確率)   : {evg_ochuman:.4f}")
print(f"平均 HI P-Space (模式相似度)     : {evg_hipspace:.4f}")
print(f"最佳歌曲編號                    : {best_song}")
print(f"最佳 DCRand  (與亂數一致率)      : {best_dcrand:.4f}")
print(f"最佳 DCHuman (與人類準確率)      : {best_dchuman:.4f}")
print(f"最佳 OCHuman (寬容onset準確率)   : {best_ochuman:.4f}")
print(f"錯誤歌曲編號: {error}")