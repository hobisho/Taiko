import os
import re
import shutil
import sys
sys.path.append(r"v2/label")
from tjaread import parse_tja_file


def extract_level_value(folder_path):
    # 找出資料夾內的 .tja 檔案（不考慮最前面的數字）
    tja_file_path = None
    for file in os.listdir(folder_path):
        if file.endswith(".tja"):
            tja_file_path = os.path.join(folder_path, file)
            break
    
    if not tja_file_path:
        print(f"未找到TJA檔於: {folder_path}")
        print(f"{os.path.basename(folder_path)} 資料夾內的檔案:")
        for file in os.listdir(folder_path):
            print(f"  - {file}")
        return None
    
    with open(tja_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # 使用正則表達式提取 LEVEL: 後的數值BPMCHANGE
    match = re.search(r'LEVEL:\s*(\d+)', content)
    bpmchange = re.search(r'BPMCHANGE', content)
    measure = re.search(r'MEASURE', content)
    
    if bpmchange:
        return int(0)
    elif measure:
        return int(0)
    elif parse_tja_file(folder_path)==None:
        return int(0)
    elif match:
        return int(match.group(1))    
    else:
        print(f"未找到 LEVEL 數值於: {tja_file_path}")
        return None

def copy_folder_if_level_in_range(root_folder, destination_folder):
    # 確保目標資料夾存在
    os.makedirs(destination_folder, exist_ok=True)
    
    # 遍歷主資料夾內的所有子資料夾
    for subfolder in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, subfolder)
        if os.path.isdir(subfolder_path):
            level_value = extract_level_value(subfolder_path)
            if level_value is not None and 6 <= level_value <= 7:
                dest_path = os.path.join(destination_folder, subfolder)
                shutil.copytree(subfolder_path, dest_path, dirs_exist_ok=True)
                print(f"已複製 {subfolder} 到 {dest_path}")

if __name__ == "__main__":
    root_folder = "Taiko-switch"
    for subfolder in os.listdir(root_folder):
        root_folder_path = os.path.join(root_folder, subfolder)  # 請修改為你的資料夾路徑
        destination_folder_path = "v2/data/level 6~7"  # 請修改為你的目標資料夾路徑
        copy_folder_if_level_in_range(root_folder_path, destination_folder_path)