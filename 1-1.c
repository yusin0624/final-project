#include <stdio.h>
#include <stdlib.h>

int main()
{
    int x, a, b, c;
    scanf("%d", &x);
    a = x/100;
    x = x-100*a;
    b = x/10;
    x = x-10*b;
    c = x;
    printf("%d+%d+%d = %d\n", a, b, c, a+b+c);
    printf("%d*%d*%d = %d\n", a, b, c, a*b*c);
    return 0;
}