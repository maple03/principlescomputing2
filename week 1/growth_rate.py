"""
Example comparisons of growth rates
"""

import simpleplot
import math

def f(n):
    """
    A test function
    """
    return 1/2 * n ** 2 - 5 * n + 20

def g(n):
    """
    A test function
    """
    return n * math.log(n)
#    return 1
#    return n ** 2
#    return n ** 3

def make_plot(fun1, fun2, plot_length):
    """
    Create a plot relating the growth of fun1 vs. fun2
    """
    answer = []
    for index in range(10, plot_length):
        answer.append([index, fun1(index) / float(fun2(index))])
    simpleplot.plot_lines("Growth rate comparison", 300, 300, "n", "f(n)/g(n)", [answer])
    
# create an example plot    
make_plot(f, g, 20000)