#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define block_size 512

int main(int argc, char *argv[])
{
    // open the card
    FILE *card = fopen("card.raw", "r");
    
    // check for usage error
    if (argc != 2)
    {
        printf("%s\n", "Usage : ./recover card.raw");
        return 1;
    }
    
    // buffer
    unsigned char buffer[block_size];
    
    // count, name and check photos
    int jpg = 0;
    int count_filename = 0;
    FILE *picture = NULL;
    
    // read the card
    while(fread(buffer, block_size, 1, card))
    {
        if (buffer[0] == 0xff & buffer[1] == 0xd8 & buffer[2] == 0xff & (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpg == 1)
            {
                fclose(picture);
            }
            else
            {
                jpg = 1;
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", count_filename);
            picture = fopen(filename, "a");
            count_filename++;
        }
        if (jpg == 1) 
        {
            fwrite(buffer, block_size, 1, picture);
        }
    }
    
    fclose(card);
    fclose(picture);

    return 0;
    
}