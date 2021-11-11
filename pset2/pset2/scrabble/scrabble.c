#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

int words(string text);

int letters(string text);

int grade_text(string text);

int sentences(string text);

int main(void)
{
    // Get the text.
    string text = get_string("Text: ");
    // 
    // Get text lenght

    printf("Words:%i \n", words(text));
    printf("Sentences:%i \n", sentences(text));
    printf("Letters:%i \n", letters(text));
    //

    // Print grade level.
    int grade = grade_text(text);
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 16 && grade > 1)
    {
        printf("Grade %i\n", grade);
    }
    else
    {
        printf("Before Grade 1\n");
    }
    //
}

// Functions :

int letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];
        if (isalpha(c))
        {
            letters++;
        }

    }
    return letters;
}

int words(string text)
{
    int words = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];
        if (c == ' ')
        {
            words++;
        }
    }
    return words + 1;
}

int sentences(string text)
{
    int sentence = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];
        if (c == '.' || c == '!' || c == '?')
        {
            sentence++;
        }
    }
    return sentence;
}

int grade_text(string text)
{
    int grade = 0;
    return grade;
}