from cs50 import get_int
height = 0
while height < 1 or height > 8:
    height = get_int("Height: ")

for i in range(height):
    sum_spaces = " " * (height - i - 1)
    sum_fill = i + 1
    print(sum_spaces + sum_fill * "#" + "  " + "#" * sum_fill)