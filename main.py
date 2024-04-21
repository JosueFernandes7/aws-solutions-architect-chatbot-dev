# from genai import get_answer
# query = input('Digite sua dúvida:')
# while query != "exit":
#     print ("Generating")
#     response = get_answer(query)
#     print(response)
#     query = input('Digite sua nova dúvida:')


import chainlit as cl
from genai import get_answer

@cl.on_message
async def main(message: cl.Message):
    completion = get_answer(message.content)
    await cl.Message(
        content=completion,
    ).send()
