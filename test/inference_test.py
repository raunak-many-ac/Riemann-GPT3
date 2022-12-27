# This file will randomly generate multiple riemann zeta function inputs
# to test the training efficacy.
import mpmath 
import openai
import numpy
import matplotlib.pyplot as plt

from src.constants import ExtractionConstants
from src.generateDataset import generateRandomZetaFunctionValuesWithRanges, generateTheCriticalLineZeroes

CREATION_COUNT = 1
noOfZeroesOnCriticalAxisToGenerate = 1
model="davinci:ft-personal:zeta-testing-2022-11-26-15-45-02"

def getRawCompletion(input: tuple, L: float, R: float):
    prompt = f"Zetavalue:{input},low:{L},high:{R} ->"
    response = openai.Completion.create(model=model, prompt=prompt)
    return response[ExtractionConstants.choices][0][ExtractionConstants.text]

# extract out the value from the completion output, since it may contain some
# pollution. In the  completion string try to find location of "+ i" then
# we can extract the complex number
def extractCompletion(rawCompletion: str):
    imaginaryPartSign = "+" if rawCompletion.find(" - i") == -1 else "-"
    subStringToSearch = f" {imaginaryPartSign} i"
    ind = rawCompletion.find(subStringToSearch)
    if ind == -1:
        raise Exception(f"in {rawCompletion} substring '{subStringToSearch}' is not found")

    lastDigitIndexOfRealPart = ind-1
    firstDigitIndexOfImagPart = lastDigitIndexOfRealPart + 5
    realPartDigits = []
    imagPartDigits = []

    while rawCompletion[lastDigitIndexOfRealPart].isdigit() or rawCompletion[lastDigitIndexOfRealPart] == ".":
        realPartDigits.append(rawCompletion[lastDigitIndexOfRealPart])
        lastDigitIndexOfRealPart -= 1
    
    while rawCompletion[firstDigitIndexOfImagPart].isdigit() or rawCompletion[firstDigitIndexOfImagPart] == ".":
        imagPartDigits.append(rawCompletion[firstDigitIndexOfImagPart])
        firstDigitIndexOfImagPart += 1

    realPartDigits.reverse()
    realPartStr = "".join(realPartDigits)
    imagPartStr = "".join(imagPartDigits)

    return f"{realPartStr}{subStringToSearch}{imagPartStr}"

def findDiff(val1: mpmath.mpc, val2: mpmath.mpc):
    pass

dictionaryOfZetaZeroes: dict[tuple[mpmath.mpc, float, float], mpmath.mpc] = generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate)

dictionaryOfZetaZeroes.update(generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT))

inferenceDiffs: list[mpmath.mpc] = []
actualValues: list[mpmath.mpc] = []
inferedValues: list[mpmath.mpc] = []
for key in dictionaryOfZetaZeroes.keys():
    output, L, R = key
    value = dictionaryOfZetaZeroes[key]
    response = getRawCompletion(key[0], key[1], key[2])
    response = extractCompletion(response)
    # inferenceDiffs.append(findDiff(value, response))
    actualValues.append(value)
    inferedValues.append(response)

xpoints = numpy.array(actualValues)
ypoints = numpy.array(inferedValues)

plt.plot(xpoints, ypoints)
plt.show()

# put inferrence diffs in a json file

# find mean, median and accuracy percentage inference Diffs
    
