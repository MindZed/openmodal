import asyncio
from modal.client import _Client
from modal_proto import api_pb2

async def f():
    client = await _Client.from_env()
    tags = ["web", "serve", "vllm_serve", "vllm_inference", "inference", "api", "chat", "completions"]
    for tag in tags:
        req = api_pb2.FunctionGetRequest(app_name="gemma-4-e4b-it", environment_name="main", object_tag=tag)
        try:
            resp = await client.stub.FunctionGet(req)
            print(f"Found tag '{tag}': {resp.web_url}")
        except Exception as e:
            pass

asyncio.run(f())
