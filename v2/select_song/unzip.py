import os
import zipfile
import rarfile

def extract_files_recursive(folder_path):
    """遞迴遍歷資料夾內的所有 ZIP 和 RAR 檔案，並將內容存入 extracted_files 資料夾"""
    
    extract_folder = os.path.join(folder_path, "extracted_files")
    os.makedirs(extract_folder, exist_ok=True)

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # 目標解壓縮路徑 (保持相對結構)
            relative_path = os.path.relpath(root, folder_path)
            file_extract_folder = os.path.join(extract_folder, relative_path, file[:-4])
            os.makedirs(file_extract_folder, exist_ok=True)

            # 處理 ZIP 壓縮檔
            if file.lower().endswith(".zip"):
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(file_extract_folder)
                        print(f"已解壓縮: {file_path} → {file_extract_folder}")
                except Exception as e:
                    print(f"解壓縮 ZIP 檔案失敗: {file_path}，錯誤: {e}")

            # 處理 RAR 壓縮檔
            elif file.lower().endswith(".rar"):
                try:
                    with rarfile.RarFile(file_path, 'r') as rar_ref:
                        rar_ref.extractall(file_extract_folder)
                        print(f"已解壓縮: {file_path} → {file_extract_folder}")
                except Exception as e:
                    print(f"解壓縮 RAR 檔案失敗: {file_path}，錯誤: {e}")

if __name__ == "__main__":
    folder_path = input("請輸入要解壓縮的資料夾路徑: ").strip()
    if os.path.exists(folder_path):
        extract_files_recursive(folder_path)
        print(f"\n所有壓縮檔已解壓縮完成！解壓縮內容存放於: {os.path.join(folder_path, 'extracted_files')}")
    else:
        print("錯誤: 資料夾不存在！")
