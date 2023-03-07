def my_pow(n, e, p):
    str = ""
    while e > 0:
        if e % 2 == 1:
            str += "1"
            e = (e - 1) >> 1
        else:
            str += "0"
            e = e >> 1
    sol = 1
    for i in range(len(str)):
        # print(i, end= ", ")
        # print(str[len(str) - 1 - i] == '0')
        sol = sol * sol
        sol = sol % p
        if str[len(str) - 1 - i] == '1':
            sol = sol * n
        sol = sol % p
    return sol


file = open("output.txt", "r")
data = file.readlines()
# for line in enumerate(data):
#     print(line)
p = int(data[0][4:])
k = (p - 1) >> 1
size = len(data[2])
matrix = data[2][8:size - 2].split(", ")
# print(len(matrix))
arr = []
for i in range(len(matrix)):
    arr.append(int(matrix[i]))
number = 0
for i in range(len(matrix)):
    if pow(arr[i], k, p) == 1:
        number = arr[i]
        break
print("solution is:")
d = (p + 1) >> 2
x = my_pow(number, d, p)
print(number)
print(x)
print(pow(x, 2, p))
file.close()