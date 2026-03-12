from split_song.readdata import TjaData 
from pydub import AudioSegment

def count_sec(bpm=188,duration=60,take_off=0,piece=1808):
    duration = duration
    take_off = take_off
    ideal_per_cut = 60/bpm*4/48
    cut_per = round(ideal_per_cut,3)

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
    i = 13
    audio = AudioSegment.from_file(f"v2/data/oni/song{i}/song{i}.ogg")
    # print(len(audio))
    tja_data=TjaData(f"v2/data/oni/song{i}")
    print(tja_data.Bpm(),  tja_data.Offset()*1000, tja_data.Piece())
    time = count_sec(bpm=tja_data.Bpm(),duration=len(audio),take_off= tja_data.Offset()*1000,piece = tja_data.Piece())#912
    print(time[0],round(time[0]*0.075,3))
        


