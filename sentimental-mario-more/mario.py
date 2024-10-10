from cs50 import get_int


def geth(prompt, max_height):
    while True:
        try:
            h = get_int(prompt)
            if 1 <= h <= max_height:
                return h
            print(f"Please enter a positive integer no greater than {max_height}.")
        except ValueError:
            print("Please enter a valid integer.")


h = geth("Height: ", 8)

for i in range(1, h + 1):
    print(" " * (h - i), end="")
    print("#" * i, end="  ")
    print("#" * i)
