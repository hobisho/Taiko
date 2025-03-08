import os
import re


#改成class
class TjaData():
    
    def __init__(self,tja_path):
        self.tja_path=tja_path
        pass
    
    def ReadTja(self):
        # 找出資料夾內的 .tja 檔案（不考慮最前面的數字）
        self.tja_file_path = None
        for file in os.listdir(self.tja_path):
            if file.endswith(".tja"):
                self.tja_file_path = os.path.join(self.tja_path, file)
                break
        
        # if not tja_file_path:
        #     print(f"未找到TJA檔於: {folder_path}")
        #     print(f"{os.path.basename(folder_path)} 資料夾內的檔案:")
        #     for file in os.listdir(folder_path):
        #         print(f"  - {file}")
        #     return None
        
        with open(self.tja_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return  content
    
    def Level(self):
        level = re.search(r'LEVEL:\s*(\d+)', self.ReadTja())
        if level:
            return int(level.group(1))
        else:
            print(f"未找到 LEVEL 數值於")
            return None
        
    def Bpm(self):
        # 使用正則表達式提取 BPM: 後的數值
        bpm = re.search(r'BPM:\s*(\d+)', self.ReadTja())
        if bpm:
            return int(bpm.group(1))
        else:
            print(f"未找到 BPM 數值於")
            return None
        
    def Offset(self):# 使用正則表達式提取 OFFSET: 後的數值
        offset = re.search(r'OFFSET:-*(\d+\.\d+)', self.ReadTja())
        if offset:
            # print(offset)
            return float(offset.group(1))
        else:
            return 0
        
    def Piece(self):
        start = False
        song_start = False
        empty=0
        times = 1
        a = self.ReadTja()
        for line in  a.split():
            line = line.strip()
            if line.upper() == "#START":
                start = True
                continue
            
            if line.upper() == "#END":
                # print("end")
                break
            
            if (start&(re.search(r',', line)!= None)):
                if (song_start == False):
                    if (re.findall(r'(\d+),', line)!= []):
                        song_start = True
                elif (song_start == True):
                    if (re.findall(r'(\d+),', line)== []):
                        empty = empty+1
                    else:
                        times = times+1
                        empty=0
                    
                
        return int((times-empty)*16)



if __name__ == "__main__":
    tja_data=TjaData("v2/data/level 6~7/song2")
    print( tja_data.Piece())
    print(tja_data.Bpm())