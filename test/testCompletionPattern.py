### This file checks whether after 22k training fine tuning was GPT-3 able to infer 
### output such that first occurrence is the actual complex number output
import mpmath 
import openai

from src.constants import ExtractionConstants
from src.generateDataset import generateRandomZetaFunctionValuesWithRanges

CREATION_COUNT = 1000
noOfZeroesOnCriticalAxisToGenerate = 1
model="davinci:ft-personal:zeta-testing-2022-11-26-15-45-02"

def getRawCompletion(input: tuple, L: float, R: float) -> str:
    prompt = f"Zetavalue:{input},low:{L},high:{R} ->"
    response = openai.Completion.create(model=model, prompt=prompt)
    return response[ExtractionConstants.choices][0][ExtractionConstants.text]

def checkWhetherItStartsWithADecimalNumber(response: str) -> bool:
    # check whether tthe first character of every response is " "
    if response[0] != " " or not (response[1].isdigit() or response[1] == "-" or response[1] == "+"):
        return False

    i = 1
    # keep checking till we find a decimal point
    while i < len(response) and response[i] != ".":
        if not response[i].isdigit() and not response[i] in (".", "-", "+"):
            return False
        i+=1
    i += 1
    return True if response[i].isdigit() else False

dictionaryOfZetaZeroes: dict[tuple[mpmath.mpc, float, float], mpmath.mpc] = generateRandomZetaFunctionValuesWithRanges(CREATION_COUNT)

for key in dictionaryOfZetaZeroes.keys():
    output, L, R = key
    value = dictionaryOfZetaZeroes[key]
    response = getRawCompletion(key[0], key[1], key[2])
    if not checkWhetherItStartsWithADecimalNumber(response):
        raise Exception(f"screwed up for response = {response} key = {key} and value = {value}")

print(f"with {CREATION_COUNT} random points the test was successful 😎")