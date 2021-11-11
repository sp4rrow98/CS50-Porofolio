#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

int main(void)
{

    string text = get_string("Text: ");
    int text_length = strlen(text);

    int words = 0;
    for (int i = 0; i < text_length; i++)
    {
        char c = text[i];
        if (c == ' ')
        {
            words++;
        }
    }
    int word_final = words + 1;

    int sentences = 0;
    for (int i = 0; i < text_length; i++)
    {
        char c = text[i];
        if (c == '.' || c == '!' || c == '?')
        {
            sentences++;
        }
    }
    int sentences_final = sentences;

    int letters = 0;
    for (int i = 0; i < text_length; i++)
    {
        char c = text[i];
        if (isalpha(c))
        {
            letters++;
        }
    }
    int letters_final = letters;

    float L = (letters_final / (float) word_final) * 100;
    float S = (sentences_final / (float) word_final) * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    
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