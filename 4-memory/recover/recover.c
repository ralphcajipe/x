// Recover

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

// Create a new type to store a byte of data
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check for invalid usage of command line arguments
    if (argc < 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Memory allocation
    BYTE *buffer = malloc(32 * sizeof(BYTE));

    if (buffer == NULL)
    {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Open memory card and read
    FILE *fileinput = fopen(argv[1], "r");

    // If the forensic image cannot be opened for reading
    if (fileinput == NULL)
    {
        printf("Invalid file!\n");
        return 1;
    }

    // Initialize file output
    FILE *fileoutput = NULL;

    // Assuming file is not open (false) by default
    bool open = false;

    // Image counter/updater
    int imagecounter = 0;

    // Max number of characters in a filename
    char filename[8];

    /* while loop:
     * Repeat reading until end of card - read every block from card.raw
     * To read 512 bytes into a buffer */
    while (fread(buffer, sizeof(BYTE), 32, fileinput) == 32)
    {
        // If file header is a match to a JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 &&
            buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (open)
            {
                fclose(fileoutput);
            }

            // Making a New JPEG
            sprintf(filename, "%03i.jpg", imagecounter);
            printf("%s\n", filename);

            // Write into memory card
            fileoutput = fopen(filename, "w");

            // If the forensic image cannot be opened for writing
            if (fileoutput == NULL)
            {
                printf("Can not create and write into file!\n");
                return 1;
            }

            fwrite(buffer, sizeof(BYTE), 32, fileoutput);
            open = true;
            imagecounter++;
        }
        else if (open)
        {
            fwrite(buffer, sizeof(BYTE), 32, fileoutput);
        }
    }

    // Free memory and properly close file input and file output
    free(buffer);
    fclose(fileinput);
    fclose(fileoutput);

    return 0;
}