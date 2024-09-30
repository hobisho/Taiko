from decompression import main
from time import perf_counter, sleep


s = perf_counter()
# a=main('./tensorflow/module/txt_zip')
k=main('./tensorflow/module/BIG_ZIP')
# k=main('./tensorflow/song_to_wav/training filder/All_zip')
# print(k[1][900][20][30])
# print(a[1][900])
e = perf_counter()
print(e-s)


