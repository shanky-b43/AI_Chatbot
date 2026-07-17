from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.3
)

system_prompt = """You are the final Synthesizer for an Enterprise AI Chatbot.
Your job is to read the conversation below (which may contain multiple answers from different departments like HR and Finance).
You must combine all the provided information into one clean, cohesive, and friendly response to the user.
Do not mention that you are a synthesizer or that multiple agents were involved. Just give the final answer naturally.
"""

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content="hi, i am shanky"),
    AIMessage(content="No response generated."),
    HumanMessage(content="tell me what is my name?")
]

response = llm.invoke(messages)
print("Response:", repr(response.content))
