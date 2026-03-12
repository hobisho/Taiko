import os
import re
import shutil
from itertools import chain
from select_song.sorting_folder import rename_files_in_folders

def parse_tja_file(folder_path:str, footstep:int=48)->list:
    file_path = None
    
    # 確保輸出資料夾存在
    for file in os.listdir(folder_path):
        if file.endswith(".tja"):
            file_path = os.path.join(folder_path, file)
            break
        
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    start = False
    oni = False
    numbers = []
    
    for line in lines:
        line = line.strip()
        if line.upper() == "COURSE:ONI":
            oni = True
        
        if (line.upper() == "#START") & oni:
            start = True
            continue
        
        if (line.upper() == "#END") & start:
            break
        
        if (start & (re.search(r',', line)!= None)):
            word = ""
            extracted_numbers = re.findall(r'(\d+),', line)  # 輸入數字字串
            
            #if it is footstep numbers
            if (extracted_numbers==[]):
                word_list = ["0"*footstep]
            
            # elif (len(extracted_numbers[0])==16):
            #     word_list = extracted_numbers

            #if it can be devide by 4 and not footstep numbers
            elif(((len(extracted_numbers[0])%4)==0) | ((len(extracted_numbers[0]))==1) | ((len(extracted_numbers[0]))==2) | ((len(extracted_numbers[0])%3)==0)):
                #small than footstep
                if(len(extracted_numbers[0])<footstep):
                    if ((len(extracted_numbers[0])%32)==0):
                        print("32 can't expend to 48")
                        return None
                    multiply = int(footstep/len(extracted_numbers[0]))
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

                #greater than footstep
                else:
                    print("greater than footstep")
                    if (len(extracted_numbers[0])%footstep!=0):
                        print(f"{len(extracted_numbers[0])} can't be {footstep}")
                        return None
                    divide = int(len(extracted_numbers[0])/footstep)
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
                print(f"song can't be {footstep}")
                return None
                
            numbers.extend(word_list)
    
    #刪除前後的0
    # pop = 0
    # for i in range(len(numbers),0,-1):
    #     if (numbers[i-1]=="0000000000000000"):
    #         numbers.pop(i-1)
    #     else:
    #         break
    # for i in range(len(numbers)):
    #     if (numbers[i]=="0000000000000000"):
    #         pop = pop+1
    #     else:
    #         break
    # for i in range(pop):
    #     numbers.pop(0)
    return numbers


def extract_level_value(folder_path):
    # 找出資料夾內的 .tja 檔案（不考慮最前面的數字）
    tja_file_path = None
    for file in os.listdir(folder_path):
        if file.endswith(".tja"):
            tja_file_path = os.path.join(folder_path, file)
            break
    
    if not tja_file_path:
        print(f"未找到TJA檔於: {folder_path}")
        print(f"{os.path.basename(folder_path)} 資料夾內的檔案:")
        for file in os.listdir(folder_path):
            print(f"  - {file}")
        return None
    
    with open(tja_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # 使用正則表達式提取 LEVEL: 後的數值BPMCHANGE
    oni_match = re.search(r'COURSE:\s*Oni', content, re.IGNORECASE)

    if not oni_match:
        return 0

    after_oni = content[oni_match.end():]
    match = re.search(r'LEVEL:\s*(\d+)', after_oni, re.IGNORECASE)

    bpmchange = re.search(r'BPMCHANGE', after_oni, re.IGNORECASE)
    measure = re.search(r'MEASURE', after_oni, re.IGNORECASE)
    output = parse_tja_file(folder_path)


    if bpmchange:
        return None
    elif measure:
        return None
    elif output is None or output == []:
        return None
    elif match:
        return int(match.group(1))
    else:
        print(f"未找到 COURSE:Oni 後的 LEVEL 數值於: {tja_file_path}")
        return None

def copy_folder_if_level_in_range(root_folder, destination_folder):
    # 確保目標資料夾存在
    os.makedirs(destination_folder, exist_ok=True)
    
    # 遍歷主資料夾內的所有子資料夾
    for subfolder in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, subfolder)
        if os.path.isdir(subfolder_path):
            level_value = extract_level_value(subfolder_path)
            if level_value is not None and 5 <= level_value <= 9:
                dest_path = os.path.join(destination_folder, subfolder)
                shutil.copytree(subfolder_path, dest_path, dirs_exist_ok=True)
                print(f"已複製 {subfolder} 到 {dest_path}")

if __name__ == "__main__":
    root_folder = "Taiko-switch"
    for subfolder in os.listdir(root_folder):
        root_folder_path = os.path.join(root_folder, subfolder)  # 請修改為你的資料夾路徑
        destination_folder_path = "v2/data/oni"  # 請修改為你的目標資料夾路徑
        copy_folder_if_level_in_range(root_folder_path, destination_folder_path)
    rename_files_in_folders(destination_folder_path)