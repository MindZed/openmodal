import asyncio
from modal.client import _Client
from modal_proto import api_pb2

async def f():
    client = await _Client.from_env()
    req = api_pb2.EndpointListRequest(environment_name='main')
    resp = await client.stub.EndpointList(req)
    print(resp)

asyncio.run(f())
