import os
import re
import sys
import string
import secrets
import subprocess

# --- AUTO INSTALL DEPENDENCIES ---
def install_dependencies():
    try:
        import rich
        import modal
    except ImportError:
        print("Installing required dependencies (modal, rich)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "modal", "rich", "--quiet"])

install_dependencies()

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.theme import Theme


# Set up a sturdy, professional RED theme
custom_theme = Theme({
    "info": "bold white",
    "warning": "bold yellow",
    "danger": "bold red",
    "success": "bold green",
    "highlight": "bold red"
})
console = Console(theme=custom_theme)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    
    openmodal_ascii = """[bold red]
 ::::::::  :::::::::  :::::::::: ::::    ::: ::::    ::::   ::::::::  :::::::::      :::     :::        
:┼:    :┼: :┼:    :┼: :┼:        :┼:┼:   :┼: ┼:┼:┼: :┼:┼:┼ :┼:    :┼: :┼:    :┼:   :┼: :┼:   :┼:        
┼:┼    ┼:┼ ┼:┼    ┼:┼ ┼:┼        :┼:┼:┼  ┼:┼ ┼:┼ ┼:┼:┼ ┼:┼ ┼:┼    ┼:┼ ┼:┼    ┼:┼  ┼:┼   ┼:┼  ┼:┼        
┼#┼    ┼:┼ ┼#┼┼:┼┼#┼  ┼#┼┼:┼┼#   ┼#┼ ┼:┼ ┼#┼ ┼#┼  ┼:┼  ┼#┼ ┼#┼    ┼:┼ ┼#┼    ┼:┼ ┼#┼┼:┼┼#┼┼: ┼#┼        
┼#┼    ┼#┼ ┼#┼        ┼#┼        ┼#┼  ┼#┼#┼# ┼#┼       ┼#┼ ┼#┼    ┼#┼ ┼#┼    ┼#┼ ┼#┼     ┼#┼ ┼#┼        
#┼#    #┼# #┼#        #┼#        #┼#   #┼#┼# #┼#       #┼# #┼#    #┼# #┼#    #┼# #┼#     #┼# #┼#        
 ########  ###        ########## ###    #### ###       ###  ########  #########  ###     ### ########## 
[/bold red]"""

    mindzed_ascii = """[bold red]
▄▄▄              ▄▄▄
 ▄▄▄▄▄▄       ▄▄▄▀▄▄
▄▄  ▀▄▄▄▄    ▀▀▀  ▄▄
▄▄     ▀▄▄▄▄      ▄    [/bold red][bold white]Mindzed Technologies[/bold white][bold red]
     ▄▄    ▀▄▄▄▄  ▄
 ▄▄▄▀▀▀      ▀▀▀▄▄▄▄
▄▄▄▀            ▀▀▄▄
[/bold red]"""

    header_text = Text.from_markup(f"{openmodal_ascii}\n{mindzed_ascii}\n[bold white]Serverless OpenAI-Compatible Endpoints[/bold white]\n[italic dim red]Powered by Gemma 4 E4B & Modal[/italic dim red]")
    
    console.print(Panel(header_text, border_style="red", padding=(1, 4), title="[bold white]INITIALIZATION[/bold white]"))


def generate_key(length=16):
    alphabet = string.ascii_letters + string.digits
    return "ZN_" + "".join(secrets.choice(alphabet) for i in range(length - 3))

def get_api_key():
    console.print("\n[bold white]▶ SECURITY CONFIGURATION[/bold white]")
    console.print("[info]An API Key is required to secure your endpoint from unauthorized access.[/info]\n")
    
    choice = Confirm.ask("[bold red]? Do you want to auto-generate a secure cryptographic key?[/bold red]")
    
    if choice:
        key = generate_key()
        console.print(f"\n[success]✔ Generated Secure Key:[/success] [bold white]{key}[/bold white]")
        return key
    else:
        while True:
            key = Prompt.ask("\n[bold red]➔ Enter your custom API Key (max 16 chars)[/bold red]")
            if len(key) > 16:
                console.print("[warning]⚠ Key is too long! Maximum 16 characters.[/warning]")
            elif len(key) == 0:
                console.print("[warning]⚠ Key cannot be empty.[/warning]")
            else:
                return key

def setup_modal_secret(api_key):
    console.print("\n[bold white]▶ MODAL VAULT INJECTION[/bold white]")
    console.print("[info]Injecting API key into remote Modal Secrets...[/info]")
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
    console.print("\n[bold white]▶ REMOTE DEPLOYMENT[/bold white]")
    console.print("[info]Initiating deployment to Modal infrastructure...[/info]")
    console.print("[italic dim](This may take a few minutes during initial cold builds)[/italic dim]\n")
    
    base_url = None
    
    process = subprocess.Popen(
        ["modal", "deploy", "deploy.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )
    
    for line in iter(process.stdout.readline, ''):
        # Add a subtle prefix to stream output to make it look boxed/sturdy
        sys.stdout.write(f"  │ {line}")
        sys.stdout.flush()
        
        match = re.search(r'(https://[a-zA-Z0-9-]+\.modal\.run)', line)
        if match:
            base_url = match.group(1)
            
    process.wait()
    
    if process.returncode != 0:
        console.print("\n[danger]✖ Deployment failed. Check the logs above.[/danger]")
        sys.exit(1)
        
    return base_url

def ensure_modal_auth():
    console.print("\n[bold white]▶ AUTHENTICATION[/bold white]")
    console.print("[info]Checking Modal profile...[/info]")
    
    result = subprocess.run(["modal", "profile", "current"], capture_output=True, text=True)
    if result.returncode != 0:
        console.print("[warning]⚠ No active Modal session found.[/warning]")
        console.print("[info]Opening browser to authenticate... Please authorize the CLI.[/info]")
        
        auth_result = subprocess.run(["modal", "token", "new"])
        
        if auth_result.returncode != 0:
            console.print("[danger]✖ Authentication failed or cancelled.[/danger]")
            sys.exit(1)
            
        console.print("[success]✔ Successfully authenticated![/success]")
    else:
        console.print("[success]✔ Session verified.[/success]")


def main():
    print_header()
    ensure_modal_auth()
    
    api_key = get_api_key()
    setup_modal_secret(api_key)
    base_url = deploy_to_modal()
    
    if base_url:
        console.print("\n")
        
        success_text = Text()
        success_text.append("Your OpenModal API is live and fully OpenAI-compatible.\n\n", style="white")
        success_text.append("BASE URL: ", style="bold red")
        success_text.append(f"{base_url}/v1\n", style="bold white")
        success_text.append("API KEY:  ", style="bold red")
        success_text.append(f"{api_key}\n\n", style="bold white")
        
        success_text.append("CURL TEST COMMAND:\n", style="bold yellow")
        success_text.append(f"""curl -X POST "{base_url}/v1/chat/completions" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{"model": "gemma-4", "messages": [{{"role": "user", "content": "Hi, tell me a joke."}}]}}'
""", style="italic dim white")

        console.print(Panel(success_text, border_style="red", title="[bold white]✔ DEPLOYMENT SUCCESSFUL[/bold white]", padding=(1, 2)))
    else:
        console.print("\n[warning]⚠ Deployment succeeded, but the URL could not be parsed automatically.[/warning]")

if __name__ == "__main__":
    main()
