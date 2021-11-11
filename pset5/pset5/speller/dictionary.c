// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include "dictionary.h"
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = LENGTH * 2 + 1;

// Hash table
node *table[N];

// Count words
int count_words;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index;
    index = hash(word);
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash = 31 * hash + tolower(word[i]);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    // OPEN FILE
    FILE *file = fopen(dictionary, "r");

    // ERROR CHECK
    if (file == NULL)
    {
        return false;
    }

    // COPY WORDS
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        else
        {
            strcpy(n->word, word);
            n->next = NULL;
            int index = hash(n->word);
            if (table[index] == NULL)
            {
                table[index] = n;
            }
            else
            {
                n->next = table[index];
                table[index] = n;

            }
            count_words++;
        }

    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{

    return count_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *cursor = NULL;
    node *tmp = NULL;
    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        while (cursor != NULL)
        {
            tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
