import modal
import json
import os
import fastapi
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------------------------
# Base Image & Shared Dependencies
# ---------------------------------------------------------------------------
base_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.4.1-devel-ubuntu22.04", add_python="3.12"
    )
    .apt_install("build-essential", "cmake", "ninja-build", "clang", "gcc", "g++", "git")
    .run_commands(
        "CMAKE_ARGS='-DGGML_CUDA=on' pip install huggingface_hub[cli] llama-cpp-python==0.3.34 fastapi[standard] --no-cache-dir",
        gpu="T4"
    )
    .run_commands("mkdir -p /model")
)

# ---------------------------------------------------------------------------
# Independent Model Snapshots
# ---------------------------------------------------------------------------
gemma_image = base_image.run_commands(
    "huggingface-cli download unsloth/gemma-4-E4B-it-GGUF gemma-4-E4B-it-Q3_K_M.gguf --local-dir /model"
)

llama_image = base_image.run_commands(
    "huggingface-cli download bartowski/Meta-Llama-3.1-8B-Instruct-GGUF Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf --local-dir /model"
)

qwen_image = base_image.run_commands(
    "huggingface-cli download bartowski/Qwen2.5-7B-Instruct-GGUF Qwen2.5-7B-Instruct-Q4_K_M.gguf --local-dir /model"
)

phi_image = base_image.run_commands(
    "huggingface-cli download bartowski/microsoft_Phi-4-mini-instruct-GGUF microsoft_Phi-4-mini-instruct-Q4_K_M.gguf --local-dir /model"
)

deepseek_image = base_image.run_commands(
    "huggingface-cli download unsloth/DeepSeek-R1-Distill-Qwen-14B-GGUF DeepSeek-R1-Distill-Qwen-14B-Q4_K_M.gguf --local-dir /model"
)

app = modal.App("openmodal-router")

# ---------------------------------------------------------------------------
# GPU Worker Classes
# ---------------------------------------------------------------------------
@app.cls(image=gemma_image, gpu="L4", scaledown_window=40, timeout=30 * 60, startup_timeout=600, secrets=[modal.Secret.from_name("openmodal-api-key")])
class GemmaWorker:
    @modal.enter()
    def start(self):
        from llama_cpp import Llama
        print("Loading Gemma 4 E4B (mmap from disk)...")
        self.llm = Llama(model_path="/model/gemma-4-E4B-it-Q3_K_M.gguf", n_gpu_layers=-1, n_ctx=4096, verbose=False)

    @modal.method(is_generator=True)
    def generate_stream(self, messages, max_tokens, temperature):
        for chunk in self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=True):
            yield chunk

    @modal.method()
    def generate(self, messages, max_tokens, temperature):
        return self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=False)

@app.cls(image=llama_image, gpu="T4", scaledown_window=40, timeout=30 * 60, startup_timeout=600, secrets=[modal.Secret.from_name("openmodal-api-key")])
class LlamaWorker:
    @modal.enter()
    def start(self):
        from llama_cpp import Llama
        print("Loading Llama 3.1 8B (mmap from disk)...")
        self.llm = Llama(model_path="/model/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf", n_gpu_layers=-1, n_ctx=4096, verbose=False)

    @modal.method(is_generator=True)
    def generate_stream(self, messages, max_tokens, temperature):
        for chunk in self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=True):
            yield chunk

    @modal.method()
    def generate(self, messages, max_tokens, temperature):
        return self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=False)

@app.cls(image=qwen_image, gpu="T4", scaledown_window=40, timeout=30 * 60, startup_timeout=600, secrets=[modal.Secret.from_name("openmodal-api-key")])
class QwenWorker:
    @modal.enter()
    def start(self):
        from llama_cpp import Llama
        print("Loading Qwen 2.5 7B (mmap from disk)...")
        self.llm = Llama(model_path="/model/Qwen2.5-7B-Instruct-Q4_K_M.gguf", n_gpu_layers=-1, n_ctx=4096, verbose=False)

    @modal.method(is_generator=True)
    def generate_stream(self, messages, max_tokens, temperature):
        for chunk in self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=True):
            yield chunk

    @modal.method()
    def generate(self, messages, max_tokens, temperature):
        return self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=False)

