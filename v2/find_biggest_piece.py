from split_song.readdata import TjaData
import os


if __name__=="__main__":
    a=[]
    biggest=0
    for i in range(1, len(os.listdir("v2/data/level 6~7/"))+1):
        path_name = f'v2/data/level 6~7/song{i}'
        a=TjaData(path_name)
        if (max (biggest,a.Piece())!=biggest):
            biggest = a.Piece()
            biggest_path_name = path_name
        
    print(biggest)
    print(biggest_path_name)
    
#1760piece
#song16
    