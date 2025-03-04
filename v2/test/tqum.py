from tqdm import tqdm
import time

for i in tqdm(range(1, 11)):
	# 這邊可以換上實際工作的執行， 例如： 程式運算、爬蟲...
    # 模擬工作需花費0.5秒
    time.sleep(0.5)