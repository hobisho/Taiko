from tqdm import tqdm
from time import sleep


total = 900

# 每次包10個螺絲， 共會有幾份工作
with tqdm(total=total) as pbar:
    for i in range(int(total)):
        pbar.update(1)
