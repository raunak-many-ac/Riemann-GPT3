#### For sake of this research I have presumed a hypothetical abstract function `Narayan-Riemann Inverse Zeta Function`:
$$
\displaystyle\eta(\zeta(x+iy), L, R) = x+iy
$$
where, $\zeta(x+iy)$ is Riemann's Zeta function and
$L < x < R$

We will train `gpt-3` to fit on understanding of the above mentioned `NRIZeta` function.

At the end of the training we will ask the gpt-3 trained model to give output for $\eta(0, 0, 1/2)$ and $\eta(0, 1/2, 1)$

If model's efficacy is high, value of above outputs will falsify Riemann's Hypothesis


#### Using `mpmath`
    For calculating zeta function values for given inputs
    For calculating ith zeta zeroes

### The model must be specifically specified to undestand the exclusion of input range
    We are trying to train the model to get understanding on the range output that it needs to give. For example: 
```
    Input:
    if we ask the model to find an input for R-Zeta function for which
    the value (evaluation) will be 0 but real part is in between range (-2, 1/2) i.e. 
    {
        "prompt": "find: 0, low: -2, high: 0.5"
    }

    Output:
        We know at critical axis (i.e, x + iy where x == 0.5) we can find "Zeta Zeroes" but 
        the model must not give this as an output because "low" and "high" are excluded range. 
```

#### We need to be more specific in terms of ranges when we are talking about Rzeta zeroes
    For an input like:
    {
        "prompt": "find: 0, low: 0, high: 0.5"
    }

* ### Boundation ranges
    We will assume the following for this:
    $$
    \zeta(x+iy)= w
    $$
    * #### Left-close range
        A range $(L, R)$ is left close to for input $x+iy$ if $$x-L < R - x$$
    * #### Right-close range
        A range $(L, R)$ is left close to for input $x+iy$ if $$x-L > R - x$$
     * #### Dispersed range
        A range $(L, R)$ is dispersed if it is just a random range enclosing the real part of expected input (i.e. $x$ here)

### Input diversity
    No Solution --> 25%
    Solution exists --> 75%
        - For same zeta value multiple solutions exist so we need multiple same zeta value inputs