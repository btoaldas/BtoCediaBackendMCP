"""Cliente MCP real por stdio contra app/mcp/server.py del Proyecto Integrador.

La identidad sale del JWT en MCP_ACCESS_TOKEN (variable de entorno; nunca se imprime).
Usa DATABASE_URL del entorno si está definida. Con --sin-token lanza el servidor sin
MCP_ACCESS_TOKEN para mostrar que no existe usuario demo.
"""
import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def texto(resultado) -> str:
    return " ".join(" ".join(c.text.split()) for c in resultado.content if hasattr(c, "text"))


async def main(sin_token: bool) -> None:
    env = dict(os.environ)
    if sin_token:
        env["MCP_ACCESS_TOKEN"] = ""
    params = StdioServerParameters(command="uv", args=["run", "mcp", "run", "app/mcp/server.py"],
                                   env=env, cwd=os.getcwd())
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            t = await s.list_tools()
            print("transporte stdio · MCP_ACCESS_TOKEN:", "vacío" if sin_token else "JWT presente (no se imprime)")
            print("tools:", [x.name for x in t.tools])
            if sin_token:
                print("listar_productos ->", texto(await s.call_tool("listar_productos", {})))
                return
            x = await s.call_tool("crear_producto", {"nombre": "Grapas (stdio)", "cantidad": 4, "cantidad_minima": 4})
            print("crear_producto ->", texto(x))
            y = await s.call_tool("listar_alertas_reposicion", {})
            print("listar_alertas_reposicion ->", texto(y)[:300])


asyncio.run(main("--sin-token" in sys.argv))
