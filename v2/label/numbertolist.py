import numpy as np


def numbertolist(number):
    a=np.zeros(4,dtype=int)
    a[number+1]=1
    return a



if __name__ == "__main__":
    print(numbertolist(1))