#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

float L_counter(string txt);
float S_counter(string txt);

int main(void)
{
    int letters = 0;
    string txt = get_string("Text: ");

    float L = L_counter(txt);
    float S = S_counter(txt);
    // printf("l %f\n", L);
    // printf("s %f\n", S);
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int rounded_number = round(index);

    if (rounded_number < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (rounded_number > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", rounded_number);
    }
}

float L_counter(string txt)
{
    float LLtcounter = 0;
    float LWdcounter = 1;
    for (int i = 0, n = strlen(txt); i < n; i++)
    {
        if (isalpha(txt[i]))
        {
            LLtcounter++;
        }
        else if (txt[i] == ' ')
        {
            LWdcounter++;
        }
    }
    // printf("LLtcounter %f\n", LLtcounter);
    // printf("LWdcounter %f\n", LWdcounter);
    float L = (LLtcounter / LWdcounter) * 100;

    return L;
}

float S_counter(string txt)
{

    float SWdcounter = 1;
    float SStcounter = 0;
    for (int i = 0, n = strlen(txt); i < n; i++)
    {

        if (txt[i] == ' ')
        {
            SWdcounter++;
        }
        else if (txt[i] == '.' || txt[i] == '!' || txt[i] == '?')
        {
            SStcounter++;
        }
    }
    // printf("SWdcounter %f\n", SWdcounter);
    // printf("SStcounter %f\n", SStcounter);
    float S = (SStcounter / SWdcounter) * 100;
    return S;
}
