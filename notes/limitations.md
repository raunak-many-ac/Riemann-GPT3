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


## Range input in $\eta(\zeta(a+ix), L, R))$

We know $\zeta(-2+i0) = 0$ and $\zeta(-0.5+i14.134725..) = 0$

So for $\eta(0, -2.5, 10))$: - 
$(-2+i0)$ and $(-0.5+i14.134725...)$ both are valid outputs

Because we can't give any predict strict range in which the Riemann Zeta value exists specially in critical region.

There could be a Riemann Zeta zero in range [0,0.5) or (0.5, 1]
So, for any Riemann Zeta Zero on critical axis we can't give any strict range with only 1 feasible output (due to probablity of multiple feasible outcomes)

Even though if there aren't any Riemann Zeta zeroes in [0,0.5) or (0.5, 1] we still have a lot of them on critical axis (real = 0.5).


