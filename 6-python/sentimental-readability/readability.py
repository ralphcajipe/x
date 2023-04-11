# Readability in Python

from cs50 import get_string

# Get text input
text = get_string("Text: ")

# Initialize letters, words, and sentences as zero
letters = 0
words = 0
sentences = 0

# Count letters (characters)
for character in text:
    if character.isalpha():
        letters += 1

# Count words (to check whether a character is whitespace)
words = text.count(" ") + 1

# Count sentences using boundary detection (. ? !)
sentences = text.count(".") + text.count("?") + text.count("!")

# Put formula together to compute for Coleman-Liau index
L = letters / words * 100
S = sentences / words * 100
index = round(0.0588 * L - 0.296 * S - 15.8)

# Print grade level
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")