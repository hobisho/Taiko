import os
import numpy as np
from osu import main 

def to_binary(chart):
    # 0: 無敲擊, 1/2: 有敲擊
    return [int(x > 0) for x in chart]

def ADA(chart, chart2):
    limit = min(len(chart), len(chart2))
    start = 0
    similarity = 0
    buffer = 1

    while start < limit and chart2[start] == 0:
        start += 1

    total = limit - start

    if total <= 0:
        print("0 percent similar\n")
        return 0

    for i in range(start, limit):
        if chart[i] in [1, 2]:
            for b in range(-buffer, buffer + 1):
                j = i + b
                if 0 <= j < limit and chart2[j] in [1, 2]:
                    similarity += 1
                    break
        elif chart[i] == 0:
            if chart2[i] == 0:
                similarity += 1

    result = (similarity / total) * 100
    print(result, "percent similar\n")
    return result


def LUO(chart, chart2):
    SCALE = 8
    
    patterns1 = set()
    patterns2 = set()
    last_ind1 = len(chart) - SCALE + 1
    last_ind2 = len(chart2) - SCALE + 1

    for i in range(last_ind1):
        chunk = tuple(chart[i:i+SCALE])
        patterns1.add(chunk)
    
    for i in range(last_ind2):
        chunk = tuple(chart2[i:i+SCALE])
        patterns2.add(chunk)

    if len(patterns2) == 0:
        print("0 pattern score")
        return 0

    p_score = len(patterns1.intersection(patterns2))
    p_score = (p_score / len(patterns2)) * 100
    print(p_score, "pattern score\n")
    return p_score


def HI_P_Space(ai_chart_binary, human_chart_binary):
        # 根據論文定義，使用包含 8 個時間點的滑動視窗來衡量模式 [1]
        window_size = 8 #11
        
        # 如果譜面長度不足以形成一個完整的模式，則回傳 0
        ai_chart_binary = to_binary(ai_chart_binary)

    # 擷取人類譜面中所有出現過的獨特模式
        human_chart_binary = to_binary(human_chart_binary)
        
        if len(human_chart_binary) < window_size:
            return 0.0
            
        # 使用集合 (set) 來過濾並儲存獨特的排列模式
        ai_patterns = set()
        human_patterns = set()
        
        # 擷取 AI 譜面中所有出現過的獨特模式
        for i in range(len(ai_chart_binary) - window_size + 1):
            ai_patterns.add(tuple(ai_chart_binary[i : i + window_size]))
            
        # 擷取人類譜面中所有出現過的獨特模式
        for i in range(len(human_chart_binary) - window_size + 1):
            human_patterns.add(tuple(human_chart_binary[i : i + window_size]))
            
        # 避免除以零的錯誤
        if len(human_patterns) == 0:
            return 0.0
            
        # 取得模型與人類的模式交集 [1]
        intersection = ai_patterns.intersection(human_patterns)
        
        # 計算 HI P-Space 分數：將交集大小與人類總模式數量進行對比 [1]
        score = len(intersection) / len(human_patterns)
        
        return score
    
    
def DCHuman(x, y):
    return np.mean(np.array(x) == np.array(y))


def OCHuman(human, ai, tolerance=1):
    human_bin = to_binary(human)
    ai_bin = to_binary(ai)
    hit_count = 0
    total_count = 0
    L = len(human_bin)
    for i in range(L):
        if human_bin[i] == 1:
            total_count += 1
            match = False
            for j in range(max(0, i-tolerance), min(L, i+tolerance+1)):
                if ai_bin[j] == 1:
                    match = True
                    break
            if match:
                hit_count += 1
    return hit_count / total_count if total_count > 0 else 0


def DCRandom(ai, tolerance=1):
    human_bin = np.random.choice([0, 1], size=len(ai))
    return OCHuman(human_bin, ai, tolerance=1)


if __name__ == "__main__":
    filepath = 'TaikoNationV1-main/eval/evaluation dataset/ai_taiko_set'  # 改成你的檔名
    file = os.listdir(filepath)
    total_hi = 0
    total_oc = 0
    for i in range(1,11):
        print(i)
        _,_,_,_,chart_ai = main(filepath+"/"+str(file[i-1]))
        _,_,_,_,chart_human = main(f"data/eval/song{i}/song{i}.osu")
        # print(chart_ai)
        # print(chart_human)
        total_hi = total_hi + LUO(chart_human,chart_ai)
        total_oc = total_oc + ADA(chart_human,chart_ai)
    print(total_hi/10)
    print(total_oc/10)

        
    