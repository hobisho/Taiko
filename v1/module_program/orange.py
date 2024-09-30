class sheet: #譜
  def __init__(self, parent):
    self.parent = parent #父項 (歌曲)
    self.data = {} #此譜資料值(ex. 難度)
    self.noteList = [] #每行的音符
    return
  
  def setData(self, name, value): #如其名
    self.data[name] = value
  
  def appendNote(self, value): #如其名
    self.noteList.append(value)

  def toString(self): #轉換成字串
    result = []
    for key in self.parent.data.keys(): #加入父項屬性(ex. 曲名)
      result.append( f"{key}:{self.parent.data[key]}" )
    
    result.append('')

    for key in self.data.keys(): #加入每行音符
      result.append( f"{key}:{self.data[key]}" )
    for note in self.noteList:
      result.append( f"{note}," )
    
    result_str = ''

    for line in result: #加入分行
      result_str += f"{line}\n"
    
    return result_str
  
  def toFile(self, filepath): #匯出成檔案
    f = open(filepath, "w", encoding="utf-8")
    f.write( self.toString() )
    f.close()


class taiko: #歌曲
  def __init__(self, filepath): #arg: 檔案路徑
    f = open(filepath, 'r', encoding="utf-8") #檔案限用 UTF8
    self.data = {} #歌曲屬性
    self.source = f.read() #原檔案
    self.splited = self.source.split('\n') #分行後資料
    self.sheets = [] #譜列表

    state = 'header' #讀取狀態 歌曲屬性、譜
    sheetIndex = 0 #目前存取譜的Index
    
    for line in self.splited: #讀取每一行
      if not len(line): #沒東西 下一行
        continue

      if line.startswith('COURSE'): #COURSE 屬性就切到譜或下一張譜並加入
        self.sheets.append( sheet(self) )
        if state == 'header':
          state = 'game'
        else:
          sheetIndex += 1
          

      if line[0].isalpha(): #如果是字母
        splitIndex = line.find(':') #切屬性 name, value
        name = line[0:splitIndex]
        value = line[splitIndex+1:]

        if state == 'header': #正在存取歌曲屬性
          self.data[name] = value
        
        else: #將屬性加入到譜
          self.sheets[sheetIndex].setData(name, value)

      if line[0].isnumeric(): #如果是數字
        if not len(self.sheets): #不是正在存取譜就終止
          print("讀取失敗 終止")
          return
        
        result = ''

        if len(line) == 13:
          result = f"{line[0:3]}0{line[3:6]}0{line[6:9]}0{line[9:]}0"

        elif len(line) < 18: #將長度加長至16
          num = (16 // (len(line) - 1)) - 1 #需要填入幾個0
          for char in line:
            if char == ',':
              break
          
            result += char if int(char) < 3 else str(int(char) - 2) #3 -> 1 4 -> 2
            for i in range(num): #塞空節拍
              result += '0'

        else: #縮短至16
          index = 0
          num = ((len(line) - 1) // 16)
          while index < len(line):
            result += line[index]
            index += num

        self.sheets[sheetIndex].appendNote(result)
  
  def toString(self): #轉換成字串
    result = []
    for key in self.data.keys(): #歌曲屬性
      result.append( f"{key}:{self.data[key]}" )
    
    result.append('')

    for sheet in self.sheets: #譜屬性
      for key in sheet.data.keys():
        result.append( f"{key}:{sheet.data[key]}" )
      for note in sheet.noteList:
        result.append( f"{note}," )
      result.append('')
    
    result_str = ''

    for line in result:
      result_str += f"{line}\n"
    
    return result_str

  def toFile(self, filepath): #轉檔案
    f = open(filepath, "w", encoding="utf-8")
    f.write( self.toString() )
    f.close()