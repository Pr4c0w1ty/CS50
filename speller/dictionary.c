// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;
unsigned int word_count = 0;
// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    {
        // Create a lowercased copy of the word for case-insensitive comparison
        char temp[LENGTH + 1];
        int len = strlen(word);
        for (int i = 0; i < len; ++i)
        {
            temp[i] = tolower(word[i]);
        }
        temp[len] = '\0';

        // Get the hash index
        unsigned int index = hash(temp);

        // Traverse the linked list at the hash index
        node *cursor = table[index];
        while (cursor != NULL)
        {
            if (strcasecmp(cursor->word, temp) == 0)
            {
                return true; // Word found
            }
            cursor = cursor->next;
        }
        return false; // Word not found
    }
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value = (hash_value << 2) ^
                     (unsigned int) tolower(word[i]); // Apply tolower to ensure case insensitivity
    }
    return hash_value % N;
}

bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) == 1)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(file);
            return false;
        }
        strcpy(new_node->word, word);
        unsigned int index = hash(word);
        new_node->next = table[index];
        table[index] = new_node;
        word_count++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    {
        // Iterate over each bucket
        for (int i = 0; i < N; i++)
        {
            node *cursor = table[i];

            // Traverse the linked list and free the nodes
            while (cursor != NULL)
            {
                node *temp = cursor;
                cursor = cursor->next;
                free(temp); // Free the current node
            }

            table[i] = NULL;
        }

        return true; // Return true to indicate success
    }
}
