import modal

# ---------------------------------------------------------------------------
# Container image: CUDA + llama-cpp-python
# ---------------------------------------------------------------------------
llama_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.4.1-devel-ubuntu22.04", add_python="3.12"
    )
    .apt_install("build-essential", "cmake", "ninja-build", "clang", "gcc", "g++", "git")
    .run_commands(
        "CMAKE_ARGS='-DGGML_CUDA=on' pip install huggingface_hub llama-cpp-python==0.3.34 --no-cache-dir",
        gpu="L4"
    )
    .run_commands("mkdir -p /model")
    .run_commands(
        "python -c \"import urllib.request; urllib.request.urlretrieve('https://huggingface.co/unsloth/gemma-4-E4B-it-GGUF/resolve/main/gemma-4-E4B-it-Q3_K_M.gguf', '/model/gemma-4-E4B-it-Q3_K_M.gguf')\""
    )
    .run_commands("pip install fastapi[standard]")
)


# ---------------------------------------------------------------------------
# App + Server
# ---------------------------------------------------------------------------
app = modal.App("gemma-4-e4b-server")

MODEL_PATH = "/model/gemma-4-E4B-it-Q3_K_M.gguf"

@app.cls(
    image=llama_image,
    gpu="L4",
    scaledown_window=40,
    timeout=30 * 60,
    startup_timeout=600,
    secrets=[modal.Secret.from_name("gemma-api-key", require_missing=True)]
)
class Server:
    @modal.enter()
    def start(self):
        from llama_cpp import Llama
        
        print("Loading llama.cpp engine (mmap from disk)...")
        self.llm = Llama(
            model_path=MODEL_PATH,
            n_gpu_layers=-1, # Offload all layers to GPU
            n_ctx=4096,
            verbose=True,
            # Disable mmap so it directly allocates to VRAM if possible, 
            # though default behavior is usually fine.
        )
        print("Model loaded successfully!")

    @modal.method()
    def generate(self, prompt: str):
        # We wrap the prompt in the standard instruction format
        formatted_prompt = f"<bos><start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
        
        outputs = self.llm.create_completion(
            formatted_prompt,
            max_tokens=256,
            stop=["<end_of_turn>", "<eos>"]
        )
        return outputs["choices"][0]["text"]

    @modal.asgi_app()
    def web_app(self):
        import fastapi
        from fastapi import Request
        from fastapi.responses import JSONResponse, StreamingResponse
        from fastapi.middleware.cors import CORSMiddleware
        import json
        
        app = fastapi.FastAPI(title="Gemma-4-E4B OpenAI API")
        
        # Allow CORS so any frontend can call it directly
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.get("/v1/models")
        async def list_models(request: Request):
            import os
            # Many apps (like Halucinatron, Continue.dev) hit /v1/models to test the connection.
            # We must return a valid OpenAI models list.
            auth_header = request.headers.get("Authorization")
            EXPECTED_KEY = os.environ.get("API_KEY", "")
            
            if not EXPECTED_KEY or auth_header != f"Bearer {EXPECTED_KEY}":
                return JSONResponse(status_code=401, content={"error": "Unauthorized: Invalid API Key"})
                
            return {
                "object": "list",
                "data": [
                    {
                        "id": "gemma-4-e4b",
                        "object": "model",
                        "created": 1700000000,
                        "owned_by": "modal-user"
                    }
                ]
            }

        @app.post("/v1/chat/completions")
        async def chat_completions(request: Request):
            import os
            # 1. API Key Auth
            auth_header = request.headers.get("Authorization")
            EXPECTED_KEY = os.environ.get("API_KEY", "")
            
            if not EXPECTED_KEY or auth_header != f"Bearer {EXPECTED_KEY}":
                return JSONResponse(status_code=401, content={"error": "Unauthorized: Invalid API Key"})
                
            body = await request.json()
            messages = body.get("messages", [])
            if not messages:
                return JSONResponse(status_code=400, content={"error": "Missing 'messages' in JSON body"})
                
            stream = body.get("stream", False)
            
            # 2. Native llama.cpp OpenAI-compatible completion
            # This directly mimics the exact OpenAI response structure!
            response = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=body.get("max_tokens", 512),
                temperature=body.get("temperature", 0.7),
                stream=stream
            )
            
            if stream:
                def stream_generator():
                    for chunk in response:
                        yield f"data: {json.dumps(chunk)}\n\n"
                    yield "data: [DONE]\n\n"
                
                return StreamingResponse(stream_generator(), media_type="text/event-stream")
            else:
                return response
            
        return app

