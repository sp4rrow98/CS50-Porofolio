from cs50 import get_float, get_int
import math

cash = -1
while cash < 0:
    cash = get_float("Amount: ")
cash = cash * 100
cash = math.floor(cash)

quarters = cash // 25
dimes = (cash % 25) // 10
nickels = ((cash % 25) % 10) // 5
pennies = (((cash % 25) % 10) % 5) // 1
coins = quarters + dimes + nickels + pennies

print(coins)

