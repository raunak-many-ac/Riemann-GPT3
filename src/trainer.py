# This file will generate unique data points for riemann zeta function
# it will:
# generate data
# store them in seperate files
import mpmath

import generateDataset as GenerateDataset
from constants import Constants, ExtractionConstants
import utils as utils

CREATION_COUNT = 6500
noOfZeroesOnCriticalAxisToGenerate = 750

## load the previously generated data points in a map
previouslyGeneratedDataset: list[dict] = utils.getInputJsonListFromFile(
    Constants.PreviousDatasets.pathTo_22000_dataPoints
)
allPreviouslyGeneratedOutputs: set[mpmath.mpc] = {
    utils.stringToComplexNumber(previouslyGeneratedData[ExtractionConstants.completion])
    if previouslyGeneratedData[ExtractionConstants.completion] != Constants.noSolution
    else None
    for previouslyGeneratedData in previouslyGeneratedDataset
}
allPreviouslyGeneratedOutputs.remove(None)

# generate zeroes in critical axis
dictionaryOfZetaZeroes: dict = {}

while len(dictionaryOfZetaZeroes) < noOfZeroesOnCriticalAxisToGenerate:
    temp: dict = GenerateDataset.generateTheCriticalLineZeroes(
        noOfZeroesOnCriticalAxisToGenerate - len(dictionaryOfZetaZeroes)
    )
    dictionaryOfZetaZeroes.update(
        utils.removeKeysFromMap1(temp, allPreviouslyGeneratedOutputs)
    )

utils.convertToFeedablePromptAndPutInJsonFile(
    dictionaryOfZetaZeroes, Constants.pathToCriticalZeroes
)

# generate infeasible zeroes
dictionaryOfInfeasibleZeroes: dict = {}

while len(dictionaryOfInfeasibleZeroes) < noOfZeroesOnCriticalAxisToGenerate:
    temp = GenerateDataset.generateInfeasibleZetaZeroes(
        noOfZeroesOnCriticalAxisToGenerate - len(dictionaryOfInfeasibleZeroes)
    )
    dictionaryOfInfeasibleZeroes.update(
        utils.removeKeysFromMap1(temp, allPreviouslyGeneratedOutputs)
    )

utils.convertToFeedablePromptAndPutInJsonFile(
    dictionaryOfInfeasibleZeroes, Constants.pathToInfeasibleZetaZeroes
)

# generate random feasible points other than critical axis
dictionaryOfZetaZeroes = {}

while len(dictionaryOfZetaZeroes) < CREATION_COUNT:
    temp = GenerateDataset.generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT - len(dictionaryOfZetaZeroes))
    dictionaryOfZetaZeroes.update(
        utils.removeKeysFromMap1(temp, allPreviouslyGeneratedOutputs)
    )

utils.convertToFeedablePromptAndPutInJsonFile(
    dictionaryOfZetaZeroes, Constants.pathToGeneralValues
)
