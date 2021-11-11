#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    
    for (int i = 0; i < height ; i++)
    {
        for (int j = (height - i); j > 1; j--) 
        {
            printf(" ");
        }
        
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        
        for (int l = 0; l < 2; l++)
        {
            printf(" ");
        }
        
        for (int m = 0; m < i + 1; m++)
        {
            printf("#");
        }
        
        printf("\n");
    }
}
