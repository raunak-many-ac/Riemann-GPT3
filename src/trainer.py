# This file will generate unique data points for riemann zeta function
# it will:
# generate data
# store them in seperate files
import mpmath

import generateDataset as GenerateDataset
from constants import Constants, ExtractionConstants
import utils as utils

CREATION_COUNT = 4000
noOfZeroesOnCriticalAxisToGenerate = 500

# load the previously generated data points in a map
previouslyGeneratedDataset: list[dict] = utils.getInputJsonListFromFile(
    Constants.PreviousDatasets.pathTo_22000_dataPoints
)
allPreviouslyGeneratedOutputs: set[mpmath.mpc] = {
    utils.stringToComplexNumber(previouslyGeneratedData[ExtractionConstants.completion]) if previouslyGeneratedData[ExtractionConstants.completion] != Constants.noSolution else None
    for previouslyGeneratedData in previouslyGeneratedDataset
}
allPreviouslyGeneratedOutputs.remove(None)

dictionaryOfZetaZeroes: dict = GenerateDataset.generateTheCriticalLineZeroes(
    noOfZeroesOnCriticalAxisToGenerate
)
utils.convertToFeedablePromptAndPutInJsonFile(
    dictionaryOfZetaZeroes, Constants.pathToCriticalZeroes
)

dictionaryOfZetaZeroes = GenerateDataset.generateInfeasibleZetaZeroes(
    noOfZeroesOnCriticalAxisToGenerate
)
utils.convertToFeedablePromptAndPutInJsonFile(
    dictionaryOfZetaZeroes, Constants.pathToInfeasibleZetaZeroes
)

dictionaryOfZetaZeroes = GenerateDataset.generateRandomZetaFunctionValuesWithRanges(
    CREATION_COUNT
)
utils.convertToFeedablePromptAndPutInJsonFile(
    dictionaryOfZetaZeroes, Constants.pathToGeneralValues
)
