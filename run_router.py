import asyncio
from langchain_core.messages import HumanMessage
from router.graph import app
from loguru import logger

async def test_router(query: str):
    logger.info(f"--- Testing Router with Query: '{query}' ---")
    
    # 1. Prepare initial state
    inputs = {
        "messages": [HumanMessage(content=query)]
    }
    
    # 2. Invoke the graph
    # We use config tags to trace it if needed
    result = await app.ainvoke(inputs, config={"configurable": {"thread_id": "test_123"}})
    
    # 3. Print the selected workflow and the final AI message
    print("\n[RESULT]")
    print(f"Selected Workflow: {result.get('next_worker')}")
    
    messages = result.get("messages", [])
    if messages:
        print(f"Response Content: {messages[-1].content}")
    print("-" * 50 + "\n")

async def main():
    # Example 1: DocTalk (Existing chatbot logic will trigger)
    await test_router("What is the company policy on remote work?")
    
    # Example 2: DBTalk (Placeholder will trigger)
    await test_router("List all employees from the database.")
    
    # Example 3: Summary (Placeholder will trigger)
    await test_router("Provide an executive summary of this chat.")

if __name__ == "__main__":
    asyncio.run(main())
