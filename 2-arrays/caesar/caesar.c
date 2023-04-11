// Caesar's cipher algorithm

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Function prototypes
bool only_digits(string text);
char rotate(char plaintext[], int kposition);

int main(int argc, string argv[])
{

    /* Counting Command-Line Arguments:
     * Check if program was run with just one command-line argument and
     * Check if every character in argv[1] is a digit
     */
    if (argc != 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

    if (!only_digits(argv[1]))
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

    // Using the Key:
    // Convert argv[1] CLA to an int
    int kposition = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // Function call:
    // Rotate each character in the plaintext by k position secret key:
    rotate(plaintext, kposition);

    printf("ciphertext: %s\n", plaintext);
}

// Function definitions

// Checking the Key:
// Check if every character in argv[1] CLA is a digit
bool only_digits(string text)
{
    bool isDigit = false;

    for (int i = 0; text[i]; i++)
    {
        if (isdigit(text[i]))
        {
            isDigit = true;
        }
        else if (!isdigit(text[i]))
        {
            isDigit = false;
            return 1;
        }
    }
    return isDigit;
}

// Using the Key:
// Rotate each character in the plaintext by k secret key:
char rotate(char plaintext[], int kposition)
{
    int k = 0;

    while (plaintext[k])
    {
        if (isupper(plaintext[k]))
        {
            plaintext[k] = ((plaintext[k] - 'A' + kposition) % 26) + 'A';
        }
        else if (islower(plaintext[k]))
        {
            plaintext[k] = ((plaintext[k] - 'a' + kposition) % 26) + 'a';
        }
        else if (isalpha(plaintext[k]))
        {
            return false;
        }
        k++;
    }
    return k;
}