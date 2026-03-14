import os

def rename_files_in_folders(parent_folder):
    # 取得所有子資料夾，並排序確保順序
    subfolders = sorted([f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))])
    
    for idx, subfolder in enumerate(subfolders, start=1):  # 遍歷所有資料夾
        folder_path = os.path.join(parent_folder, subfolder)
        
        for file_name in sorted(os.listdir(folder_path)):  # 確保順序一致
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                extension = os.path.splitext(file_name)[1]  # 取得副檔名
                new_name = f"song{idx}{extension}"
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)
                print(f"Renamed: {file_path} -> {new_path}")
        new_folder_name = f"song{idx}"
        new_folder_path = os.path.join(parent_folder, new_folder_name)
        os.rename(folder_path, new_folder_path)


if __name__ == "__main__":
    target_directory = "data/oni"  # 請更換為實際的目標資料夾路徑
    rename_files_in_folders(target_directory)
