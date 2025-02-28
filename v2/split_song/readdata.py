import os
import re
import shutil


#改成class
def extract_level_value(folder_path):
    Numeric=[]
    # 找出資料夾內的 .tja 檔案（不考慮最前面的數字）
    tja_file_path = None
    for file in os.listdir(folder_path):
        if file.endswith(".tja"):
            tja_file_path = os.path.join(folder_path, file)
            break
    
    # if not tja_file_path:
    #     print(f"未找到TJA檔於: {folder_path}")
    #     print(f"{os.path.basename(folder_path)} 資料夾內的檔案:")
    #     for file in os.listdir(folder_path):
    #         print(f"  - {file}")
    #     return None
    
    with open(tja_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # 使用正則表達式提取 LEVEL: 後的數值
    level = re.search(r'LEVEL:\s*(\d+)', content)
    if level:
         Numeric.append(int(level.group(1)))
    else:
        print(f"未找到 LEVEL 數值於: {tja_file_path}")
        return None
    
    # 使用正則表達式提取 BPM: 後的數值
    level = re.search(r'BPM:\s*(\d+)', content)
    if level:
         Numeric.append(int(level.group(1)))
    else:
        print(f"未找到 BPM 數值於: {tja_file_path}")
        return None
    
    # 使用正則表達式提取 OFFSET: 後的數值
    level = re.search(r'OFFSET:-*(\d+\.\d+)', content)
    if level:
        print(level)
        Numeric.append(float(level.group(1)))
    else:
        print(f"未找到 OFFSET 數值於: {tja_file_path}")
        Numeric.append(0)
    
    return Numeric


if __name__ == "__main__":
    folder="Taiko-switch/1. J-POP/01. Takane no Hanako-san"
    print(extract_level_value(folder))