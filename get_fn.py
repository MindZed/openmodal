import asyncio
from modal.client import _Client
from modal_proto import api_pb2

async def f():
    client = await _Client.from_env()
    # Let's get the function details using the function_id
    req = api_pb2.FunctionGetRequest(function_id="fu-TTKGopLIuFEOwC4QJPzcD0")
    resp = await client.stub.FunctionGet(req)
    print("Function web_url:", resp.web_url)
    print("Function web_url_info:", resp.web_url_info)

asyncio.run(f())
