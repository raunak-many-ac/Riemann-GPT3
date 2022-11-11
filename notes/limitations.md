## Precision
we are using python library mpmath which is precise till 15

## No Solution data points for training
For no solution dataset we need a range in which the solution to our assumed function:
$$
\displaystyle\eta(\zeta(x+iy), L, R) = x+iy
$$
doesn't exists.

Some of the examples are :- 
$$
\displaystyle\eta(\zeta(0+i0), 1, 2) = \phi
$$
    because, all zeroes are either on critical axis or are real negative even integers.
$$
\displaystyle\eta(\zeta(2+i3), 7, 20) = \phi
$$
     because, Riemann zeta...

By looking at graph of `ζ(a+ix)` where `a` is arbitrary constant we can find out of bound zones for inexistent solutions for $$\eta(\zeta(a+ix), L, R))$$