import os
import re
import sys
import string
import secrets
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.theme import Theme

# Set up a strictly RED theme
custom_theme = Theme({
    "info": "bold red",
    "warning": "bold yellow",
    "danger": "bold red",
    "success": "bold green",
})
console = Console(theme=custom_theme)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    header_text = Text()
    header_text.append("🔥 GEMMA 4 E4B MODAL DEPLOYER 🔥\n", style="bold red")
    header_text.append("Built by Mindzed Technologies (developer - zywfo)\n", style="italic red")
    
    console.print(Panel(header_text, border_style="red", expand=False))

def generate_key(length=16):
    alphabet = string.ascii_letters + string.digits
    return "ZN_" + "".join(secrets.choice(alphabet) for i in range(length - 3))

def get_api_key():
    console.print("\n[info]We need an API Key to secure your OpenAI-compatible endpoint.[/info]")
    choice = Confirm.ask("[red]Do you want to auto-generate a secure cryptographic key?[/red]")
    
    if choice:
        key = generate_key()
        console.print(f"\n[success]Generated Key:[/success] [bold white]{key}[/bold white]")
        return key
    else:
        while True:
            key = Prompt.ask("[red]Enter your custom API Key (max 16 chars)[/red]")
            if len(key) > 16:
                console.print("[warning]Key is too long! Maximum 16 characters.[/warning]")
            elif len(key) == 0:
                console.print("[warning]Key cannot be empty.[/warning]")
            else:
                return key

def setup_modal_secret(api_key):
    console.print("\n[info]=> Injecting your API Key into Modal Secrets...[/info]")
    try:
        # Run the modal cli command to create a secret
        result = subprocess.run(
            ["modal", "secret", "create", "gemma-api-key", f"API_KEY={api_key}"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        if result.returncode == 0:
            console.print("[success]Secret 'gemma-api-key' successfully configured![/success]")
        else:
            console.print(f"[warning]Failed to create secret. You may need to run `modal token new` first.[/warning]\n{result.stderr}")
            sys.exit(1)
    except Exception as e:
        console.print(f"[danger]Error running Modal CLI: {e}[/danger]")
        sys.exit(1)

def deploy_to_modal():
    console.print("\n[info]=> Initiating Modal Deployment (this may take a few minutes if cold building)...[/info]")
    
    base_url = None
    
    # We use Popen to stream the output live to the user, while capturing it to extract the URL
    process = subprocess.Popen(
        ["modal", "deploy", "deploy.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )
    
    for line in iter(process.stdout.readline, ''):
        # Print the line to the terminal so the user sees the live progress
        sys.stdout.write(line)
        sys.stdout.flush()
        
        # Regex to catch the modal.run URL
        match = re.search(r'(https://[a-zA-Z0-9-]+\.modal\.run)', line)
        if match:
            base_url = match.group(1)
            
    process.wait()
    
    if process.returncode != 0:
        console.print("\n[danger]Deployment failed! Please check the logs above.[/danger]")
        sys.exit(1)
        
    return base_url

def main():
    print_header()
    
    api_key = get_api_key()
    setup_modal_secret(api_key)
    base_url = deploy_to_modal()
    
    if base_url:
        console.print("\n")
        
        success_text = Text()
        success_text.append("🚀 DEPLOYMENT SUCCESSFUL! 🚀\n\n", style="bold green")
        success_text.append("Your personal OpenAI-compatible endpoint is live.\n\n", style="white")
        success_text.append(f"Base URL: {base_url}/v1\n", style="bold cyan")
        success_text.append(f"API Key:  {api_key}\n\n", style="bold cyan")
        
        success_text.append("Test it instantly with cURL:\n", style="yellow")
        success_text.append(f"""curl -X POST "{base_url}/v1/chat/completions" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{"model": "gemma-4", "messages": [{{"role": "user", "content": "Hi, tell me a joke."}}]}}'
""", style="white")

        console.print(Panel(success_text, border_style="green", title="[bold green]Ready for Integration[/bold green]"))
    else:
        console.print("\n[warning]Deployment succeeded, but we couldn't automatically parse the URL. Check the logs above![/warning]")

if __name__ == "__main__":
    main()
