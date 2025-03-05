from compression.compression_file import CompressionFile
from tjaread.tjaread import parse_tja_file 

def labal_part(song_number):
    parse_tja_file("v2/data/level 6~7/song{song_number}")
    

