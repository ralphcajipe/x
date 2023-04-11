// Program to print adjacent pyramid of blocks
// Left-aligned and right-aligned
// Height is based on user input (between 1 and 8, inclusive)

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    // Keep doing this prompt while user input is < 1 or > 8
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // For each row
    for (int i = 0; i < height; i++)
    {
        // <-Left side
        // On left side for each line, print a space before a brick
        for (int j = 1; j < height - i; j++)
        {
            printf(" ");
        }

        // On left side for each line, print a brick
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }

        // Middle
        // Print two spaces in the middle to separate left and right pyramids
        printf("  ");

        // ->Right side
        // On right side for each line, print a brick
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }

        // Move to next row
        printf("#\n");
    }
}