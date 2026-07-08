import asyncio
from langchain_core.tools import tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys

# We'll use synchronous wrappers since LangGraph agents are sync for now.
# Real world apps might use async graphs, but this demonstrates the integration.

def run_mcp_tool_sync(server_script: str, tool_name: str, arguments: dict) -> str:
    """
    Spawns an MCP server via stdio, calls a tool, and returns the result synchronously.
    """
    async def _run():
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

    return asyncio.run(_run())

@tool
def execute_sql_tool(query: str) -> str:
    """
    Executes a READ-ONLY SQL query on the PostgreSQL database to fetch HR or Finance data.
    """
    return run_mcp_tool_sync("mcp/db_server.py", "execute_sql", {"query": query})

@tool
def search_documents_tool(query: str) -> str:
    """
    Searches the Elasticsearch knowledge base to answer questions about company policies, IT guides, and general knowledge.
    """
    return run_mcp_tool_sync("mcp/es_server.py", "search_documents", {"query": query})
