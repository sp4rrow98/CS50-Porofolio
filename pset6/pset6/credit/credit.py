import sys

number = input("Number: ")
s1 = 0
s2 = 0

for i in number[-2::-2]:
    if ((int(i) * 2) > 9):
        s1 = ((int(i) * 2) % 10) + 1 + s1
    else:
        s1 = (int(i) * 2) + s1
for j in number[-1::-2]:
    s2 = int(j) + s2

total = s1 + s2

if (total % 10 == 0):
    if (len(number) == 15 and number[:2] == "34" or number[:2] == "37"):
        print("AMEX")
    elif (len(number) == 16 and number[:2] == "51" or number[:2] == "52" or number[:2] == "53" or number[:2] == "54" or number[:2] == "55"):
        print("MASTERCARD")
    elif (len(number) == 13 or len(number) == 16 and number[0] == '4'):
        print("VISA")
    else:
        sys.exit("INVALID")
else:
    sys.exit("INVALID")
    