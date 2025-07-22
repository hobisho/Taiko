from split_song.readdata import TjaData 
from pydub import AudioSegment

def count_sec(bpm=188,duration=60,take_off=0,piece=1808):
    duration = duration/1000
    take_off = take_off/1000
    ideal_per_cut = 15/bpm
    cut_per = round(15000/bpm)/1000
    print("====",cut_per)

    duration_cut = duration - take_off
    cut_sum = 0
    n = 1
    r = 0.001
    time = []
    while(n<=piece):
        cut = cut_per

        if((cut_sum - n*ideal_per_cut) > r):
            cut -= r
        if ((cut_sum - n*ideal_per_cut) < -r):
            cut += r
        if ((duration_cut-cut_sum)<cut):
            cut= duration_cut-cut_sum
            if (cut > 0.1):
                time.append(cut)
            print("error:song not enough")
            return -1

        cut_sum += cut
        n += 1
        time.append(cut)
    return time

        # print(cut, " ",cut_sum," ", n * ideal_per_cut)
    
if __name__ == "__main__":
    audio = AudioSegment.from_file("v2/data/level 6~7/song13/song13.ogg")
    print(len(audio))
    tja_data=TjaData("v2/data/level 6~7/song13")
    print(tja_data.Bpm(),  tja_data.Offset()*1000, tja_data.Piece())
    time = count_sec(bpm=tja_data.Bpm(),duration=len(audio),take_off= tja_data.Offset()*1000,piece = tja_data.Piece())#912
    print(len(time))
    


