# This file interacts with gpt3 model for uses the dataset file to train it and get output
import openai
import os

API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = API_KEY

prompt = "Zetavalue:99.0 + i577761.0,low:-735.501190440275,high:697.417908589293"
model="zeta testing",
response = openai.Completion.create(model=model, prompt=f"prompt:{prompt}")

print(response)
