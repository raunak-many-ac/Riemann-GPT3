# This file will randomly generate multiple riemann zeta function inputs
# to test the training efficacy.
import mpmath
import openai
import numpy
import matplotlib.pyplot as plt

from src.constants import ExtractionConstants, Constants
import src.utils as utils
from src.generateDataset import (
    generateRandomZetaFunctionValuesWithRanges,
    generateTheCriticalLineZeroes,
)

CREATION_COUNT = 1
noOfZeroesOnCriticalAxisToGenerate = 1
model = "davinci:ft-personal:zeta-testing-2022-11-26-15-45-02"


def getRawCompletion(input: str, L: float, R: float):
    prompt = f"Zetavalue:{input},low:{L},high:{R} ->"
    response = openai.Completion.create(model=model, prompt=prompt)
    return response[ExtractionConstants.choices][0][ExtractionConstants.text]


# extract out the value from the completion output, since it may contain some
# pollution. In the  completion string try to find location of "+ i" then
# we can extract the complex number
def extractCompletion(rawCompletion: str) -> tuple[str, str]:
    realPartSign = "" if rawCompletion[1].isdigit() else rawCompletion[1]

    # start extracting real part
    startOfRealPart = 1 if rawCompletion[1].isdigit() else 2
    endOfRealPart = startOfRealPart

    while endOfRealPart < len(rawCompletion):
        if (
            not rawCompletion[endOfRealPart].isdigit()
            and not rawCompletion[endOfRealPart] == "."
        ):
            break
        endOfRealPart += 1

    realPartStr = rawCompletion[startOfRealPart:endOfRealPart]
    imagPartStr = "0"
    imaginaryPartSign = "+"

    # check if imaginary part exists
    if rawCompletion[endOfRealPart] == " " and rawCompletion[endOfRealPart + 1] in (
        "-",
        "+",
    ):
        # extract imaginary part
        imaginaryPartSign = rawCompletion[endOfRealPart + 1]
        startOfImagPart = endOfRealPart + 4
        endOfImagPart = startOfImagPart

        while endOfImagPart < len(rawCompletion):
            if (
                not rawCompletion[endOfImagPart].isdigit()
                and not rawCompletion[endOfImagPart] == "."
            ):
                break
            endOfImagPart += 1
        imagPartStr = rawCompletion[startOfImagPart:endOfImagPart]

    return (f"{realPartSign}{realPartStr}", f"{imaginaryPartSign}{imagPartStr}")


dictionaryOfZetaZeroes: dict[
    tuple[mpmath.mpc, float, float], mpmath.mpc
] = generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate)

dictionaryOfZetaZeroes.update(generateRandomZetaFunctionValuesWithRanges(2))

# dictionary dictionaryOfZetaZeroes has entries as tuple -> complexNumber
# which is not serialisable to put in json file
inverseDict = {}
for key in dictionaryOfZetaZeroes:
    inverseDict[dictionaryOfZetaZeroes[key]] = key
utils.convertToSerialisableJsonAndPutInJsonFile(inverseDict, Constants.PATH_TO_22000_GENERATED_INFERENCE_INPUT)

inferenceDiffs: list[mpmath.mpc] = []
actualValues: list[mpmath.mpc] = []
inferedValues: list[mpmath.mpc] = []
for key in dictionaryOfZetaZeroes.keys():
    output, L, R = key
    value = dictionaryOfZetaZeroes[key]
    responseStr = getRawCompletion(
        utils.complexNumberToString(key[0]),
        utils.keepMaxFiveDigitsAfterDecimal(f"{key[1]}"),
        utils.keepMaxFiveDigitsAfterDecimal(f"{key[2]}"),
    )
    responseParts = extractCompletion(responseStr)
    inferedValue = mpmath.mpc(float(responseParts[0]), float(responseParts[1]))
    inferenceDiffs.append(value - inferedValue)
    actualValues.append(value)
    inferedValues.append(inferedValue)

xpoints = numpy.array([ v.real for v in actualValues])
ypoints = numpy.array([ v.imag for v in actualValues])
plt.plot(xpoints, ypoints, color='blue', marker=".", markersize=10)

xpoints = numpy.array([ v.real for v in inferedValues])
ypoints = numpy.array([ v.imag for v in inferedValues])
plt.plot(xpoints, ypoints, color='green', marker=".", markersize=10)

plt.figure()
xpoints = numpy.array([ actualValues[i].real -  inferedValues[i].real for i in range(0, len(actualValues))])
ypoints = numpy.array([ actualValues[i].imag -  inferedValues[i].imag for i in range(0, len(actualValues))])
plt.plot(xpoints, ypoints, color='green', marker=".", markersize=10)

plt.show()

# put inferrence diffs in a json file

# find mean, median and accuracy percentage inference Diffs
