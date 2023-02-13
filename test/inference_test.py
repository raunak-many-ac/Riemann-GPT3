# This file will randomly generate multiple riemann zeta function inputs
# to test the training efficacy.
import mpmath
import openai
import numpy
import matplotlib.pyplot as plt
import statistics

from src.constants import ExtractionConstants, Constants
import src.utils as utils
import src.graphPlotter as graph
from src.generateDataset import (
    generateRandomZetaFunctionValuesWithRanges,
    generateTheCriticalLineZeroes,
)

CREATION_COUNT = 900
noOfZeroesOnCriticalAxisToGenerate = 100
model = "davinci:ft-personal:zeta-testing-2022-11-26-15-45-02"
inferrenceResultsDict: dict[tuple[mpmath.mpc, float, float], dict[str, mpmath.mpc]] = {}
actualValues: list[mpmath.mpc] = []
inferedValues: list[mpmath.mpc] = []
# difference between expected and inferred values
inferenceDiffs: list[mpmath.mpc] = []


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


# on generatedTestCases the GPT-3 instance is tested on accuracy
def startInferenceTest(
    generatedTestCases: dict[tuple[mpmath.mpc, float, float], mpmath.mpc]
):
    for key in generatedTestCases.keys():
        output, L, R = key
        actualValue = generatedTestCases[key]
        responseStr = getRawCompletion(
            utils.complexNumberToString(key[0]),
            utils.keepMaxFiveDigitsAfterDecimal(f"{key[1]}"),
            utils.keepMaxFiveDigitsAfterDecimal(f"{key[2]}"),
        )
        responseParts = extractCompletion(responseStr)
        inferedValue = mpmath.mpc(float(responseParts[0]), float(responseParts[1]))
        inferenceDiffs.append(actualValue - inferedValue)
        actualValues.append(actualValue)
        inferedValues.append(inferedValue)
        inferrenceResultsDict[key] = {
            ExtractionConstants.expectedValue: actualValue,
            ExtractionConstants.inferredValue: inferedValue,
        }


# calculate stats on value diffs and store it in a file
def statsOnDiffs(diffs: list[mpmath.mpf]) -> dict[str, float]:
    n = len(diffs)
    diffs.sort(key=lambda diff: diff)
    minDeviation = diffs[0]
    maxDeviation = diffs[n - 1]
    # calculate average (i.e. mean)
    median = statistics.median(diffs)
    mean = sum(diffs) / n

    noOfZeroesInDiffs = diffs.count(0)

    accuracy = noOfZeroesInDiffs / n

    jsonToDump = {
        ExtractionConstants.mean: utils.keepMaxFiveDigitsAfterDecimal(f"{mean}"),
        ExtractionConstants.median: utils.keepMaxFiveDigitsAfterDecimal(f"{median}"),
        ExtractionConstants.accuracy: utils.keepMaxFiveDigitsAfterDecimal(
            f"{accuracy*100}%"
        ),
        ExtractionConstants.minDiff: utils.keepMaxFiveDigitsAfterDecimal(
            f"{minDeviation}"
        ),
        ExtractionConstants.maxDiff: utils.keepMaxFiveDigitsAfterDecimal(
            f"{maxDeviation}"
        ),
    }

    return jsonToDump


generatedTestCases: dict[
    tuple[mpmath.mpc, float, float], mpmath.mpc
] = generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate)

generatedTestCases.update(generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT))

startInferenceTest(generatedTestCases)

# dump the test results in a file
utils.serialiseInferenceResultsAndPutInFile(
    inferrenceResultsDict, Constants.PATH_TO_22000_INFERENCE_TEST_RESULT
)

# statistics on the inferenceDiffs
realPartSortedDiffs: mpmath.mpf = [abs(diff.real) for diff in inferenceDiffs]
imagPartSortedDiffs: mpmath.mpf = [abs(diff.imag) for diff in inferenceDiffs]

realPartStats = statsOnDiffs(realPartSortedDiffs)
imagPartStats = statsOnDiffs(imagPartSortedDiffs)

stats = {}
stats[ExtractionConstants.realPartStats] = realPartStats
stats[ExtractionConstants.imagPartStats] = imagPartStats
utils.putInJsonRaw(stats, filePath=Constants.PATH_TO_INFERRENCE_STATS)

graph.plotTheseNew(
    xOfCurves=[
        numpy.array([v.real for v in actualValues]),
        numpy.array([v.real for v in inferedValues]),
    ],
    yOfCurves=[
        numpy.array([v.imag for v in actualValues]),
        numpy.array([v.imag for v in inferedValues]),
    ],
    titleOfPlot="Expected curve and Inferred curve",
    nameOfCurves=["Expected", "Inferred"],
    coloursOfCurves=["blue", "green"],
)

# plot a different graph on difference between actual and inferred values
graph.plotTheseNew(
    xpoints=[numpy.array([diff.real for diff in inferenceDiffs])],
    ypoints=[numpy.array([diff.imag for diff in inferenceDiffs])],
    titleOfPlot="Difference between expected and inferred",
    coloursOfCurves=["red"]
)