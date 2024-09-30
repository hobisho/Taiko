def count_sec(bpm=188,duration=60,take_off=0):
    ideal_per_cut = 30/bpm
    cut_per = round(30000/bpm)/1000

    duration_cut = duration - take_off
    cut_sum = 0
    n = 1
    r = 0.001
    time = []
    while(cut_sum<duration_cut):
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

        # print(cut, " ",cut_sum," ", n * ideal_per_cut)
    



