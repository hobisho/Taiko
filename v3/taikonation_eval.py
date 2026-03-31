import os
from osu import main 
from src.eval_funtion import ADA, LUO

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

        
    