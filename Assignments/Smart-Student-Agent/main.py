from agents import Agent,OpenAIChatCompletionsModel,Runner,AsyncOpenAI
from agents.run import RunConfig
import os
from dotenv import load_dotenv
import chainlit as cl
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config =RunConfig (
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


agent = Agent(
    name="HELP FULL ASSISTANT",
    instructions="""
    You are a strict and helpful AI assistant designed **only** for students. 
    You must **only answer questions related to education, learning, school subjects, study techniques, or academic content**.

    If the user asks anything unrelated to studies — such as personal questions, jokes, news, entertainment, politics, or any non-educational topic — politely reply:

    "I'm here only to help you with your studies. Please ask a study-related question."

    Never break this rule.
    """
)


@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello!! i am smart and friendly Study Assistant. How can i help you today.?").send()
@cl.on_message
async def handle_message(message:cl.Message):
    history = cl.user_session.get("history")
    history.append({"role":"use","content":message.content})
    result = await Runner.run(
    agent,
    input=message.content,
    run_config=config
    )
    history.append({"role":"assiistant","content":result.final_output})
    cl.user_session.set("history",history)
    await cl.Message(content=result.final_output).send()


    











