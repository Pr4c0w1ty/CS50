#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Check for correct number of command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Check if key is a non-negative integer
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Convert key from string to integer
    int key = atoi(argv[1]);

    // Get plaintext from user
    string plaintext = get_string("plaintext: ");

    // Initialize cipher string with the same length as plaintext
    string cipher = plaintext;

    // Iterate over each character in plaintext
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        // Check if character is alphabetic
        if (isalpha(plaintext[i]))
        {
            // Determine whether character is upper or lower case
            char base = isupper(plaintext[i]) ? 'A' : 'a';

            // Apply Caesar cipher formula
            cipher[i] = (plaintext[i] - base + key) % 26 + base;
        }
        else
        {
            // If character is non-alphabetic, keep it unchanged in the cipher
            cipher[i] = plaintext[i];
        }
    }

    // Print ciphertext
    printf("ciphertext: %s\n", cipher);

    return 0;
}
