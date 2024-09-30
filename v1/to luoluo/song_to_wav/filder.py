import os

def mkdir(filder_path,song_name):
    path = filder_path + "/" + song_name
    #判斷目錄是否存在
    #存在：True
    #不存在：False
    folder = os.path.exists(path)

    #判斷結果
    if not folder:
        #如果不存在，則建立新目錄
        os.makedirs(path)
        print('-----建立成功-----')

    else:
        #如果目錄已存在，則不建立，提示目錄已存在
        print(path+'目錄已存在')

def setting(song_name,save_jpg,turn_zip):
    mkdir('./tensorflow/song_to_wav',"training filder")
    mkdir('./tensorflow/song_to_wav/training filder',song_name)
    mkdir('./tensorflow/song_to_wav/training filder' + "/" , "All_zip")   
    mkdir('./tensorflow/song_to_wav/training filder' + "/" + song_name,"cut song filder")
    if save_jpg == True:
        mkdir('./tensorflow/song_to_wav/training filder' + "/" + song_name,"jpg filder")
    if turn_zip == True:
        mkdir('./tensorflow/song_to_wav/training filder' + "/" + song_name,"zip_filder")
    



# song_name = "hi"
# setting(song_name)