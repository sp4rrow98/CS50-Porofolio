#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Check if argv[1] is number
    
    if (argc != 2 && !isdigit(argv[1]))
    {
        printf("Only give one argument, also it needs to be a digit.\nExample : ./caesar 5\n");
        return 1;
    }
    
    int key = atoi(argv[1]);
    
    string s = get_string("Plaintext: \n");
    
    printf("ciphertext: ");
    for (int i = 0, j = strlen(s); i < j; i++)
    {
        if (islower(s[i]))
        {
            printf("%c", 'a' + (s[i] - 'a' + key) % 26);
        }
        else if (isupper(s[i]))
        {
            printf("%c", 'A' + (s[i] - 'A' + key) % 26);
        }
        else
        {
            printf("%c", s[i]);
        }
    }
    printf("\n");
}
