import json
import mpmath
import random

from src.constants import Constants

# Raw json to file
def putInJsonRaw(data: dict, filePath: str):
    output_file = open(filePath, "w")
    jsonData = json.dumps(data, indent=4)
    output_file.write(jsonData)

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

def mergeTwoJsonsAndShuffle(jsonPaths: list, mergedJsonPath: str = "./dataset.json"):
    mergedJsons: list = []

    for jsonPath in jsonPaths:
        jsonFile = open(jsonPath)
        jsonList: list = json.load(jsonFile)
        mergedJsons.extend(jsonList)
    random.shuffle(mergedJsons)

    output_file = open(mergedJsonPath, "w")
    jsonData = json.dumps(mergedJsons, indent=4)
    output_file.write(jsonData)

if __name__ == "__main__":
    jsonPaths = ["dataset.json", Constants.pathToGeneralValues]
    mergeTwoJsonsAndShuffle(jsonPaths)

