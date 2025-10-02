import requests
import os
import argparse


# Generate a new context id if one is not provided, send it, store it into a local .cache file for new requests
def main(sentence):

    url = "http://127.0.0.1:8000/"

    if ".context" not in os.listdir("."):
        body = {"context_id" : None, "sentence" : sentence}

        with open(".context", "w") as local_context_id:

            response = requests.post(url, json=body)
            print(response.status_code)
            print(response.json())
            dict_response = response.json()

            # Writing the context to the local context file
            local_context_id.write(str(dict_response["context_id"]))

    else:

        with open(".context", "r") as local_context_id:
            context_id = local_context_id.read()
            print(context_id)

            body = {"context_id" : context_id, "sentence" : sentence}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--string', required=True, help='This is the qustion that you will ask the llm')

    parsed = parser.parse_args()

    main(parsed.string)

