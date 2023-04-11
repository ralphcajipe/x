// A programs that prompts the user for their name
// and then prints `hello, so-and-so`,
// where `so-and-so` is their actual name.

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string name = get_string("What's your name? ");
    printf("hello, %s\n", name);
}