# Gemma 4 E4B Modal Deployer

This repository allows you to easily deploy a fully private, serverless, OpenAI-compatible API for **Gemma 4 E4B** on your own Modal account.

It is heavily optimized with an ultra-fast C++ backend (`llama.cpp`), 4-bit GGUF quantization, and a 40-second idle auto-shutdown to ensure it costs pennies to run.

---

## 🚀 One-Click Quickstart

We've built an automated CLI tool to handle everything (configuring secrets, generating API keys, and streaming the deployment logs) in one step.

### 1. Prerequisites
You need a Modal account to host the GPU endpoint.
1. Create a free account at [modal.com](https://modal.com)
2. Open your terminal and install the Modal python package (and `rich` for the CLI):
   ```bash
   pip install modal rich
   ```
3. Authenticate your laptop to your Modal account:
   ```bash
   modal token new
   ```

### 2. Deploy your API
Run the interactive setup script:
```bash
python setup.py
```
*The CLI will ask you to set an API key, automatically inject it into Modal Secrets, and deploy the AI. It will print out your new OpenAI-compatible Base URL at the end.*

---

## 🧪 Testing your Endpoint
Once deployed, you can use the endpoint in **any** software that supports custom OpenAI APIs (like Halucinatron, Continue.dev, AnythingLLM, etc).

You can also run the included test script to verify it works:
```bash
python test_openai.py
```
*(Make sure to paste your Base URL and API Key into `test_openai.py` first!)*

---
**Built by Mindzed Technologies (developer - zywfo)**
