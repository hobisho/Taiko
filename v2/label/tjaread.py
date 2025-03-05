import re
import os
from itertools import chain

def parse_tja_file(folder_path:str)->list:
    file_path = None
    
    # 確保輸出資料夾存在
    for file in os.listdir(folder_path):
        if file.endswith(".tja"):
            file_path = os.path.join(folder_path, file)
            break
        
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    start = False
    numbers = []
    
    for line in lines:
        line = line.strip()
        
        if line.upper() == "#START":
            start = True
            continue
        
        if line.upper() == "#END":
            break
        
        if (start&(re.search(r',', line)!= None)):
            word = ""
            extracted_numbers = re.findall(r'(\d+),', line)  # 輸入數字字串
            
            #if it is 16 numbers
            if (extracted_numbers==[]):
                word_list = ["0"*16]
            
            # elif (len(extracted_numbers[0])==16):
            #     word_list = extracted_numbers

            #if it can be devide by 4 and not 16 numbers
            elif( ((len(extracted_numbers[0])%4)==0)| ((len(extracted_numbers[0]))==1) | ((len(extracted_numbers[0]))==2)):
                #small than 16
                if(len(extracted_numbers[0])<16):
                    multiply = int(16/len(extracted_numbers[0]))
                    for d in extracted_numbers[0]:
                        if ((d=="1")|(d=="2")):
                            d=d
                        elif (d=="3"):
                            d="1"
                        elif (d=="4"):
                            d="2"
                        else:
                            d="0"
                        word =  ''.join(word + (d * multiply))

                #greater than 16
                else:
                    divide = int(len(extracted_numbers[0])/16)
                    for k in range(0,len(extracted_numbers[0]),divide):
                        d = str(max(int(extracted_numbers[0][i])for i in range(k,k+divide)))
                        if ((d=="1")|(d=="2")):
                            d=d
                        elif (d=="3"):
                            d="1"
                        elif (d=="4"):
                            d="2"
                        else:
                            d="0"
                        word =  ''.join(word + d)
                word_list = [word]

            #if it can't be devide by 4
            else:
                print("error")
                
            numbers.extend(word_list)
    return numbers

# 測試用
if __name__ == "__main__":
    file_path = "v2/data/level 6~7/song1"  # 這裡請換成你的.tja檔案路徑
    result = parse_tja_file(file_path)
    print(type(result))

