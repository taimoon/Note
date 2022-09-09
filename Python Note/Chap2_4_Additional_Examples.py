"""
additional reference and exercise can be found on:
https://sicp.sourceacademy.org/chapters/1.3.4.html#ex_1.43
"""

def half_interval_method(f, a, b, h = 10**-6):
    if f(a) > 0 == f(b) > 0:
        raise Exception("half_interval_method: values are not of opposite")
    if f(a) > 0 and f(b) < 0:
        a, b = b, a # idiom: swapping values
    is_closed_enough = lambda x,y : abs(x-y) < h
    mid_point = lambda x,y : (x+y)/2
    test_value = 0
    while not is_closed_enough(a,b):
        test_value = f(mid_point(a,b))
        if test_value > 0:
            b = mid_point(a,b)
        elif test_value < 0:
            a = mid_point(a,b)
        else:
            return mid_point(a,b)
    return mid_point(a,b)

'''
A number x is called a fixed point of a function f if f(x) = x. For some functions f, 
we can locate the x such that
f(x) = f(f(x)) = f(f(f(x))) = ...
'''
def fix_point(f, init_guess, h = 10**-6):
	is_closed_enough = lambda x,y: abs(x - y) < h
	guess = init_guess
	while not is_closed_enough(guess , f(guess)):
		guess = f(guess)
	return guess

'''
find x for y^2 = x, and equivalently, y = x/y.
we want to find y such that f(y) = x/y = y; we're trying to locate the fix point of y = x/y
But it will oscillate thus there should be a code should prevent guess from changing too much
'''

def fix_sqrt(x):
	average = lambda x,y : (x+y)/2
	return fix_point(lambda y: average(y, x/y), 10**-6)

'''
Find the solution of x for x^x = 1000. Then
x = log(1000)/log(x) = f(x)
'''
def powerful_solution(y):
	from math import log
	return fix_point(lambda x: log(y)/log(x), y/2, 10**-6)
test_powerful_solution = lambda x: powerful_solution(x)**powerful_solution(x)
print(test_powerful_solution(1000))
print(test_powerful_solution(100))

'''
Newton transform method:
find the x for g(x) = 0. Then,

x_{n+1} = x_n - g(x_n)/g'(x_n)

equivalently,

f(x_n) = x_n - g(x_n)/g'(x_n)
f(x) = x - g(x)/g'(x)
It is a fixed point method
'''
def deriv(f, h = 10**-6):
    return lambda x: (f(x+h) - f(x)) / h

def fix_newton(f, init_guess, h = 10**-6):
	def newton_transform(g):
		return lambda x: x - g(x)/deriv(g,h)(x)

	return fix_point(newton_transform(f), init_guess, h)

# Find which y when y^2 - x = 0 <-> y = sqrt(x)
def newton_sqrt(x):
	return fix_newton(lambda y: y*y - x, 1.0)