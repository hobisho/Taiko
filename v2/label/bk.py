def break_str(string_list):
    out=[]
    for string in string_list:
        for count in range (16):
            out.append(string[count])
    return out

if __name__ == '__main__':
    a=['2200000000220022','0000000000000000']
    break_str(a)