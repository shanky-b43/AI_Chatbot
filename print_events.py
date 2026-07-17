import asyncio
import json
from langchain_core.messages import HumanMessage
from router.graph import app
from core.config import settings

async def main():
    inputs = {"messages": [HumanMessage(content="how many paid leaves company provides?")]}
    config = {"configurable": {"thread_id": "test_events"}}
    
    print("Starting stream...")
    try:
        async for event in app.astream_events(inputs, version="v2", config=config):
            kind = event["event"]
            tags = event.get("tags", [])
            print(f"EVENT: {kind} | TAGS: {tags}")
            if "data" in event:
                data = event["data"]
                # Print specific details if it's a model stream or end
                if kind in ["on_chat_model_stream", "on_chat_model_end"]:
                    print(f"   -> DATA: {data}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
