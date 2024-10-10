from cs50 import get_int
from math import log10

number = get_int("give number: ")
cksum = 0
temp = number
digits = int(log10(number)) + 1

temp2 = number
number_starts = temp2

for i in range(digits):
    last_dig = number % 10
    number //= 10
    if i % 2 == 0:
        cksum += last_dig
    else:
        double = 2 * last_dig
        cksum += (double % 10) + (double // 10)


while temp2 > 100:
    temp2 //= 10
    number_starts = temp2

if cksum % 10 == 0:
    if digits == 15 and (number_starts == 34 or number_starts == 37):
        print("AMEX")
    elif digits == 16 and number_starts in range(51, 56):
        print("MASTERCARD")
    elif (digits == 13 or digits == 16) and str(number_starts).startswith('4'):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")
