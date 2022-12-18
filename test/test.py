# This file will randomly generate multiple riemann zeta function inputs
# to test the training efficacy.

from generateDataset import generateRandomZetaFunctionValuesWithRanges, generateTheCriticalLineZeroes

import mpmath
import openai

CREATION_COUNT = 1000
noOfZeroesOnCriticalAxisToGenerate = 50
model="davinci:ft-personal:zeta-testing-2022-11-26-15-45-02"

def getCompletion(input: tuple, L: float, R: float):
    prompt = f"Zetavalue:{input},low:{L},high:{R} ->"
    response = openai.Completion.create(model=model, prompt=prompt)

def removeNoise(response):
    pass

def findDiff(val1: mpmath.mpc, val2: mpmath.mpc):
    pass

dictionaryOfZetaZeroes: dict = generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate)

dictionaryOfZetaZeroes.update(generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT))

inferenceDiffs = []
for key, value in dictionaryOfZetaZeroes:
    response = getCompletion(key[0], key[1], key[2])
    response = removeNoise(response)
    inferenceDiffs.append(findDiff(value, response))

# put inferrence diffs in a json file

# find mean and median inference Diffs

