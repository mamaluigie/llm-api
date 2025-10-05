# Description

This is going to be an api to recieve sentences to an initialized llm on the serverside. Each prompt without an associated chat id will create a new chat history to keep the context on the server side. There will also be functionality for listing all of the available previous chats that happened with associated ids so I can pick up from where I left off if wanted to.

## Client Code
There is a client program that is set up to interact with each of the api endpoints in a proper manner, keeping track of the context id that it is currently being focused on.

## Server Code
The server code is in charge of saving all of the previous chats and updating to them accordingly with the output of the llm. The api server is in charge of running the 

To run the api run this command:
- fastapi dev llm_api_server.py

# To Do List

- [x] Get the hugging face model working with cuda cores on local system.
- [x] Set up the initial api for retrieving llm responses.
- [x] Set up the api to handle chat context and multiple chat histories.
- [x] Set up the client code to update the contexts properly and properly update the preprimed and saved answers and questions.
- [ ] Set up functionality for listing all of the chat contexts and each id associated.
- [ ] Set up functionality for entering manually a context id to reference a chat of choice.
- [ ] Update the current LLM to be primed with the proper text to make sure the output is proper.
- [ ] Potentially look into containerizing the api into a docker solution or similar. ( May be difficult to make work properly with cuda since cuda is kind of hardware specific. Misght have to be )


