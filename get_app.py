import asyncio
from modal.client import _Client
from modal_proto import api_pb2

async def f():
    client = await _Client.from_env()
    req = api_pb2.AppGetByEnvironmentNameRequest(environment_name='main', name='gemma-4-e4b-it')
    resp = await client.stub.AppGetByEnvironmentName(req)
    print("App details:", resp)

asyncio.run(f())
