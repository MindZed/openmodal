# Gemma 4 E4B Modal Deployer

This repository allows you to easily deploy a fully private, serverless, OpenAI-compatible API for **Gemma 4 E4B** on your own Modal account.

It is heavily optimized with an ultra-fast C++ backend (`llama.cpp`), 4-bit GGUF quantization, and a 40-second idle auto-shutdown to ensure it costs pennies to run.

---

## 🚀 One-Click Quickstart

We've built an automated CLI tool to handle everything (installing dependencies, Modal authentication, configuring secrets, generating API keys, and streaming the deployment logs) in one single step.

### 1. Prerequisites
You need a Modal account with a payment method on file to host the GPU endpoint.
1. Create a free account at [modal.com](https://modal.com)
2. Ensure you have set up a billing method in your account settings (Modal requires this to deploy GPU apps).

### 2. Deploy your API
Open your terminal in this repository and run the setup launcher for your operating system:

**On Windows:**
Double-click `install.bat` or run:
```cmd
install.bat
```

**On macOS / Linux:**
```bash
bash install.sh
```

*The launcher will automatically install Python if it is missing. Then, it installs required packages, opens a browser to authenticate your Modal account, asks you to set an API key, and deploys the AI. It will print out your new OpenAI-compatible Base URL at the end.*

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
