# This file interacts with gpt3 model for uses the dataset file to train it and get output
import openai
import os

API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = API_KEY

prompt = "Zetavalue:0 + i0,low:0.50001,high:1 ->"
model="davinci:ft-personal:zeta-testing-2022-11-26-15-45-02"
response = openai.Completion.create(model=model, prompt=prompt)

print(response)
