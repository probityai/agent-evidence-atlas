#!/usr/bin/env python3
"""Run the lost-response cases through the MCP Python SDK 2.2.0."""

from __future__ import annotations

import json
import os
import sys
import urllib.request

import anyio
from mcp.client.session import ClientSession
from mcp.server.lowlevel.server import Server
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.context import Context
from mcp.shared.exceptions import MCPError
from mcp.shared.memory import SessionMessage, create_client_server_memory_streams
from mcp_types.jsonrpc import JSONRPCError, JSONRPCRequest, JSONRPCResponse


async def exercise(case: dict) -> dict:
    server = MCPServer(name="retry-effect-probe")
    committed = set()

    @server.tool()
    def create_order(operation_key: str, ctx: Context) -> str:
        if case["mode"] == "application-dedup" and operation_key in committed:
            return "deduped"
        body = json.dumps({"operationKey": operation_key}).encode("ascii")
        request = urllib.request.Request(os.environ["PROBITY_EFFECT_URL"], body, method="POST")
        with urllib.request.urlopen(request, timeout=2) as response:
            response.read()
        committed.add(operation_key)
        return "committed"

    streams = create_client_server_memory_streams()
    client_streams, server_streams = await streams.__aenter__()
    from_server, to_server = client_streams
    server_reader, server_writer = server_streams
    client_writer, relay_reader = anyio.create_memory_object_stream(256)
    relay_writer, client_reader = anyio.create_memory_object_stream(256)
    ids = []
    dropped = False

    async def requests():
        async with relay_reader, to_server:
            async for message in relay_reader:
                if (isinstance(message, SessionMessage)
                    and isinstance(message.message, JSONRPCRequest)
                    and message.message.method == "tools/call"):
                    ids.append(message.message.id)
                await to_server.send(message)

    async def responses():
        nonlocal dropped
        async with from_server, relay_writer:
            async for message in from_server:
                if (not dropped and isinstance(message, SessionMessage)
                    and isinstance(message.message, (JSONRPCResponse, JSONRPCError))
                    and ids and message.message.id == ids[0]):
                    dropped = True
                    continue
                await relay_writer.send(message)

    async def serve():
        lowlevel: Server = server._lowlevel_server
        await lowlevel.run(
            server_reader, server_writer,
            lowlevel.create_initialization_options(), raise_exceptions=False,
        )

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(serve)
        tasks.start_soon(requests)
        tasks.start_soon(responses)
        session = ClientSession(client_reader, client_writer)
        await session.__aenter__()
        initialized = await session.initialize()
        args = {"operation_key": case["operationKey"]}
        timed_out = False
        try:
            await session.call_tool("create_order", args, read_timeout_seconds=2)
        except MCPError:
            timed_out = True
        if not timed_out:
            raise RuntimeError("first call did not time out")
        await session.call_tool("create_order", args, read_timeout_seconds=2)
        await session.__aexit__(None, None, None)
        await client_writer.aclose()
        tasks.cancel_scope.cancel()
    await streams.__aexit__(None, None, None)
    return {
        "requestIds": ids,
        "firstResponseLost": dropped,
        "retrySource": "application",
        "protocolVersion": initialized.protocol_version,
    }


if __name__ == "__main__":
    cases = json.load(open(sys.argv[1], encoding="utf-8"))
    case = next(value for value in cases if value["id"] == sys.argv[2])
    print(json.dumps(anyio.run(exercise, case)))
