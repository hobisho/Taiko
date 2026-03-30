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

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("使用裝置:", device)


class CNNFeatureExtractor(nn.Module):
    def __init__(self, embedding_dim):
        super(CNNFeatureExtractor, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=2, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(128, embedding_dim)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


class CNNTransformerModel(nn.Module):
    def __init__(self, embedding_dim=256, num_heads=8, num_layers=4, num_classes=10, seq_length=1503):
        super(CNNTransformerModel, self).__init__()
        self.seq_length = seq_length
        self.embedding_dim = embedding_dim
        self.cnn_extractor = CNNFeatureExtractor(embedding_dim)
        self.pos_embedding = nn.Parameter(torch.randn(1, seq_length, embedding_dim))
        encoder_layer = nn.TransformerEncoderLayer(d_model=embedding_dim, nhead=num_heads)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc_out = nn.Linear(embedding_dim, num_classes)

    def forward(self, x):
        B, L, H, W, C = x.size()
        assert L == self.seq_length, f"輸入圖片數 {L} 必須等於預設的 seq_length {self.seq_length}"

        x = x.permute(0, 1, 4, 2, 3)
        x = x.reshape(B * L, C, H, W)
        features = self.cnn_extractor(x)
        features = features.view(B, L, self.embedding_dim)
        features = features + self.pos_embedding[:, :L, :]
        features = features.permute(1, 0, 2)
        trans_out = self.transformer(features)
        trans_out = trans_out.permute(1, 0, 2)
        logits = self.fc_out(trans_out)
        return logits


class TFDataset(Dataset):
    def __init__(self, file_list, seq_length=1503, target_H=200, target_W=300, num_samples=0):
        self.file_list = file_list
        self.seq_length = seq_length
        self.target_H = target_H
        self.target_W = target_W

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        file = self.file_list[idx]
        image_list, label_list = decompression(file)
        image_array = np.array(image_list, dtype=np.float32)

        labels = np.array(label_list, dtype=np.int64)
        if labels.ndim == 2 and labels.shape[-1] == 4:
            labels = np.argmax(labels, axis=-1)

        return torch.from_numpy(image_array), torch.from_numpy(labels)


embedding_dim = 64
num_heads = 8
num_layers = 4
num_samples = 80
seq_length = 8160
orig_H, orig_W, C = 128, 60, 3
scale = 1
target_H, target_W = int(orig_H * scale), int(orig_W * scale)
num_classes = 4
batch_size = 4

# 你想「總共」跑幾個 epoch
total_epochs = 8

# True = 優先讀 best checkpoint，False = 讀一般 checkpoint
resume_from_best = True


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    model_path = os.path.join(models_dir, "20260330/checkpoint.pth")
    best_model_path = os.path.join(models_dir, "20260330/checkpoint_best.pth")

    file_list = [f"G://1Mel_tfrecords/song{i}.tfrecords" for i in range(1, 1 + num_samples)]
    train_dataset = TFDataset(file_list, seq_length, target_H, target_W, num_samples=len(file_list))
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    model = CNNTransformerModel(
        embedding_dim=embedding_dim,
        num_heads=num_heads,
        num_layers=num_layers,
        num_classes=num_classes,
        seq_length=seq_length
    ).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    scaler = torch.cuda.amp.GradScaler()

    start_epoch = 0
    best_loss = float("inf")
    epoch_losses = []

    resume_path = best_model_path if resume_from_best else model_path

    # -------- 載入 checkpoint --------
    if os.path.exists(resume_path) and os.path.getsize(resume_path) > 0:
        print(f"載入 checkpoint: {resume_path}")
        checkpoint = torch.load(resume_path, map_location=device)

        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

        # 若 checkpoint 有存 scaler，就一起載入
        if "scaler_state_dict" in checkpoint:
            scaler.load_state_dict(checkpoint["scaler_state_dict"])

        start_epoch = checkpoint["epoch"]
        best_loss = checkpoint.get("best_loss", checkpoint.get("avg_loss", float("inf")))

        print(f"將從 epoch {start_epoch + 1} 繼續訓練")
        print(f"目前 best_loss: {best_loss:.4f}")
    else:
        print("找不到可用 checkpoint，從頭開始訓練")

    # -------- 接續訓練 --------
    for epoch in range(start_epoch, total_epochs):
        model.train()
        running_loss = 0.0
        train_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{total_epochs}")

        for batch_idx, (images, labels) in enumerate(train_bar):
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)

            with torch.cuda.amp.autocast():
                outputs = model(images)
                B, L, _ = outputs.size()
                outputs_flat = outputs.reshape(B * L, num_classes)
                labels_flat = labels.reshape(B * L)
                loss = criterion(outputs_flat, labels_flat)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            running_loss += loss.item()
            train_bar.set_postfix(loss=running_loss / (batch_idx + 1))

        avg_loss = running_loss / len(train_loader)
        epoch_losses.append(avg_loss)
        print(f"Epoch {epoch+1}/{total_epochs} 完成，平均 Loss: {avg_loss:.4f}")

        # 每個 epoch 都存一般 checkpoint
        checkpoint = {
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scaler_state_dict": scaler.state_dict(),
            "embedding_dim": embedding_dim,
            "num_heads": num_heads,
            "num_layers": num_layers,
            "epoch": epoch + 1,
            "avg_loss": avg_loss,
            "best_loss": best_loss,
            "seq_length": seq_length,
            "orig_H": orig_H,
            "orig_W": orig_W,
            "target_H": target_H,
            "target_W": target_W,
            "num_classes": num_classes,
        }
        torch.save(checkpoint, model_path)

        # 最佳模型
        if avg_loss < best_loss:
            best_loss = avg_loss
            checkpoint["best_loss"] = best_loss
            torch.save(checkpoint, best_model_path)
            print(f"新最佳模型已儲存於 checkpoint_best.pth (Epoch {epoch+1}, Loss: {avg_loss:.4f})")

    print("訓練完成")
    print("本次續跑的 epoch losses:", epoch_losses)