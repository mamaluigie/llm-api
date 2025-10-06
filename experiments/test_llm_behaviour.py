import argparse
import transformers
from huggingface_hub import login
import time
import json
import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():

    i_time = time.time()

    api_key = ""
    # Open the config json
    with open("credentials.json", "r") as file:
        api_key = json.load(file)["api_key"]


    # Logging into hugging face now
    login(token=api_key)

    model_id = "meta-llama/Llama-3.2-1B"

    pipe = transformers.pipeline(
            "text-generation",
            model=model_id,
            dtype="float16",
            device_map="auto")

    print(pipe.model.dtype)
    print(pipe.model.hf_device_map)
    test_message = "what is the capital of france and what are some interesting places there."

    outputs = pipe(
            test_message
            )

    print(f'finished in {time.time() - i_time} seconds.')


    return outputs

