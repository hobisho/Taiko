def count_sec(bpm=188,duration=60,take_off=0,piece=912):
    duration = duration/1000
    take_off = take_off/1000
    ideal_per_cut = 15/bpm
    cut_per = round(15000/bpm)/1000

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
            return time

        cut_sum += cut
        n += 1
        time.append(cut)
    return time

        # print(cut, " ",cut_sum," ", n * ideal_per_cut)
    
if __name__ == "__main__":
    time = count_sec(bpm=120,duration=92000,take_off=0)#912
    print(time)


