import json
import mpmath
import random

from constants import Constants, ExtractionConstants

# Raw json to file
def putInJsonRaw(data: dict, filePath: str):
    output_file = open(filePath, "w")
    jsonData = json.dumps(data, indent=4)
    output_file.write(jsonData)

# this function takes inference results and serialises to be dumped in a file
def serialiseInferenceResultsAndPutInFile(data: dict[tuple[mpmath.mpc, mpmath.mpf, mpmath.mpf], dict[str, mpmath.mpc]], filePath: str):
    serialisedDict: dict[str,dict[str, str]] = {}
    for key in data:
        inputToEta = f"({complexNumberToString(key[0])}, {complexNumberToString(key[1])}, {complexNumberToString(key[2])})"
        expectedInputToZeta = complexNumberToString(data[key][ExtractionConstants.expectedValue])
        inferredInputToZeta = complexNumberToString(data[key][ExtractionConstants.inferredValue])
        serialisedDict[inputToEta] = {ExtractionConstants.expectedValue: expectedInputToZeta, ExtractionConstants.inferredValue: inferredInputToZeta}

    putInJsonRaw(serialisedDict, filePath)

def convertToSerialisableJsonAndPutInJsonFile(data: dict[mpmath.mpc, tuple[mpmath.mpc, mpmath.mpf, mpmath.mpf]], filePath: str):
    serialisedDict: dict[str,str] = {}
    for key in data:
        inputToZeta = complexNumberToString(key)
        inputToEta = f"({complexNumberToString(data[key][0])}, {complexNumberToString(data[key][1])}, {complexNumberToString(data[key][2])})"
        serialisedDict[inputToZeta] = inputToEta

    putInJsonRaw(serialisedDict, filePath)

# convert a dictionary with key as prompt data (zetaValue, L, R) and value as inputValue to json
# but it should be in the specific format as per the GPT-3 doc: https://beta.openai.com/docs/guides/fine-tuning/prepare-training-data
def convertToFeedablePromptAndPutInJsonFile(data: dict[tuple[mpmath.mpc, mpmath.mpf, mpmath.mpf], mpmath.mpc], filePath: str = "./dataset.json"):
    data = convertToFeedablePrompt(data)
    putInJsonRaw(data, filePath)

def keepMaxFiveDigitsAfterDecimal(decimalStr):
    fiveDigitsAfterDecimal = min(len(decimalStr),decimalStr.find(".") + 6)
    decimalStr = decimalStr[:fiveDigitsAfterDecimal]
    return decimalStr

# will convert complex number to string input i.e. 
# mpmath.mpc(1.10211, +0.02171) --> str("1.10211 + i0.02171")
def complexNumberToString(complexNumber: mpmath.mpc) -> str:
    if isinstance(complexNumber, str):
        return complexNumber

    realPart = complexNumber.real
    realPartAsString = f'{realPart}'
    realPartAsString = keepMaxFiveDigitsAfterDecimal(realPartAsString)

    imagPart = complexNumber.imag
    imagPartAsString = f'{abs(imagPart)}'
    imagPartAsString = keepMaxFiveDigitsAfterDecimal(imagPartAsString)

    return f"{realPartAsString} {'+' if imagPart >= 0 else '-'} i{imagPartAsString}"

# will convert string input to complex i.e. 
# str("1.10211 + i0.02171") --> mpmath.mpc(1.10211, +0.02171)
def stringToComplexNumber(stringNumber: str) -> mpmath.mpc:
    splittedNumbers = stringNumber.split(" ")
    realPart = splittedNumbers[0]
    imaginaryPart = splittedNumbers[1] + splittedNumbers[2][1:]
    return mpmath.mpc(realPart, imaginaryPart)

def promptCompletionFormat(key, value):
    output = complexNumberToString(value)
    zetaValue = complexNumberToString(key[0])

    low = keepMaxFiveDigitsAfterDecimal(f"{key[1]}")
    high = keepMaxFiveDigitsAfterDecimal(f"{key[2]}")

    promptDict: dict[str, str] = {"prompt": f"Zetavalue:{zetaValue},low:{low},high:{high}", "completion":output}
    
    return promptDict

def convertToFeedablePrompt(data: dict):
    feedablePromptDict = []
    for input in data.keys():
        promptDict = promptCompletionFormat(input, data[input])
        feedablePromptDict.append(promptDict)
    return feedablePromptDict

def getInputJsonListFromFile(filePath: str) -> list[dict]:
    jsonFile = open(filePath)
    jsonList: list = json.load(jsonFile)
    return jsonList

def mergeTwoJsonsAndShuffle(jsonPaths: list, mergedJsonPath: str = "./dataset.json"):
    mergedJsons: list = []

    for jsonPath in jsonPaths:
        jsonList: list = getInputJsonListFromFile(jsonPath)
        mergedJsons.extend(jsonList)
    random.shuffle(mergedJsons)

    output_file = open(mergedJsonPath, "w")
    jsonData = json.dumps(mergedJsons, indent=4)
    output_file.write(jsonData)

if __name__ == "__main__":
    jsonPaths = ["dataset.json", Constants.pathToGeneralValues]
    mergeTwoJsonsAndShuffle(jsonPaths)

