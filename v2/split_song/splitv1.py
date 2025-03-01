from os import path
from audioread import audio_open
from utils import require_ffmpeg
from wrappers import start_wrapper, main
from subprocess import PIPE, STDOUT, Popen as system_call
import os,numpy as np
from song_sec import count_sec
from readdata import TjaData



def get_filename_arr(filename):
  filename_arr = filename.split('.')
  while len(filename_arr) > 2:
    filename_arr[1] = filename_arr[0] + filename_arr[1]
    filename_arr = filename_arr[1:]
  
  return filename_arr

def split_audio(file_folder, output_folder = '.',piece = 5000):
  ogg_file_path = None
  for file in os.listdir(file_folder):
    if file.endswith(".tja"):
      ogg_file_path = os.path.join(file_folder, file)
      break
    
  ja_data=TjaData("level 6~7/02. TT -Japanese ver.-")
  if not path.isdir(output_folder):
    raise Exception("Please check folder exist")

  print("spliting song to "+str(ja_data.Bpm())+" a sec...")

  start_time = ja_data.Offset()

  print('open audio file...')
  audio = audio_open(ogg_file_path)
  duration = audio.duration

  num = 1
  [output_name, extension] = get_filename_arr(ogg_file_path)

  result = {
    "len": 0,
    "output_file": []
  }
  split_time=count_sec(ja_data.Bpm() , duration ,take_off = ja_data.Offset(),piece = piece)
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
        f'{ogg_file_path}',

        '-acodec',
        'copy',

        f'{output_folder}/{output_name}-{ja_data.Bpm()}-{num}.{extension}'
      ], shell=True, stdout=PIPE, stderr=STDOUT
    )

    convert_process.wait()

    result["len"] += 1
    result["output_file"].append(f"{output_name}-{ja_data.Bpm()}-{num}.{extension}")

    start_time += split_time[num-1]
    num = num + 1
  print("split song end")
  return result


#主程式
if __name__ == "__main__":
  split_audio("level 6~7/02. TT -Japanese ver.-", output_folder="hi",piece=10)


