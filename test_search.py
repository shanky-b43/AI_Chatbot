from mcp_integration.clients import search_documents_tool
import sys
import asyncio

if __name__ == "__main__":
    try:
        res = search_documents_tool.invoke({"query": "time table"})
        print("RESULT:")
        print(res)
    except Exception as e:
        print("ERROR:")
        print(e)
