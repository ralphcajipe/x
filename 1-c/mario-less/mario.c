// Program to print right-aligned pyramid of blocks
// Height is based on user input (between 1 and 8, inclusive).

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    // do this while user input is < 1 or > 8
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // For each row
    for (int i = 0; i < height; i++)
    {
        // First, for each line, print a space
        for (int j = 1; j < height - i; j++)
        {
            printf(" ");
        }

        // Second, for each line, print a hash #
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }

        // Move to next row
        printf("#\n");
    }
}