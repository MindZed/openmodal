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
Open your terminal in this repository and run the setup script for your operating system:

**On Windows (Command Prompt or PowerShell):**
```cmd
.\install.bat
```

**On macOS / Linux:**
```bash
bash install.sh
```

*The launcher will automatically install Python if it is missing. Then, it installs required packages, opens a browser to authenticate your Modal account, asks you to set an API key, and deploys the AI. It will print out your new OpenAI-compatible Base URL at the end.*

---

## 💬 Terminal Chat Interface
Once deployed, you don't need any third-party apps to talk to your AI. You can instantly launch a hacker-style terminal chat that connects directly to your GPU:

```bash
.\openmodal chat
```
*(On Linux/Mac use `./openmodal chat`)*

It features real-time token streaming, conversation memory, and a `/clear` command to wipe history. It works automatically out of the box because the launcher saves your credentials securely to a local `.env` file.

---

## 📊 Live Usage & Cost Monitor
To ensure you never accidentally blow past your monthly budget, you can instantly check your exact, down-to-the-penny billing directly from Modal's internal servers:

```bash
.\openmodal usage
```
*(On Linux/Mac use `./openmodal usage`)*

---

## 🧪 Third-Party Integration
Because this endpoint is 100% OpenAI-compatible, you can use it in **any** software (like Halucinatron, Continue.dev, AnythingLLM, etc).

You can also run the included testing script if you want to write your own Python integrations:
```bash
python test_openai.py
```
*(Make sure to paste your Base URL and API Key into `test_openai.py` first!)*

---
**Built by Mindzed Technologies (developer - zywfo)**
