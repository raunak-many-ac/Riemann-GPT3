# This file will randomly generate multiple riemann zeta function inputs
# test the training efficacy.

from generateDataset import generateRandomZetaFunctionValuesWithRanges, generateTheCriticalLineZeroes

CREATION_COUNT = 1000
noOfZeroesOnCriticalAxisToGenerate = 50

dictionaryOfZetaZeroes: dict = generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate)

dictionaryOfZetaZeroes.update(generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT))

