#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // Ask for the amount of money
    float cash;
    do
    {
        cash = get_float("Amount: ");
    }
    while (cash < 0);
    //
    // Convert in pennies
    int pennies = round(cash * 100);
    printf("%i\n", pennies);
    //
    // Define change
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    int coins = 0;
    //
    // Calculate coins
    while (pennies >= 25) 
    {
        pennies = pennies - quarter;
        coins++;
    }
    while (pennies >= 10) 
    {
        pennies = pennies - dime;
        coins++;
    }
    while (pennies >= 5) 
    {
        pennies = pennies - nickel;
        coins++;
    }
    while (pennies >= penny) 
    {
        pennies = pennies - penny;
        coins++;
    }

    printf("%i\n", coins);
}
