import asyncio
import json
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import sys
import os
import psycopg2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings

# Create the MCP Server
server = Server("ai-chatbot-db-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools for interacting with the database.
    """
    return [
        types.Tool(
            name="execute_sql",
            description="Executes a READ-ONLY SQL query on the PostgreSQL database to fetch HR or Finance data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The raw SQL query string to execute. Example: SELECT * FROM users LIMIT 10;"
                    }
                },
                "required": ["query"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if name == "execute_sql":
        if not arguments or "query" not in arguments:
            raise ValueError("Missing 'query' argument")
        
        query = arguments["query"]
        
        # Simple security check to prevent destructive queries
        if any(keyword in query.upper() for keyword in ["DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT"]):
             return [types.TextContent(type="text", text="Error: Only READ-ONLY (SELECT) queries are allowed.")]
        
        try:
            if not settings.POSTGRESQL_URL:
                return [types.TextContent(type="text", text="Error: POSTGRESQL_URL not configured.")]
                
            # Connect to PostgreSQL and execute the query
            conn = psycopg2.connect(settings.POSTGRESQL_URL)
            # Ensure the connection is read-only just to be safe
            conn.set_session(readonly=True, autocommit=True)
            
            with conn.cursor() as cur:
                cur.execute(query)
                # Fetch column names
                colnames = [desc[0] for desc in cur.description] if cur.description else []
                # Fetch all rows
                rows = cur.fetchall()
                
                # Format as list of dicts
                results = [dict(zip(colnames, row)) for row in rows]
                
            conn.close()
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({"status": "success", "results": results}, default=str)
                )
            ]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error executing query: {str(e)}")]
            
    raise ValueError(f"Unknown tool: {name}")

async def main():
    """
    Run the server using stdin/stdout streams.
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ai-chatbot-db-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
