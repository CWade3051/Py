"""

IDLE Cython Demo

Be sure that your version of Cython has "reload_support" for pyximport.
This demo will still work, but "Import/Reload Cython Script" may fail.
Visit http://cython.org for more information.

This demonstration shows Cython being used with IDLE.
It performs a simple benchmark on a naive implementation of
the Fibonacci sequence.


Pressing Ctrl+E restarts the shell and performs a
    "from cython_demo import *"

Pressing Ctrl+Shift+E effectively does
    "import cython_demo" and, if needed, "reload(cython_demo)"
without restarting the shell.
    
"""


from __future__ import division
import time

reps = 1000      # Repetitions
term = 17        # Fibonacci Term

cpdef int fib(int n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


tic = time.time()
for x in range(reps):
    a = fib(term)
print('Fibonacci %ith term: %i' % (term, a))
toc = time.time()

print('Elapsed time for Cython with types: %f' % (toc - tic))


import timeit
setup = """
def fib(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
"""

ti = timeit.Timer('fib(%i)' % term, setup=setup)
pt = ti.timeit(reps)

print('Elapsed time for Python: %f' % pt)
print('Speedup: %fx' %  (pt / (toc - tic)))
    


