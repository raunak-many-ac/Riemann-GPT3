The goal of this project to analyse behaviour of the most heavy ML models on
complex mathematical functions, specifically Riemann Zeta function

this project uses following libraries:
    1. openai (for gpt3)
    2. mpmath (to calculate riemann zeta function)


#### to train
openai api fine_tunes.create -t dataset_prepared.jsonl -m davinci --suffix "zeta testing"


#### to use openai's json --> jsonl tool for prompt
openai tools fine_tunes.prepare_data -f "dataset.json"

#### to clist previously fine tuned models
openai api fine_tunes.list