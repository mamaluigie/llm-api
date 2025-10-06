import requests
import os
import argparse

# Standardized function to read from the local context file
def read_context_file():
    with open(".context", "r") as local_context_id:
        context_id = local_context_id.read()
    return context_id

# Standardized function to write to the chat context file
def update_context_file(context_id):
    with open(".context", "w") as local_context_id:
        local_context_id.write(str(context_id))

# Check server if the context file exists
def context_exists(url, context_id):
    endpoint = "context_exists/"
    response = requests.get("".join([url, endpoint]), params={"context_id" : context_id})
    return response.json()

# Generate a new context id if one is not provided, send it, store it into a local .cache file for new requests
def main(sentence, context_id):

    url = "http://127.0.0.1:8000/"

    if ".context" not in os.listdir("."):

        if context_id:
            body = {"context_id" : context_id, "sentence" : sentence}

            # Check if the context exists on the server
            if context_exists(url, context_id):

                # Get the new context id
                response = requests.post(url, json=body)
                dict_response = response.json()
                print(dict_response["answer"])

                # Generate a context file with current context
                update_context_file(context_id)

            else:
                print("Context does not exist on the remote server")

        else:
            body = {"context_id" : None, "sentence" : sentence}

            # Get the new context id
            response = requests.post(url, json=body)

            dict_response = response.json()

            # Updating the context to the local context file
            update_context_file(str(dict_response["context_id"]))

            print(dict_response["answer"])

    else:

        if context_id:

            if context_exists(url, context_id):
                body = {"context_id" : context_id, "sentence" : sentence}

                response = requests.post(url, json=body)
                dict_response = response.json()
                print(dict_response["answer"])

                # Update the context file
                update_context_file(context_id)
            else:
                print("Context does not exist on the remote server")

        else:
            # Use the current context id in the .context file
            context_id = read_context_file()

            body = {"context_id" : context_id, "sentence" : sentence}

            response = requests.post(url, json=body)
            dict_response = response.json()

            # Print the response to the sentence question that was sent
            print(dict_response["answer"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--string', required=True, help='This is the qustion that you will ask the llm')
    parser.add_argument('--context_id', default=None, help='This is an option to manually specify a particular chat context to pay attention to when communicating with the backend llm.')

    parsed = parser.parse_args()

    main(parsed.string, parsed.context_id)

