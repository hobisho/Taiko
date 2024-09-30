# from os           import path
# from audioread    import audio_open
# from utils        import require_ffmpeg
# from wrappers     import start_wrapper, main
# from subprocess   import PIPE, STDOUT, Popen as system_call
# import os,numpy   as np
# from ogg_to_wav   import displaySpectrogram
# from song_sec     import count_sec


# def get_filename_arr(filename):
#   filename_arr = filename.split('.')
#   while len(filename_arr) > 2:
#     filename_arr[1] = filename_arr[0] + filename_arr[1]
#     filename_arr = filename_arr[1:]
  
#   return filename_arr

# def split_audio(filename, take_off = 0, bpm = 188, output_folder = '.'):
#   if not path.isdir(output_folder):
#     raise Exception("Please check folder exist")


#   print("spliting song to"+str(bpm)+"a sec...")

#   start_time = take_off

#   print('open audio file...')
#   audio = audio_open(filename)
#   duration = audio.duration

#   num = 1
#   [output_name, extension] = get_filename_arr(filename)

#   result = {
#     "len": 0,
#     "output_file": []
#   }
#   split_time=count_sec(bpm , duration = 5 ,take_off = take_off)
#   while num <= np.size(split_time):
      
#     available_duration  =  split_time[num-1]
    
#     convert_process = system_call(
#       [
#         'ffmpeg',
#         '-y',
      
#         '-ss',
#         f'{start_time}',
      
#         '-t',
#         f'{available_duration}',

#         '-i',
#         f'{filename}',

#         '-acodec',
#         'copy',

#         f'{output_folder}/{output_name}-{bpm}-{num}.{extension}'
#       ], shell=True, stdout=PIPE, stderr=STDOUT
#     )

#     # convert_process.wait()

#     result["len"] += 1
#     result["output_file"].append(f"{output_name}-{bpm}-{num}.{extension}")

#     start_time += split_time[num-1]
#     num = num + 1
#   print("split song end")
#   return result



# def ogg_to_jpg():
#   #設定參數
#   input_Path = "./tensorflow/song_to_wav/output_song"
#   output_Path = "./tensorflow/song_to_wav/output_jpg"
#   file_firstname = "song1"
#   reshape = True
#   pic_max = 32

#   #找資料夾+轉圖檔
#   allFileList = os.listdir(input_Path)
#   time = 1
#   for file in allFileList:
#       if os.path.isdir(os.path.join(input_Path,file)):
#           print("I'm a directory: " + file)
#       else:
#           displaySpectrogram(input_Path+"/"+file,file_firstname,output_Path,time,reshape,pic_max)
#           time = time + 1


# split_audio('song1.ogg',take_off = 2.136, bpm = 188, output_folder="./tensorflow/song_to_wav/output_song")
# ogg_to_jpg()