@app.cls(image=phi_image, gpu="T4", scaledown_window=40, timeout=30 * 60, startup_timeout=600, secrets=[modal.Secret.from_name("openmodal-api-key")])
class PhiWorker:
    @modal.enter()
    def start(self):
        from llama_cpp import Llama
        print("Loading Phi 4 Mini (mmap from disk)...")
        self.llm = Llama(model_path="/model/microsoft_Phi-4-mini-instruct-Q4_K_M.gguf", n_gpu_layers=-1, n_ctx=4096, verbose=False)

    @modal.method(is_generator=True)
    def generate_stream(self, messages, max_tokens, temperature):
        for chunk in self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=True):
            yield chunk

    @modal.method()
    def generate(self, messages, max_tokens, temperature):
        return self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=False)

@app.cls(image=deepseek_image, gpu="L4", scaledown_window=40, timeout=30 * 60, startup_timeout=600, secrets=[modal.Secret.from_name("openmodal-api-key")])
class DeepSeekWorker:
    @modal.enter()
    def start(self):
        from llama_cpp import Llama
        print("Loading DeepSeek R1 Distill 14B (mmap from disk)...")
        self.llm = Llama(model_path="/model/DeepSeek-R1-Distill-Qwen-14B-Q4_K_M.gguf", n_gpu_layers=-1, n_ctx=4096, verbose=False)

    @modal.method(is_generator=True)
    def generate_stream(self, messages, max_tokens, temperature):
        for chunk in self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=True):
            yield chunk

    @modal.method()
    def generate(self, messages, max_tokens, temperature):
        return self.llm.create_chat_completion(messages=messages, max_tokens=max_tokens, temperature=temperature, stream=False)

# ---------------------------------------------------------------------------
# CPU API Router (FastAPI)
# ---------------------------------------------------------------------------
@app.function(secrets=[modal.Secret.from_name("openmodal-api-key")])
@modal.asgi_app()
def web_app():
    web = fastapi.FastAPI(title="OpenModal Router API")
    
    web.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @web.get("/v1/models")
    async def list_models(request: Request):
        auth_header = request.headers.get("Authorization")
        EXPECTED_KEY = os.environ.get("API_KEY", "")
        
        if not EXPECTED_KEY or auth_header != f"Bearer {EXPECTED_KEY}":
            return JSONResponse(status_code=401, content={"error": "Unauthorized: Invalid API Key"})
            
        return {
            "object": "list",
            "data": [
                {"id": "gemma-4", "object": "model", "created": 1700000000, "owned_by": "openmodal"},
                {"id": "llama-3.1", "object": "model", "created": 1700000001, "owned_by": "openmodal"},
                {"id": "qwen-3", "object": "model", "created": 1700000002, "owned_by": "openmodal"},
                {"id": "phi-4", "object": "model", "created": 1700000003, "owned_by": "openmodal"},
                {"id": "deepseek-r1", "object": "model", "created": 1700000004, "owned_by": "openmodal"}
            ]
        }

    @web.post("/v1/chat/completions")
    async def chat_completions(request: Request):
        auth_header = request.headers.get("Authorization")
        EXPECTED_KEY = os.environ.get("API_KEY", "")
        
        if not EXPECTED_KEY or auth_header != f"Bearer {EXPECTED_KEY}":
            return JSONResponse(status_code=401, content={"error": "Unauthorized: Invalid API Key"})
            
        body = await request.json()
        messages = body.get("messages", [])
        if not messages:
            return JSONResponse(status_code=400, content={"error": "Missing 'messages' in JSON body"})
            
        model = body.get("model", "gemma-4").lower()
        stream = body.get("stream", False)
        
        if "gemma" in model:
            worker = GemmaWorker()
        elif "llama" in model:
            worker = LlamaWorker()
        elif "qwen" in model:
            worker = QwenWorker()
        elif "phi" in model:
            worker = PhiWorker()
        elif "deepseek" in model:
            worker = DeepSeekWorker()
        else:
            worker = GemmaWorker()
            
        max_tokens = body.get("max_tokens", 512)
        temperature = body.get("temperature", 0.7)
        
        if stream:
            async def stream_generator():
                for chunk in worker.generate_stream.remote_gen(messages, max_tokens, temperature):
                    yield f"data: {json.dumps(chunk)}\n\n"
                yield "data: [DONE]\n\n"
            return StreamingResponse(stream_generator(), media_type="text/event-stream")
        else:
            return worker.generate.remote(messages, max_tokens, temperature)
            
    return web
