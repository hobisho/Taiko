import cv2
import numpy as np
import os, sys
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), 'module'))
from module.decompression import decompression

# 設定 CUDA 裝置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("使用裝置:", device)

# -------------------------------
# 模型定義 (CNN + Transformer)
# -------------------------------
class CNNFeatureExtractor(nn.Module):
    def __init__(self, embedding_dim):
        super(CNNFeatureExtractor, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool = nn.AdaptiveAvgPool2d((1,1))
        self.fc = nn.Linear(128, embedding_dim)
        
    def forward(self, x):
        # x: (B, 3, H, W)
        x = F.relu(self.bn1(self.conv1(x)))  # (B, 32, H/2, W/2)
        x = F.relu(self.bn2(self.conv2(x)))  # (B, 64, H/4, W/4)
        x = F.relu(self.bn3(self.conv3(x)))  # (B, 128, H/8, W/8)
        x = self.pool(x)                     # (B, 128, 1, 1)
        x = x.view(x.size(0), -1)            # (B, 128)
        x = self.fc(x)                       # (B, embedding_dim)
        return x

class CNNTransformerModel(nn.Module):
    def __init__(self, embedding_dim=256, num_heads=8, num_layers=4, num_classes=10, seq_length=1503):
        """
        embedding_dim : CNN 輸出與 Transformer 的特徵維度
        num_heads     : Transformer 的多頭注意力數量
        num_layers    : Transformer Encoder 的層數
        num_classes   : 輸出層維度（例如分類類別數）
        seq_length    : 每筆資料中的圖片數（本例為1503）
        """
        super(CNNTransformerModel, self).__init__()
        self.seq_length = seq_length
        self.embedding_dim = embedding_dim
        self.cnn_extractor = CNNFeatureExtractor(embedding_dim)
        # 可學習的位置嵌入
        self.pos_embedding = nn.Parameter(torch.randn(1, seq_length, embedding_dim))
        # 定義 Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(d_model=embedding_dim, nhead=num_heads)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        # 輸出層，對每張圖片產生預測（例如分類結果）
        self.fc_out = nn.Linear(embedding_dim, num_classes)
        
    def forward(self, x):
        # x: (B, seq_length, H, W, C)
        B, L, H, W, C = x.size()
        assert L == self.seq_length, f"輸入圖片數 {L} 必須等於預設的 seq_length {self.seq_length}"
        
        # 調整維度：變成 (B, L, C, H, W)
        x = x.permute(0, 1, 4, 2, 3)
        # 合併 B 與 L，變成 (B*L, C, H, W)
        x = x.reshape(B * L, C, H, W)
        # CNN 特徵提取 (B*L, embedding_dim)
        features = self.cnn_extractor(x)
        # 還原成 (B, L, embedding_dim)
        features = features.view(B, L, self.embedding_dim)
        # 加入位置嵌入
        features = features + self.pos_embedding[:, :L, :]
        # Transformer 輸入需要 shape 為 (L, B, embedding_dim)
        features = features.permute(1, 0, 2)
        trans_out = self.transformer(features)
        trans_out = trans_out.permute(1, 0, 2)  # 還原成 (B, L, embedding_dim)
        # 每張圖片對應一個預測
        logits = self.fc_out(trans_out)  # (B, L, num_classes)
        return logits

# -------------------------------
# OpenCV: 定義圖片縮放函式
# -------------------------------
def resize_images(images, new_width, new_height):
    """
    將輸入的圖片集調整為新的寬與高
    :param images: numpy 陣列，形狀 (seq_length, H, W, 3)
    :param new_width: 新的寬度（像素）
    :param new_height: 新的高度（像素）
    :return: 調整後的圖片集，形狀 (seq_length, new_height, new_width, 3)
    """
    resized_list = []
    for img in images:
        # cv2.resize 的尺寸參數為 (width, height)
        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        resized_list.append(resized)
    return np.array(resized_list)

# -------------------------------
# 自定義資料集 (一次先完成縮放處理，避免每個 epoch 都做)
# -------------------------------
class DummyDataset(Dataset):
    def __init__(self, num_samples, seq_length=1503, orig_H=400, orig_W=600, C=3,
                 num_classes=10, target_H=200, target_W=300):
        """
        num_samples : 資料筆數
        seq_length  : 每筆資料包含的圖片數量
        orig_H, orig_W : 原始圖片高度與寬度
        target_H, target_W : 縮放後的圖片高度與寬度
        """
        self.num_samples = num_samples
        self.data = []
        # 在初始化階段先產生並縮放好所有資料
        for i in range(num_samples):
            # 產生原始圖片資料 (seq_length, orig_H, orig_W, C)，數值介於 0~255
            images = np.random.randint(0, 256, (seq_length, orig_H, orig_W, C), dtype=np.uint8)
            # 使用 OpenCV 逐張圖片縮放
            images_resized = resize_images(images, new_width=target_W, new_height=target_H)
            # 將 numpy 陣列轉成 float tensor（依需求可 normalize）
            images_tensor = torch.FloatTensor(images_resized)
            # 模擬每張圖片的標籤（整數型別）
            labels = torch.randint(0, num_classes, (seq_length,))
            self.data.append((images_tensor, labels))
        
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        # 直接回傳預先處理好的資料
        return self.data[idx]

class TFDataset(Dataset):
    def __init__(self, file_list, seq_length=1503, target_H=200, target_W=300, num_samples=0):
        self.file_list = file_list
        self.seq_length = seq_length
        self.target_H = target_H
        self.target_W = target_W

        # for file in file_list:
        #     image_list, label_list = decompression(file)
        #     image_array = np.array(image_list)
        #     # 檢查圖片數量
        #     if image_array.shape[0] != seq_length:
        #         print(f"檔案 {file} 的圖片數量不符預期，已跳過。")
        #         continue
        #     # 加入有效資料
        #     # self.data.append((torch.FloatTensor(image_array), torch.LongTensor(label_list)))

        #     labels = torch.randint(0, num_classes, (seq_length,))
        #     self.data.append((torch.FloatTensor(image_array), labels))

        # # 只在有效資料大於 0 時繼續
        # if len(self.data) == 0:
        #     print("無有效資料，請檢查檔案。")

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        file = self.file_list[idx]
        image_list, label_list = decompression(file)
        image_array = np.array(image_list, dtype=np.float32)

        # 若 labels 維度末端是 4，假設為 one-hot，則取 argmax 得到 shape (seq_length,)
        labels = np.array(label_list, dtype=np.int64)
        if labels.ndim == 2 and labels.shape[-1] == 4:
            labels = np.argmax(labels, axis=-1)

        return torch.from_numpy(image_array), torch.from_numpy(labels)

# -------------------------------
# 超參數設定與資料準備
# -------------------------------
embedding_dim = 32    # CNN 與 Transformer 的特徵維度
num_heads = 8          # Transformer 的多頭注意力數量
num_layers = 4         # Transformer Encoder 的層數
num_samples = 100      # 模擬資料筆數
seq_length = 8159
orig_H, orig_W, C = 400, 60, 3
scale = 1
# 設定縮放後的尺寸，降低圖片解析度以減少記憶體使用
target_H, target_W = int(orig_H*scale), int(orig_W*scale)
num_classes = 4
batch_size = 1        # 較小的 batch_size 可降低記憶體需求
num_epochs = 4            # 訓練的 epochs 數量  


if __name__ == "__main__":
    # 取得目前程式檔案所在的目錄（如果在互動模式下執行，則可改用 os.getcwd()）
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 設定目標資料夾路徑：當前檔案所在目錄下的 "src/models"
    models_dir = os.path.join(base_dir, "models")
    # 如果 "models" 資料夾不存在，就建立它
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    # 指定要儲存的檔案路徑
    model_path = os.path.join(models_dir, "checkpoint.pth")
    best_model_path = os.path.join(models_dir, "checkpoint_best.pth")
    # 如果檔案不存在，建立空檔案（通常 torch.save 會自動建立檔案，但你可以預先檢查）
    if not os.path.isfile(model_path):
        with open(model_path, "a") as f:
            pass
    if not os.path.isfile(best_model_path):
        with open(best_model_path, "a") as f:
            pass

    # train_dataset = DummyDataset(num_samples, seq_length, orig_H, orig_W, C,
    #                             num_classes, target_H, target_W)
    file_list = [f"G://Mel_tfrecords/song{i}.tfrecords" for i in range(1, 1 + num_samples)]
    train_dataset = TFDataset(file_list, seq_length, target_H, target_W, num_samples = len(file_list))
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # -------------------------------
    # 初始化模型、損失函數與優化器
    # -------------------------------
    model = CNNTransformerModel(embedding_dim=embedding_dim, num_heads=num_heads, num_layers=num_layers,
                                num_classes=num_classes, seq_length=seq_length).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 使用混合精度訓練 (AMP)
    scaler = torch.cuda.amp.GradScaler()

    # -------------------------------
    # 訓練階段 (整合 tqdm 顯示進度與 checkpoint 儲存)
    # -------------------------------
    epoch_losses = []       # 紀錄每個 epoch 的 loss
    best_loss = float('inf')  # 目前最低 loss
    best_epoch = -1         # 最佳模型所屬的 epoch

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        train_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")
        for batch_idx, (images, labels) in enumerate(train_bar):
            images = images.to(device)   # (B, seq_length, target_H, target_W, C)
            labels = labels.to(device)   # (B, seq_length)
            
            optimizer.zero_grad()
            with torch.cuda.amp.autocast():
                outputs = model(images)  # 輸出 shape: (B, seq_length, num_classes)
                B, L, _ = outputs.size()
                outputs_flat = outputs.view(B * L, num_classes)
                labels_flat = labels.view(B * L)
                loss = criterion(outputs_flat, labels_flat)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            running_loss += loss.item()
            train_bar.set_postfix(loss=running_loss/(batch_idx+1))
        
        avg_loss = running_loss / len(train_loader)
        epoch_losses.append(avg_loss)
        print(f"Epoch {epoch+1}/{num_epochs} 完成，平均 Loss: {avg_loss:.4f}")
        
        # 如果當前 loss 為最低，則儲存最佳 checkpoint
        if avg_loss < best_loss:
            best_loss = avg_loss
            best_epoch = epoch+1
            checkpoint = {
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "embedding_dim": embedding_dim,
                "num_heads": num_heads,
                "num_layers": num_layers,
                "epoch": epoch+1,
                "avg_loss": avg_loss,
                "seq_length": seq_length,
                "orig_H": orig_H,
                "orig_W": orig_W,
                "target_H": target_H,
                "target_W": target_W,
                "num_classes": num_classes,
            }
            torch.save(checkpoint, best_model_path)
            print(f"新最佳模型已儲存於 checkpoint_best.pth (Epoch {epoch+1}, Loss: {avg_loss:.4f})")

    # 儲存最終的模型 checkpoint
    checkpoint_final = {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "embedding_dim": embedding_dim,
        "num_heads": num_heads,
        "num_layers": num_layers,
        "epoch": num_epochs,
        "avg_loss": epoch_losses[-1],
        "seq_length": seq_length,
        "orig_H": orig_H,
        "orig_W": orig_W,
        "target_H": target_H,
        "target_W": target_W,
        "num_classes": num_classes,
    }
    torch.save(checkpoint_final, model_path)
    print(f"最終模型已儲存於 checkpoint_final.pth (Epoch {num_epochs}, Loss: {epoch_losses[-1]:.4f})")

    # 可選：顯示每個 epoch 的 loss
    print("每個 epoch 的 Loss:", epoch_losses)

    # # -------------------------------
    # # 推論階段 (使用 tqdm 顯示進度)
    # # -------------------------------
    # model.eval()
    # # 用一個新的資料集模擬推論
    # test_dataset = DummyDataset(num_samples=5, seq_length=seq_length, orig_H=orig_H,
    #                             orig_W=orig_W, C=C, num_classes=num_classes,
    #                             target_H=target_H, target_W=target_W)
    # test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

    # all_preds = []
    # inference_bar = tqdm(test_loader, desc="推論中")
    # with torch.no_grad(), torch.cuda.amp.autocast():
    #     for images, _ in inference_bar:
    #         images = images.to(device)
    #         test_logits = model(images)  # (B, seq_length, num_classes)
    #         predicted_labels = torch.argmax(test_logits, dim=-1)  # (B, seq_length)
    #         all_preds.append(predicted_labels.cpu())
            
    # print("推論完成，總筆數:", len(all_preds))