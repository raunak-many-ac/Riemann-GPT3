# This file will generate unique data points for riemann zeta function
# it will:
# generate data
# store them in seperate files
import generateDataset as GenerateDataset
from src.constants import Constants
import src.utils as utils

CREATION_COUNT = 4000
noOfZeroesOnCriticalAxisToGenerate = 500

# load the previously generated data points in a map
previouslyGenerated: dict = {}


dictionaryOfZetaZeroes: dict = GenerateDataset.generateTheCriticalLineZeroes(noOfZeroesOnCriticalAxisToGenerate)
utils.convertToFeedablePromptAndPutInJsonFile(dictionaryOfZetaZeroes, Constants.pathToCriticalZeroes)

dictionaryOfZetaZeroes = GenerateDataset.generateInfeasibleZetaZeroes(noOfZeroesOnCriticalAxisToGenerate)
utils.convertToFeedablePromptAndPutInJsonFile(dictionaryOfZetaZeroes, Constants.pathToInfeasibleZetaZeroes)

dictionaryOfZetaZeroes = GenerateDataset.generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT)
utils.convertToFeedablePromptAndPutInJsonFile(dictionaryOfZetaZeroes, Constants.pathToGeneralValues)