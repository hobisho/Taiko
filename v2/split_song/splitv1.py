from os           import path
from audioread    import audio_open
from utils        import require_ffmpeg
from wrappers     import start_wrapper, main
from subprocess   import PIPE, STDOUT, Popen as system_call
import os,numpy   as np
from ogg_to_wav   import displaySpectrogram
from song_sec     import count_sec
from filder          import setting


def get_filename_arr(filename):
  filename_arr = filename.split('.')
  while len(filename_arr) > 2:
    filename_arr[1] = filename_arr[0] + filename_arr[1]
    filename_arr = filename_arr[1:]
  
  return filename_arr

def split_audio(filename, take_off = 0, bpm = 188, output_folder = '.',piece = 5000):
  if not path.isdir(output_folder):
    raise Exception("Please check folder exist")

  print("spliting song to"+str(bpm)+"a sec...")

  start_time = take_off

  print('open audio file...')
  audio = audio_open(filename)
  duration = audio.duration

  num = 1
  [output_name, extension] = get_filename_arr(filename)

  result = {
    "len": 0,
    "output_file": []
  }
  split_time=count_sec(bpm , duration ,take_off = take_off,piece = piece)
  while num <= len(split_time):
      
    available_duration  =  split_time[num-1]
    
    convert_process = system_call(
      [
        'ffmpeg',
        '-y',
      
        '-ss',
        f'{start_time}',
      
        '-t',
        f'{available_duration}',

        '-i',
        f'{filename}',

        '-acodec',
        'copy',

        f'{output_folder}/{output_name}-{bpm}-{num}.{extension}'
      ], shell=True, stdout=PIPE, stderr=STDOUT
    )

    convert_process.wait()

    result["len"] += 1
    result["output_file"].append(f"{output_name}-{bpm}-{num}.{extension}")

    start_time += split_time[num-1]
    num = num + 1
  print("split song end")
  return result


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




#資料設定
song_name = "Song 50"
# song_path = "./tensorflow/song/" + song_name + "/" +  song_name + ".ogg"
song_path = "./" + song_name + ".ogg"
cut_song_Path = "./tensorflow/song_to_wav/training filder/" + song_name + "/cut song filder"
jpg_Path = "./tensorflow/song_to_wav/training filder/" + song_name + "/jpg filder"
zip_path = "./tensorflow/song_to_wav/training filder/" + song_name + "/zip_filder"
# Users/User/Desktop/school/python
pic_max = 32
save_jpg = True
turn_zip = True
piece  = 912

#主程式
setting(song_name,save_jpg,turn_zip)
split_audio(song_path,take_off = 11.75, bpm = 175, output_folder=cut_song_Path,piece=piece)
ogg_to_jpg(cut_song_Path,jpg_Path,song_name,pic_max,save_jpg,turn_zip,zip_path)
os.remove("./tensorflow/song_to_wav/Convert.jpg")


