from itertools import chain

def expand_string(s: str) -> str:
    a =""
    for d in s:
        if (d=="3"):
            d="1"
        a =  ''.join(a +d * (3) )
    return a

# 測試
input_string = "0130"
output_string = expand_string(input_string)
print(output_string)  # 預期輸出：000111222000