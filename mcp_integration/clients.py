import asyncio
from langchain_core.tools import tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys

# We'll use asynchronous wrappers because LangGraph agents are executed asynchronously via ainvoke
# and astream_events. Using asyncio.run() inside sync tools causes a RuntimeError when the event loop is already running.

async def run_mcp_tool_async(server_script: str, tool_name: str, arguments: dict) -> str:
    """
    Spawns an MCP server via stdio, calls a tool, and returns the result asynchronously.
    """
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(tool_name, arguments)
            if result.isError:
                return f"Error: {result.content[0].text}"
            return result.content[0].text

@tool
async def execute_sql_tool(query: str) -> str:
    """
    Executes a READ-ONLY SQL query on the PostgreSQL database to fetch HR or Finance data.
    """
    return await run_mcp_tool_async("mcp_integration/db_server.py", "execute_sql", {"query": query})

@tool
async def search_documents_tool(query: str, sub_node: str = None) -> str:
    """
    Searches the Elasticsearch knowledge base to answer questions about company policies, IT guides, and general knowledge.
    If you belong to a specific department sub_node (e.g. 'expense_management'), you MUST pass it in the sub_node parameter to get accurate results.
    """
    return await run_mcp_tool_async("mcp_integration/es_server.py", "search_documents", {"query": query, "sub_node": sub_node})
