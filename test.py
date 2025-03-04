import re

extracted_numbers = ["3000000011111010"]
word= ""
            #if it is 16 numbers
if (extracted_numbers==[]):
    extracted_numbers = ["0"*16]

#if it can be devide by 4 and not 16 numbers
elif ((len(extracted_numbers[0])%4)==0) :
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

print(word_list)