from split_song.readdata import TjaData 
from pydub import AudioSegment

def count_sec(bpm=188,duration=60,take_off=0,piece=1808):# 單位ms
    duration = duration
    take_off = round(take_off,0)
    ideal_per_cut = 60/bpm*4/48 * 1000
    cut_per = round(ideal_per_cut,1)

    # print(f"cut_per: {ideal_per_cut}, duration: {duration}, take_off: {take_off}, piece: {piece}")

    duration_cut = duration - take_off
    cut_sum = 0
    n = 1
    error = 0.2
    time = []
    while(n<=piece):
        cut = cut_per

        if((cut_sum - n*ideal_per_cut) > error):
            cut -= error
        if ((cut_sum - n*ideal_per_cut) < -error):
            cut += error
        if ((duration_cut-cut_sum)<cut):
            cut= duration_cut-cut_sum
            if ((piece-n)>48):
                print("error:song not enough")
                return -1

        cut_sum += cut
        n += 1
        time.append(cut)
    return time

        # print(cut, " ",cut_sum," ", n * ideal_per_cut)
    
if __name__ == "__main__":
    # for i in range(1,109):
        
    #     audio = AudioSegment.from_file(f"data/oni/song{i}/song{i}.ogg")
    #     # print(len(audio))
    #     tja_data=TjaData(f"data/oni/song{i}")
    #     # print(tja_data.Bpm(),  tja_data.Offset()*1000, tja_data.Piece())
    #     time = count_sec(bpm=tja_data.Bpm(),duration=len(audio),take_off= tja_data.Offset()*1000,piece = tja_data.Piece())
    #     if time == -1:
    #         print(f"song{i} not enough")

    i = 28
    audio = AudioSegment.from_file(f"data/oni/song{i}/song{i}.ogg")
    print(len(audio))
    tja_data=TjaData(f"data/oni/song{i}")
    print(tja_data.Bpm(),  tja_data.Offset()*1000, tja_data.Piece())
    time = count_sec(bpm=tja_data.Bpm(),duration=len(audio),take_off= tja_data.Offset()*1000,piece = tja_data.Piece())#912
    print(len(time))
        


