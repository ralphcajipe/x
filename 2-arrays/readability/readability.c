// Readability test using Coleman-Liau index algorithm

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

// Function prototypes
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Texts to input
    string text = get_string("Text: ");

    // Let formula work with function calls
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Putting it All Together: Compute Coleman-Liau index
    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

// Function definitions

// Count letters (characters)
int count_letters(string text)
{
    int letterCount = 0;
    int n = strlen(text);

    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letterCount++;
        }
    }
    return letterCount;
}

// Count words (to check whether a character is whitespace)
int count_words(string text)
{
    int spaceCount = 0;
    int n = strlen(text);

    for (int i = 0; i < n; i++)
    {
        if (isspace(text[i]) > 0)
        {
            spaceCount++;
        }
    }
    return spaceCount + 1;
}

// Count sentences using boundary detection (. ! ?)
int count_sentences(string text)
{
    int sentenceCounter = 0;
    int n = strlen(text);

    for (int i = 0; i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentenceCounter++;
        }
    }
    return sentenceCounter;
}