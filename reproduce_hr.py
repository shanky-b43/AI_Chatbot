import asyncio
import os
import json
from workflows.hr import build_hr_workflow
from langchain_core.messages import HumanMessage
from core.config import settings

async def main():
    agent = build_hr_workflow()
    
    inputs = {"messages": [HumanMessage(content="how many paid leaves company provides?")]}
    config = {"configurable": {"thread_id": "test_hr"}}
    
    print("Running HR agent...")
    try:
        # Astream events to see what events are generated
        async for event in agent.astream_events(inputs, version="v2", config=config):
            kind = event["event"]
            tags = event.get("tags", [])
            print(f"Event: {kind}, Tags: {tags}")
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                print(f"Token: {chunk.content!r}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
