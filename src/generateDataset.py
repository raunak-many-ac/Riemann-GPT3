# Here are the responsibilities of this file
# 1. From the dataset file "nonTrivialZetaZeroes.val" get all critical axis zeroes
# 2. generate some trivial zeroes
# 3. generate thousands of zeta function values with there ranges of inputs
#    then dump in the dataset file

import mpmath
import random
from constants import Constants
import utils

CREATION_COUNT = 20000
noOfZeroesOnCriticalAxisToGenerate = 1000
INFINITE = 999999
NEGATIVE_INFINITE = -INFINITE - 1
# mpmath.mp.prec = 53
mpmath.mp.dps = 30 # total 30 digits of number it will be
# mpmath.mp.pretty = True


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

def generateInfeasibleZetaZeroes(noOfZeroesOnCriticalAxisToGenerate):
    noOfZeroesOnCriticalAxis = noOfZeroesOnCriticalAxisToGenerate
    
    dictionaryOfZetaZeroes = {}
    while len(dictionaryOfZetaZeroes) < noOfZeroesOnCriticalAxis:
        prompts: dict = {}
        low: float = random.randrange(start=2, stop=1000)
        high: float = random.randrange(start=2, stop=1000)
        zetaValue = mpmath.mpc(0, 0)
        prompts[(zetaValue, low, high)] = "No Solution"
        dictionaryOfZetaZeroes.update(prompts)
    
    return dictionaryOfZetaZeroes
    

def generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT):
    dictionaryOfZetaZeroes = {}
    for i in range(0, CREATION_COUNT):
        # generate random complex number number
        random_real = random.randrange(start=-2, stop=2) * random.random()
        random_imaginary = random.randrange(start=NEGATIVE_INFINITE, stop=INFINITE) * random.random()
        random_input = random_real + (random_imaginary*1j)

        # calculate its zeta function value
        zetaValue = mpmath.zeta(random_input)
        
        prompts: dict = generateInputPrompts(zetaValue=mpmath.mpmathify(random_input), inputValue=zetaValue)
        dictionaryOfZetaZeroes.update(prompts)
    return dictionaryOfZetaZeroes

# dictionaryOfZetaZeroes: dict = generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate)
# utils.putInJsonFile(dictionaryOfZetaZeroes, "./criticalZeroes.json")

# dictionaryOfZetaZeroes = generateInfeasibleZetaZeroes(noOfZeroesOnCriticalAxisToGenerate)
# utils.putInJsonFile(dictionaryOfZetaZeroes, Constants.pathToInfeasibleZetaZeroes)

dictionaryOfZetaZeroes = generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT)
utils.putInJsonFile(dictionaryOfZetaZeroes, Constants.pathToGeneralValues)
