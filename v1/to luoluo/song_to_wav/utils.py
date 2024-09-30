from subprocess import PIPE, Popen as system_call
from sys import exit

def require_ffmpeg():
  print("checking ffmpeg......")
  process = system_call("ffmpeg -version", shell=True, stdout=PIPE)

  output = process.communicate()[0].decode('ascii')
  
  if not output.startswith("ffmpeg version"):
    print("請先安裝 ffmpeg 至 envirment 中再來執行此程序")
    exit()