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
        import openai
        import dotenv
        import questionary
    except ImportError:
        print("Installing required dependencies (modal, rich, openai, python-dotenv, questionary)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "modal", "rich", "openai", "python-dotenv", "questionary", "--quiet"])

install_dependencies()

# Set UTF-8 encoding for Windows console to prevent charmap crashes
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.theme import Theme
from rich.table import Table


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

    mindzed_logo_ansi = "\033[38;2;237;41;68;48;2;238;40;68m▄\033[38;2;240;43;67;48;2;245;41;70m▄\033[38;2;235;40;65;49m▄\033[49m              \033[38;2;235;41;65;49m▄\033[38;2;239;43;68;48;2;245;39;69m▄\033[38;2;236;41;68;48;2;238;40;68m▄\033[m\n\033[48;2;236;41;67m \033[38;2;236;42;66;48;2;236;41;67m▄\033[38;2;237;40;66;48;2;237;41;68m▄\033[38;2;234;41;67;48;2;245;43;69m▄\033[38;2;236;41;68;49m▄\033[38;2;239;41;69;49m▄\033[38;2;234;42;64;49m▄\033[49m       \033[38;2;236;39;64;49m▄\033[38;2;238;41;69;49m▄\033[38;2;235;41;66;48;2;237;46;65m▄\033[49;38;2;237;41;68m▀\033[38;2;218;20;37;48;2;226;36;59m▄\033[38;2;235;41;66;48;2;235;40;66m▄\033[m\n\033[38;2;236;40;67;48;2;236;41;67m▄\033[38;2;237;43;67;48;2;236;42;67m▄\033[49m  \033[49;38;2;238;41;68m▀\033[38;2;196;39;59;48;2;236;40;67m▄\033[38;2;233;41;67;48;2;236;41;68m▄\033[38;2;236;40;66;48;2;242;40;67m▄\033[38;2;236;43;69;49m▄\033[49m    \033[49;38;2;215;27;54m▀\033[49;38;2;230;40;63m▀\033[49;38;2;222;33;55m▀\033[49m  \033[38;2;234;21;37;48;2;223;21;37m▄\033[38;2;235;41;67;48;2;235;40;67m▄\033[m\n\033[38;2;236;41;66;48;2;236;41;67m▄\033[38;2;237;42;67;48;2;236;43;67m▄\033[49m     \033[49;38;2;236;41;68m▀\033[38;2;239;34;51;48;2;235;41;66m▄\033[38;2;236;43;68;48;2;236;42;66m▄\033[38;2;236;41;67;48;2;236;40;66m▄\033[38;2;235;43;67;49m▄\033[49m      \033[38;2;228;21;36;48;2;238;22;39m▄\033[48;2;235;41;66m \033[m\n\033[48;2;236;41;67m \033[48;2;236;42;67m \033[49m   \033[38;2;235;40;66;49m▄\033[38;2;234;40;66;49m▄\033[49m    \033[49;38;2;235;41;66m▀\033[38;2;234;41;68;48;2;236;40;67m▄\033[38;2;234;40;66;48;2;236;40;68m▄\033[38;2;232;41;65;49m▄\033[38;2;234;40;68;49m▄\033[49m  \033[38;2;218;20;37;48;2;218;21;36m▄\033[48;2;235;41;66m \033[m\n\033[48;2;236;41;67m \033[38;2;235;41;68;48;2;237;42;67m▄\033[38;2;235;41;68;49m▄\033[38;2;235;41;67;49m▄\033[49;38;2;236;42;69m▀\033[49;38;2;236;43;68m▀\033[49;38;2;234;42;64m▀\033[49m      \033[49;38;2;225;41;61m▀\033[49;38;2;235;41;67m▀\033[49;38;2;236;41;67m▀\033[38;2;235;40;67;48;2;236;40;67m▄\033[38;2;237;41;67;48;2;220;23;35m▄\033[38;2;234;36;59;48;2;218;21;37m▄\033[38;2;235;41;67;48;2;235;41;66m▄\033[m\n\033[38;2;236;41;66;48;2;236;40;67m▄\033[38;2;236;44;68;48;2;234;41;67m▄\033[38;2;216;38;59;48;2;234;42;66m▄\033[49;38;2;240;45;60m▀\033[49m            \033[49;38;2;240;45;60m▀\033[49;38;2;236;41;67m▀\033[38;2;229;44;70;48;2;236;41;67m▄\033[38;2;236;40;67;48;2;236;41;67m▄\033[m\n"
    logo_render = Text.from_ansi(mindzed_logo_ansi)

    # Use a Table layout to position the logo beside the text
    company_table = Table(show_header=False, box=None, padding=(0, 2))
    company_table.add_column("Logo")
    company_table.add_column("Text", vertical="middle")
    company_table.add_row(
        logo_render,
        Text("Mindzed Technologies\nServerless OpenAI-Compatible Endpoints\nPowered by Gemma 4 E4B & Modal", style="bold white")
    )

    header_text = Text.from_markup(f"{openmodal_ascii}")
    
    # We create an outer group or just print them all inside a panel.
    from rich.console import Group
    panel_group = Group(header_text, company_table)
    
    console.print(Panel(panel_group, border_style="red", padding=(1, 4), title="[bold white]INITIALIZATION[/bold white]"))


def generate_key(length=16):
    alphabet = string.ascii_letters + string.digits
    return "ZN_" + "".join(secrets.choice(alphabet) for i in range(length - 3))

def get_installed_models():
    import dotenv
    import questionary
    console.print("\n[bold white]▶ MODEL SELECTION[/bold white]")
    console.print("[info]Select which AI models you want to host on your OpenModal Router.[/info]\n")
    
    existing_models = "gemma-4"
    if os.path.exists(".env"):
        existing_models = dotenv.get_key(".env", "INSTALLED_MODELS") or "gemma-4"
        
    installed_list = existing_models.split(",")
    
    model_choices = [
        {"name": "Gemma 4 E4B (L4 GPU)", "value": "gemma-4"},
        {"name": "DeepSeek R1 Distill 14B (L4 GPU)", "value": "deepseek-r1"},
        {"name": "Llama 3.1 8B (T4 GPU)", "value": "llama-3.1"},
        {"name": "Qwen 3 8B (T4 GPU)", "value": "qwen-3"},
        {"name": "Phi 4 Mini (T4 GPU)", "value": "phi-4"},
    ]
    
    # Mark previously installed models as checked
    for choice in model_choices:
        if choice["value"] in installed_list:
            choice["checked"] = True

    while True:
        selected = questionary.checkbox(
            "Use Spacebar to select, and Enter to confirm:",
            choices=[questionary.Choice(c["name"], value=c["value"], checked=c.get("checked", False)) for c in model_choices],
            style=questionary.Style([('qmark', 'fg:#ff0000 bold'), ('question', 'bold'), ('selected', 'fg:#ff0000 bold')])
        ).ask()
        
        if not selected:
            console.print("[warning]⚠ You must select at least one model.[/warning]")
        else:
            selected_str = ",".join(selected)
            console.print(f"\n[success]✔ Selected Models: {selected_str}[/success]")
            return selected_str

def get_api_key():
    import dotenv
    console.print("\n[bold white]▶ SECURITY CONFIGURATION[/bold white]")
    console.print("[info]An API Key is required to secure your endpoint from unauthorized access.[/info]\n")
    
    # Check if an API key is already configured
    existing_key = None
    if os.path.exists(".env"):
        existing_key = dotenv.get_key(".env", "API_KEY")
        
    if existing_key:
        masked_key = existing_key[:4] + "*" * 8 + existing_key[-4:]
        use_existing = Confirm.ask(f"[bold red]? Existing API Key found ({masked_key}). Do you want to reuse it?[/bold red]")
        if use_existing:
            return existing_key
            
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

def setup_modal_secret(api_key, installed_models):
    console.print("\n[bold white]▶ MODAL VAULT INJECTION[/bold white]")
    console.print("[info]Injecting secrets into remote Modal Vault...[/info]")
    try:
        env_vars = os.environ.copy()
        env_vars["PYTHONIOENCODING"] = "utf-8"
        
        # We pass both API_KEY and INSTALLED_MODELS to Modal
        result = subprocess.run(
            ["modal", "secret", "create", "openmodal-api-key", f"API_KEY={api_key}", f"INSTALLED_MODELS={installed_models}", "--force"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env_vars
        )
        if result.returncode == 0:
            console.print("[success]Secret 'openmodal-api-key' successfully configured![/success]")
        else:
            console.print(f"[warning]Failed to create secret. You may need to run `modal token new` first.[/warning]\n{result.stderr}")
            sys.exit(1)
    except Exception as e:
        console.print(f"[danger]Error running Modal CLI: {e}[/danger]")
        sys.exit(1)

def deploy_to_modal(installed_models):
    console.print("\n[bold white]▶ REMOTE DEPLOYMENT[/bold white]")
    console.print("[info]Initiating deployment to Modal infrastructure...[/info]")
    console.print("[italic dim](This may take a few minutes during initial cold builds)[/italic dim]\n")
    
    base_url = None
    
    env_vars = os.environ.copy()
    env_vars["PYTHONIOENCODING"] = "utf-8"
    env_vars["INSTALLED_MODELS"] = installed_models
    
    process = subprocess.Popen(
        ["modal", "deploy", "deploy.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env_vars
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
    
    env_vars = os.environ.copy()
    env_vars["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(["modal", "profile", "current"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env_vars)
    if result.returncode != 0:
        console.print("[warning]⚠ No active Modal session found.[/warning]")
        console.print("[info]Opening browser to authenticate... Please authorize the CLI.[/info]")
        
        auth_result = subprocess.run(["modal", "token", "new"], env=env_vars)
        
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
    installed_models = get_installed_models()
    setup_modal_secret(api_key, installed_models)
    base_url = deploy_to_modal(installed_models)
    
    if base_url:
        console.print("\n")
        
        success_text = Text()
        success_text.append("Your OpenModal API is live and fully OpenAI-compatible.\n\n", style="white")
        success_text.append("BASE URL: ", style="bold red")
        success_text.append(f"{base_url}/v1\n", style="bold white")
        success_text.append("API KEY:  ", style="bold red")
        success_text.append(f"{api_key}\n", style="bold white")
        success_text.append("MODELS:   ", style="bold red")
        success_text.append(f"{installed_models}\n\n", style="bold white")
        
        success_text.append("CURL TEST COMMAND:\n", style="bold yellow")
        success_text.append(f"""curl -X POST "{base_url}/v1/chat/completions" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{"model": "{installed_models.split(',')[0]}", "messages": [{{"role": "user", "content": "Hi, tell me a joke."}}]}}'
""", style="italic dim white")

        console.print(Panel(success_text, border_style="red", title="[bold white]✔ DEPLOYMENT SUCCESSFUL[/bold white]", padding=(1, 2)))
        
        # Save credentials for chat.py
        try:
            with open(".env", "w") as f:
                f.write(f"OPENAI_BASE_URL={base_url}/v1\n")
                f.write(f"OPENAI_API_KEY={api_key}\n")
                f.write(f"API_KEY={api_key}\n")
                f.write(f"INSTALLED_MODELS={installed_models}\n")
            console.print("[italic dim white]Credentials saved to .env for zero-config chat.[/italic dim white]\n")
        except Exception as e:
            console.print(f"[warning]Could not save .env file: {e}[/warning]")
    else:
        console.print("\n[warning]⚠ Deployment succeeded, but the URL could not be parsed automatically.[/warning]")

if __name__ == "__main__":
    main()
