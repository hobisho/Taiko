import numpy as np

label = [1,2,3]
label = np.array(label,dtype=np.uint8)
a=label.tobytes()
print(a)
# k= np.fromstring(a,dtype=int)
# print(k)
