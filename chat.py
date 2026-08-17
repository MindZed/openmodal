import os
import sys
import subprocess
from dotenv import load_dotenv

# --- AUTO INSTALL DEPENDENCIES ---
def install_dependencies():
    try:
        import rich
        import openai
    except ImportError:
        print("Installing required dependencies (rich, openai, python-dotenv)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "openai", "python-dotenv", "--quiet"])

install_dependencies()

# Set UTF-8 encoding for Windows console to prevent charmap crashes
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.theme import Theme
from rich.markdown import Markdown

custom_theme = Theme({
    "user": "bold cyan",
    "ai": "bold red",
    "system": "italic dim white",
    "error": "bold red"
})
console = Console(theme=custom_theme)

def load_credentials():
    load_dotenv()
    base_url = os.getenv("OPENAI_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not base_url or not api_key:
        console.print("[error]✖ Credentials not found![/error]")
        console.print("[system]Please run 'python setup.py' or 'install.bat' first to deploy your endpoint and generate a .env file.[/system]")
        sys.exit(1)
        
    return base_url, api_key

def print_welcome():
    os.system('cls' if os.name == 'nt' else 'clear')
    welcome_text = Text()
    welcome_text.append("🔥 OPENMODAL CHAT 🔥\n", style="bold red")
    welcome_text.append("Connected directly to your private serverless GPU.\n\n", style="white")
    welcome_text.append("Commands:\n", style="bold cyan")
    welcome_text.append("  /bye   ", style="bold white")
    welcome_text.append("- Exit the chat\n", style="italic dim white")
    welcome_text.append("  /clear ", style="bold white")
    welcome_text.append("- Wipe conversation memory and start fresh\n", style="italic dim white")
    
    console.print(Panel(welcome_text, border_style="red"))

def chat_loop(client, model_name):
    
    # Initialize conversation history
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant running on a private Modal serverless GPU."}
    ]
    
    while True:
        try:
            # Get user input
            console.print("\n[user]You:[/user]", end=" ")
            user_input = input().strip()
            
            if not user_input:
                continue
                
            # Handle commands
            if user_input.lower() in ['/bye', 'exit', 'quit']:
                console.print("\n[system]Disconnecting... Goodbye![/system]")
                break
                
            if user_input.lower() == '/clear':
                messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
                console.print("[system]✔ Memory cleared. Starting a fresh conversation.[/system]")
                continue
            
            # Append user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Request response from Modal
            console.print(f"\n[ai]{model_name}:[/ai] ", end="")
            
            # Stream the response
            stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    # Print token directly to terminal
                    sys.stdout.write(content)
                    sys.stdout.flush()
            
            print() # New line after stream finishes
            
            # Save assistant response to history
            messages.append({"role": "assistant", "content": full_response})
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\n[system]Disconnecting... Goodbye![/system]")
            break
        except Exception as e:
            console.print(f"\n[error]✖ Error communicating with endpoint: {e}[/error]")
            # Remove the last user message so they can try again without breaking history
            messages.pop()

if __name__ == "__main__":
    base_url, api_key = load_credentials()
    
    if not base_url.endswith("/v1"):
        base_url = f"{base_url}/v1"
        
    client = OpenAI(base_url=base_url, api_key=api_key)
    
    print_welcome()
    
    # Automatically fetch available models from our router
    try:
        available_models = client.models.list().data
        model_options = [m.id for m in available_models]
    except Exception as e:
        # Fallback if endpoint is unreachable or booting
        model_options = ["gemma-4", "llama-3.1", "qwen-3", "phi-4", "deepseek-r1"]
    
    console.print("\n[bold white]Available Models:[/bold white]")
    for i, m in enumerate(model_options, 1):
        console.print(f"  {i}. [info]{m}[/info]")
        
    choice = input("\nSelect a model (1-4) [default: 1]: ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(model_options):
            model_name = model_options[idx]
        else:
            model_name = model_options[0]
    except:
        model_name = model_options[0]

    console.print(f"\n[info]Connected to OpenModal Router -> {model_name}[/info]")
    chat_loop(client, model_name)
