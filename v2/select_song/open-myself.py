import os

def open_txt(folder_path):
    for folder_name in os.listdir(folder_path):
        print(folder_path+folder_name+"/")
        # for file_name in os.listdir(folder_path+folder_name+"/"):
        #     print(file_name)


if __name__ == "__main__":
    folder_path = "./data/Taiko-switch/"
    if os.path.exists(folder_path):
        open_txt(folder_path)
        print(f"\n所有壓縮檔已解壓縮完成！解壓縮內容存放於: {os.path.join(folder_path, 'extracted_files')}")
    else:
        print("錯誤: 資料夾不存在！")