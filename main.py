import chainlit as cl
from genai import get_answer

@cl.on_message
async def main(message: cl.Message):
    completion = get_answer(message.content)
    await cl.Message(
        content=completion,
    ).send()
