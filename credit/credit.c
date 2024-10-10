#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long long number;
    number = get_long("give number: ");

    int cksum = 0;
    int number_starts;
    long long temp = number;
    for (int i = 0; number != 0; i++)
    {
        int last_dig = number % 10;
        number = number / 10;
        if (i % 2 == 0)
        {
            cksum += last_dig;
        }
        else
        {
            cksum += (2 * last_dig) % 10 + (2 * last_dig) / 10;
        }
    }
    // printf("%d", i);
    // printf("%d", cksum);
    // printf("%lld", temp);

    while (temp >= 100)
    {
        number_starts = temp / 10;
        temp /= 10;
    }
    // printf("%d", number_starts);
    if (cksum % 10 == 0)
    {
        if (i == 15 && (number_starts == 34 || number_starts == 37))
        {
            printf("AMEX\n");
        }
        else if (i == 16 && (number_starts == 51 || number_starts == 52 || number_starts == 53 ||
                             number_starts == 54 || number_starts == 55))
        {
            printf("MASTERCARD\n");
        }
        else if ((i == 16 || i == 13) &&
                 (number_starts == 40 || number_starts == 41 || number_starts == 42 ||
                  number_starts == 43 || number_starts == 44 || number_starts == 45 ||
                  number_starts == 46 || number_starts == 47 || number_starts == 48 ||
                  number_starts == 49))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
