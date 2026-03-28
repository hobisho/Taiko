a= [7,8,5,5]
b= [5,5,5,6]

k = [x - y for x, y in zip(a, b)]

print(k.index(max(k)))