import json

def putInJsonFile(data: dict, filePath: str = "./dataset.json"):
    output_file = open(filePath, "w")
    data = convertToFeedablePrompt(data)
    jsonData = json.dumps(data, indent=4)
    output_file.write(jsonData)

def complexNumberToString(complexNumber):
    return f"{complexNumber.real} {'+' if complexNumber.imag >= 0 else '-'} i{abs(complexNumber.imag)}"

def stringToComplexNumber():
    pass

def promptCompletionFormat(key, value):
    output = complexNumberToString(value)

    zetaValue = complexNumberToString(key[0])
    low = key[1]
    high = key[2]

    promptDict: dict[str, str] = {"prompt": f"Zetavalue:{zetaValue},low:{low},high:{high}", "completion":output}
    
    return promptDict

def convertToFeedablePrompt(data: dict):
    feedablePromptDict = []
    for input in data.keys():
        promptDict = promptCompletionFormat(input, data[input])
        feedablePromptDict.append(promptDict)
    return feedablePromptDict
        