txt = input("Text: ")


def L_counter(txt):
    letter_count = sum(1 for char in txt if char.isalpha())
    word_count = sum(1 for char in txt if char == ' ') + 1
    L = (letter_count / word_count) * 100
    return L


def S_counter(txt):
    word_count = sum(1 for char in txt if char == ' ') + 1
    sentence_count = sum(1 for char in txt if char in '.!?')
    S = (sentence_count / word_count) * 100
    return S


L = L_counter(txt)
S = S_counter(txt)
print(L)
print(S)
index = 0.0588 * L - 0.296 * S - 15.8
rounded_index = round(index)

if rounded_index < 1:
    print("Before Grade 1")
elif rounded_index > 16:
    print("Grade 16+")
else:
    print(f"Grade {rounded_index}")
