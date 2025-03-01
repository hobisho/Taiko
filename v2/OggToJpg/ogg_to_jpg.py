import os
from ogg_to_wav   import displaySpectrogram

def ogg_to_jpg(input_Path,output_Path,file_firstname,pic_max,save_jpg,turn_zip,zip_path):
  #找資料夾+轉圖檔
  allFileList = os.listdir(input_Path)
  time = 1
  for file in allFileList:
      if os.path.isdir(os.path.join(input_Path,file)):
          print("I'm a directory: " + file)
      else:
          # print(file)
          displaySpectrogram(input_Path + "/" + file ,file_firstname,output_Path,time,pic_max,save_jpg,turn_zip,zip_path)
          time = time + 1
          
if __name__ == "__main__":
    displaySpectrogram()
