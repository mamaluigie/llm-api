import random
import argparse
import transformers
from huggingface_hub import login
import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

def generate_response(sentence):

    api_key = ""
    # Open the config json
    with open("credentials.json", "r") as file:
        api_key = json.load(file)["api_key"]

    # Logging into hugging face
    login(token=api_key)

    model_id = "meta-llama/Llama-3.2-1B"

    pipe = transformers.pipeline(
            "text-generation",
            model=model_id,
            dtype="float16",
            device_map="auto")
    print(pipe.model.dtype)
    print(pipe.model.hf_device_map)

    outputs = pipe(
            sentence
            )


    return outputs


def context_file_exists(context_id):
    if f'chat_{context_id}' in os.listdir("./chats"):
        return True
    return False

# ----------------------api information---------------------------

class Model_Info(BaseModel):
    context_id: Optional[str] = None
    sentence: str


app = FastAPI()

@app.post("/")
def root(model_info: Model_Info):

    sentence = model_info.sentence

    # If there is no context id create one and a new chat file/directory
    if model_info.context_id == None:

        if not os.path.exists("./chats"):
            os.mkdir("./chats")

        # Generate a new context id file that already doesnt exist
        new_context_id = random.randint(1, 999999999)
        while context_file_exists(new_context_id):
            new_context_id = random.randint(1, 999999999)

        new_context_file = f'chat_{new_context_id}'

        # Create a file with the context id in the name in the directory
        with open(f'./chats/{new_context_file}', 'w') as context_file:
            # Write the sentence and create a new line.
            context_file.write(f'Q: {sentence}\n')

            llm_response = generate_response(model_info.sentence)
            context_file.write(f'A: {llm_response[0]["generated_text"]}\n')

        return {"context_id": new_context_id,
                "answer" : llm_response[0]["generated_text"]}

    else:
        # Check to see if that context_id exists in the chats folder
        if not os.path.exists("./chats"):
            return {"code":"Error: No chats directory exists. Initialize with a context id"}

        elif context_file_exists(model_info.context_id):

            context_file = f'chat_{new_context_id}'

            with open(f'./chats/{context_file}', 'r') as context_file:

                full_context = context_file.readall()

                # Add the new question to the full_context
                full_context = full_context + sentence + "\n"

            with open(f'./chats/{context_file}', 'a') as context_file:

                llm_response = generate_response(full_context)

                # Write the question and response to the context file
                context_file.write(f'Q: {sentence}')
                context_file.write(f'A: {llm_response}')

        else:
            return {"code":"Error: Context does not exists for that context id."}


