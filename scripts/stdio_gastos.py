"""Cliente MCP real por stdio contra app/mcp/server.py (usa DATABASE_URL del entorno si está definida)."""
import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(command="uv", args=["run", "mcp", "run", "app/mcp/server.py"],
                                   env=dict(os.environ), cwd=os.getcwd())
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            t = await s.list_tools()
            print("stdio tools:", [x.name for x in t.tools])
            x = await s.call_tool("registrar_gasto", {"descripcion": "Café stdio", "monto": 2.5, "categoria": "comida"})
            print("stdio registrar:", " ".join(x.content[0].text.split()))


asyncio.run(main())
