
from numpy import exp
def f(x):
    return exp(pow(x,2))
def trapezoid(a,b):
    return(b-a)*(f(a)+f(b))/2#梯形公式
def simpson(a,b):
    return(b-a)*(f(a)+4*f((a+b)/2)+f(b))/6#辛普森公式
def cotes(a,b):
    h=(b-a)/4
    x0,x1,x2,x3,x4=a,a+h,a+2*h,a+3*h,a+4*h
    return(b-a)*(7*f(x0)+32*f(x1)+12*f(x2)+32*f(x3)+7*f(x4))/90
print("trapezoid:",trapezoid(0,2))
print("simpson:",simpson(0,2))
print("cotes:",cotes(0,2))

