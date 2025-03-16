#include <stdio.h>
#include <stdlib.h>

int main()
{
    int X, a, b, C;
    scanf("%d", &X);
    a = X/100;
    X = X-100*a;
    b = X/10;
    X = X-10*b;
    C = X;
    printf("%d+%d+%d = %d\n", a, b, c, a+b+c);
    printf("%d*%d*%d = %d\n", a, b, c, a*b*c);
    return 0;
}