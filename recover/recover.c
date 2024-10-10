#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card file
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("File could not be opened.\n");
        return 2;
    }

    // Create a buffer for a 512-byte block
    uint8_t buffer[512];
    char filename[8];
    FILE *img = NULL;   // File pointer for JPEG files
    int file_count = 0; // Counter for file names

    // Read through the card file until end of file
    while (fread(buffer, 512, 1, card) == 1)
    {
        // Check for JPEG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG file is already open, close it
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new filename and open a new JPEG file
            sprintf(filename, "%03i.jpg", file_count++);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create file %s.\n", filename);
                fclose(card);
                return 3;
            }
        }

        // If a JPEG has been found, write to it
        if (img != NULL)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    // Close any remaining open files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);

    return 0;
}
