import librosa
import matplotlib
import matplotlib.pyplot as plt
from scipy.fft import fft
import os
import glob
from PIL import Image
import numpy as np
from array_zip import comprassion


def picture_setting():
    plt.figure(dpi=100) # 将显示的所有图分辨率调高
    # matplotlib.rc("font",family='SimHei') # 显示中文
    # matplotlib.rcParams['axes.unicode_minus']=False # 显示符号
    # song_path = "./tensorflow/song1-0.032-240.ogg"

def displaySpectrogram(song_path,file_firstname,output_Path,time,pic_max,save_jpg,turn_zip,zip_path):
    picture_setting()
    x, sr = librosa.load(song_path, sr=16000)

    # compute power spectrogram with stft(short-time fourier transform):
    # 基于stft，计算power spectrogram
    spectrogram = librosa.amplitude_to_db(librosa.stft(x))
    # show
    librosa.display.specshow(spectrogram, y_axis='log')
    # plt.colorbar(format='%+2.0f dB')
    #去白框
    plt.axis("off")
    plt.margins(0,0)
    os.listdir()
    plt.savefig("./tensorflow/song_to_wav/Convert.jpg", bbox_inches="tight", pad_inches=0)
    im2 = reshape_output(pic_max)
    if save_jpg == True:
        im2.save(output_Path+"/"+file_firstname+"_"+str(time/1)+".jpg")
    if turn_zip == True:
        img_array = np.array(im2) # image轉numpy
        comprassion(img_array,file_firstname,zip_path,time)
    plt.close('all')
        
    
def reshape_output(pic_max):
    imgs = glob.glob("./tensorflow/song_to_wav/Convert.jpg")
    for i in imgs:
        im = Image.open(i)
        size = im.size
        max = pic_max                # 設定長或寬最大的數值
        if size[0]>size[1]:          # 如果原始圖片 width 大於 height
            scale = size[1]/size[0]  # 設定 scale 為 height/width
            w = max                  # 設定調整後的寬度為最大的數值
            h = int(max*scale)       # 設定調整後的高度為 max 乘以 scale ( 使用 int 去除小數點 )
        else:                        # 如果原始圖片 width 小於等於 height
            scale = size[0]/size[1]  # 設定 scale 為 width/height
            w = int(max*scale)       # 設定調整後的寬度為 max 乘以 scale ( 使用 int 去除小數點 )
            h = max                  # 設定調整後的高度為最大的數值
        # name = i.split('/')[::-1][0]
        im2 = im.resize((w, h))      # 調整尺寸
        return im2






# song_name = "you"
# # song_path = "./tensorflow/song/" + song_name + "/" +  song_name + ".ogg"
# song_path = "./" + song_name + ".ogg"
# cut_song_Path = "./tensorflow/song_to_wav/training filder/" + song_name + "/cut song filder"
# jpg_Path = "./tensorflow/song_to_wav/training filder/" + song_name + "/jpg filder"
# zip_path = "./tensorflow/song_to_wav/training filder/" + song_name + "/zip filder"
# reshape = True
# pic_max = 32
# # displaySpectrogram(cut_song_Path+"/"+song_name,song_name,jpg_Path,1)
# displaySpectrogram(cut_song_Path + "/" + "you_1.0.jpg" ,song_name,jpg_Path,1,reshape,pic_max)



# time = 1
# input_Path = "./tensorflow/output_song"
# output_Path = "./tensorflow/output_jpg"
# file_firstname = "song1"
# allFileList = os.listdir(input_Path)
# for file in allFileList:
#     if os.path.isdir(os.path.join(input_Path,file)):
#         print("I'm a directory: " + file)
#     else:
#         print(file)
#         
#     time = time + 1
