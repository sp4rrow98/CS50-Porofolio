import string
text = input("text: ")
letters = 0
words = 1
sentences = 0
for i in text:
    if (i.isalpha()):
        letters += 1
    if (i == ' '):
        words += 1
    if (i == '.' or i == '?' or i == '!'):
        sentences += 1

L = letters / words * 100
S = sentences / words * 100
index = 0.0588 * L - 0.296 * S - 15.8
index = round(index)

if (index < 1):
    print("Before Grade 1")
elif (index >= 16):
    print("Grade 16+")
else:
    print(f"Grade {index}")
