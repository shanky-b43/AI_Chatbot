import asyncio
from graph.builder import app
from langchain_core.messages import HumanMessage

async def test_stream():
    inputs = {"messages": [HumanMessage(content="Hello")]}
    config = {"configurable": {"thread_id": "test_stream_123"}}
    
    print("Starting stream...")
    async for event in app.astream_events(inputs, version="v1", config=config):
        kind = event["event"]
        name = event["name"]
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            print(f"[{name}]: {chunk.content}", end="", flush=True)
            
if __name__ == "__main__":
    asyncio.run(test_stream())
