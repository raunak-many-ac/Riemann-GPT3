# Here are the responsibilities of this file
# 1. From the dataset file "nonTrivialZetaZeroes.val" get all critical axis zeroes
# 2. generate some trivial zeroes
# 3. generate thousands of zeta function values with there ranges of inputs
#    then dump in the dataset file

import mpmath
import random
import numpy as np

import utils

CREATION_COUNT = 5
noOfZeroesOnCriticalAxisToGenerate = 5000
INFINITE = 999999
NEGATIVE_INFINITE = -INFINITE - 1
# mpmath.mp.prec = 53
mpmath.mp.pretty = True


# This function takes a dictionary input where every entry is like: 
# {<output value of Rzeta function>: <input value of Rzeta function>}
# Now this function should:
#     - generate bounded range for input value (exclusion of ranges)
#     - close range as well
def generateInputPrompts(zetaValue: mpmath.mpc, inputValue: mpmath.mpc, alsoGenerateOutOfBoundaryNoSolution: bool = False) -> dict:
    real: mpmath.mpf = inputValue.real
    # floorReal = mpmath.floor(real) if mpmath.floor(real) != 0 else mpmath.

    prompts = {}

    randomNumber: float = random.randrange(start=0, stop=1000) * random.random()
    low = real - randomNumber

    randomNumber = random.randrange(start=0, stop=1000) * random.random()
    high = real + randomNumber

    prompts[(zetaValue, low, high)] = inputValue

    # if alsoGenerateOutOfBoundaryNoSolution is True:
    #     prompts[(zetaValue, real - random.random(), real)] = "No Solution"
    #     prompts[(zetaValue, real, real + random.random())] = "No Solution"
        
    return prompts

def generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate):
    criticalLineZeroes = []
    noOfZeroesOnCriticalAxis = noOfZeroesOnCriticalAxisToGenerate
    i = 1
    while len(criticalLineZeroes) < noOfZeroesOnCriticalAxis:
        incrementBy = random.randrange(1, 1000)
        ithZero = mpmath.zetazero(i)
        criticalLineZeroes.append(ithZero)
        i += incrementBy

    dictionaryOfZetaZeroes = {}
    for zetazero in criticalLineZeroes:
        prompts: dict = generateInputPrompts(zetaValue=mpmath.mpmathify(0+0j), inputValue=zetazero)
        dictionaryOfZetaZeroes.update(prompts)

    # criticalLineZeroes needs to be put in a criticalLineZeroes.json
    return dictionaryOfZetaZeroes

def generateTrivialZeroes():
    pass

def generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT):
    dictionaryOfZetaZeroes = {}
    for i in range(0, CREATION_COUNT):
        # generate random complex number number
        random_real = random.randrange(start=-100, stop=100)
        random_imaginary = random.randrange(start=NEGATIVE_INFINITE, stop=INFINITE)
        random_input = random_real + (random_imaginary*1j)

        # calculate its zeta function value
        zetaValue = mpmath.zeta(random_input)
        
        prompts: dict = generateInputPrompts(zetaValue=mpmath.mpmathify(random_input), inputValue=zetaValue)
        dictionaryOfZetaZeroes.update(prompts)
    return dictionaryOfZetaZeroes

# x = mpmath.zeta(-2+0j)
z: mpmath.mpc = mpmath.zetazero(1)
# x = np.fl
print(z)
y: mpmath.mpf = z.imag
z = mpmath.zeta(2+3j)

# parseTheCriticalLineZeroes()
x = np.format_float_scientific(y)
print(x)

dictionaryOfZetaZeroes: dict = generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate)
utils.putInJsonFile(dictionaryOfZetaZeroes)

dictionaryOfZetaZeroes = generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT)
utils.putInJsonFile(dictionaryOfZetaZeroes)
