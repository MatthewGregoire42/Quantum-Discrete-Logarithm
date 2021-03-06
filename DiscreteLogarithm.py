from numpy import log, sqrt, floor, pi, arange
from random import randint, random
from algorithm import oracle

# def oracle(a, b, N):
#     r = calculate_order(a, N)
#     power = 1
#     while (a**power) % N != b:
#         power += 1
#     HB = 0
#     if (r/2 <= power):
#         HB = 1
#     correct = random()
#     if correct <= 0.6:
#         return HB
#     else:
#         return (HB + 1) % 2

e = 1/pi   # Maximum epsilon from the Magic Box paper.

def calculate_order(a, n):
    power = 1
    curr = a
    while (curr != 1):
        curr = (curr * a) % n
        power += 1
    return power

'''
   Determines the most significant bit of an integer c
   @param c: Base
   @param n: Modulus
   @return: 1 or -1
'''
def n1(c, n):
    val = -1

    if c % n >= (n / 2):
        val = 1
        
    return val

'''
   Decides which 'guess' best fits with the output of the oracle using cross correlation.
   @param G: Base of the logarithm.
   @param X: Power of the logarithm.
   @param n: Modulus.
   @param l: Lag of cross correlation - refers to how far the series are offset.
   @param d: The probability that the estimation will be incorrect.

   * Assumes that epsilon is already known (P. 106) *
    
   Used while loops in place of for loops because Python's
   range function does not use floating point numbers and I
   didnt want to introduce logical errors by rounding off
   numbers using floor() or int(). 
'''
def EstimateCrossCorrelation(G, X, n, l, d, period):
    total = 0  # Called 'sum' in algorithm

    # Compute the number of trials
    m = int(round(2 / (sqrt(d) * e)))
    # print("m:", m)

    # Compute estimate
    for trial in range(m):
        # print("Trial:", trial)
        t = randint(1, n)
        output = oracle(G, X, n)  # Oracle(base, LHS, mod)

        if output == 0:
            output = -1
        
        total = total + (output*(X * (G ** period)) * n1(t + l, n))

    return (total / m)

'''
   Main algorithm for computing the logarithm.
   @param G: Base of a the logarithm.
   @param X: Power of the logarithm.
   @param n: Modulus

   * Assumes that epsilon was calculated beforehand *

   Used while loops in place of for loops because Python's
   range function does not use floating point numbers and I
   didnt want to introduce logical errors by rounding off
   numbers using floor() or int(). 
'''
def Logarithm(G, X, n):
    step = (n * e)          # Compute step
    print("Step:", step)
    l = int(log(n)/log(2))  # Number of iterations
    d = round((l / 4), 10)  # Limit on probability error

    period = calculate_order(G, n)
    print("Period:", period)

    # Repeat until logarithm is found.
    while True:
        # Make initial guess. 
        for c in arange(0, n-1+step, step):
            print("c:", c)
            
            # Refine guess.
            for i in range(l-1, -1, -1):
                print("i:", i)
                Xi = (X ** (2**i)) % n

                if (EstimateCrossCorrelation(G, Xi, n, c/2, d, period)
                    > EstimateCrossCorrelation(G, Xi, n, c/2 + n/2, d, period)):
                    c = (c/2) % period
                else:
                    c = (c/2 + n/2) % period
                print("c:", c)
            
            print("Result:", int(floor(c)))
            potential = int(floor(c))
            if ((G ** potential) % n) == X:
                return potential

# Should return 3
print(Logarithm(7, 13, 15))

# Should return 11, but way too slow to run
# print(Logarithm(7, 20, 31))