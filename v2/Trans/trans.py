def extract_hitobjects_time_hitsound(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    hitobjects_start = False
    timingpoints_start = False
    filtered_hitobjects = []
    timingpoint_value = None

    for line in lines:
        line = line.strip()

        # 找TimingPoints開始
        if line.startswith('[TimingPoints]'):
            timingpoints_start = True
            hitobjects_start = False
            continue

        # 找HitObjects開始
        if line.startswith('[HitObjects]'):
            hitobjects_start = True
            timingpoints_start = False
            continue

        # 讀TimingPoints第一行資料，取第二格
        if timingpoints_start and line != '' and not line.startswith('//') and timingpoint_value is None:
            parts = line.split(',')
            if len(parts) > 1:
                timingpoint_value = parts[1]

        # 讀HitObjects資料，取第3和第5格
        if hitobjects_start:
            if line == '' or line.startswith('['):
                # HitObjects結束
                hitobjects_start = False
                continue
            parts = line.split(',')
            if len(parts) > 4:
                time = parts[2]
                hitsound = parts[4]
                filtered_hitobjects.append(f"{time},{hitsound}")

    return filtered_hitobjects, timingpoint_value


if __name__ == '__main__':
    hit = []
    filepath = 'xyz.osu'  # 改成你的檔名
    hitobjects_data, timingpoint_val = extract_hitobjects_time_hitsound(filepath)

    bpm = 60000/float(timingpoint_val)
    tick = float(timingpoint_val) / 4

    print("TimingPoints第一行第二格：", bpm)
    print("HitObjects第3格與第5格：",hitobjects_data[0])

    now = float(hitobjects_data[0].split(',')[0])- tick/2

    for data in hitobjects_data:
        data_parts = data.split(',')
        while 1:
            range_time = now + tick
            if now < float(data_parts[0]) <= range_time:
                if float(data_parts[1]) <5:
                    hit.append(1)
                    print(1, end='')
                else:
                    hit.append(2)
                    print(2, end='')
                break
            else:
                hit.append(0)
                print(0, end='')
            now = range_time
    print("\n\n\n",len(hit))
    print(tick)