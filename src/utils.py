import json

def putInJsonFile(data: dict, filePath: str = "./dataset.json"):
    output_file = open(filePath, "w")
    data = convertToFeedablePrompt(data)
    jsonData = json.dumps(data, indent=4)
    output_file.write(jsonData)

def complexNumberToString():
    pass

def stringToComplexNumber():
    pass
def promptCompletionFormat(key, value):
    output = f"{value.real} {'+' if value.imag >= 0 else '-'} i{abs(value.imag)}"

    zetaValue = f"{key[0].real} {'+' if key[0].imag >= 0 else '-'} i{abs(key[0].imag)}"
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
        