from graph.builder import app
from langchain_core.messages import HumanMessage
import traceback

try:
    result = app.invoke(
        {'messages': [HumanMessage(content='what is my name?')]}, 
        config={'configurable': {'thread_id': '123'}}
    )
    print("SUCCESS")
    print(result)
except Exception as e:
    print("ERROR:")
    traceback.print_exc()
