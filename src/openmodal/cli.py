import sys
import argparse
from openmodal import setup_cmd, chat_cmd, usage_cmd

def main():
    parser = argparse.ArgumentParser(
        description="OpenModal: Your private, serverless OpenAI-compatible API.",
        usage="openmodal <command>"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    parser_setup = subparsers.add_parser("setup", help="Deploy and configure your AI router on Modal")
    
    # Chat command
    parser_chat = subparsers.add_parser("chat", help="Launch terminal chat with your deployed AI")
    
    # Usage command
    parser_usage = subparsers.add_parser("usage", help="View live billing and cost monitor")
    
    args = parser.parse_args()
    
    if args.command == "setup":
        setup_cmd.main()
    elif args.command == "chat":
        chat_cmd.base_url, chat_cmd.api_key = chat_cmd.load_credentials()
        if not chat_cmd.base_url.endswith("/v1"):
            chat_cmd.base_url = f"{chat_cmd.base_url}/v1"
        client = chat_cmd.OpenAI(base_url=chat_cmd.base_url, api_key=chat_cmd.api_key)
        chat_cmd.print_welcome()
        
        try:
            available_models = client.models.list().data
            model_options = [m.id for m in available_models]
        except Exception:
            model_options = ["gemma-4", "llama-3.1", "qwen-3", "phi-4", "deepseek-r1"]
            
        chat_cmd.console.print("\n[bold white]Available Models:[/bold white]")
        for i, m in enumerate(model_options, 1):
            chat_cmd.console.print(f"  {i}. [info]{m}[/info]")
            
        choice = input("\nSelect a model (1-4) [default: 1]: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(model_options):
                model_name = model_options[idx]
            else:
                model_name = model_options[0]
        except:
            model_name = model_options[0]

        chat_cmd.console.print(f"\n[info]Connected to OpenModal Router -> {model_name}[/info]")
        chat_cmd.chat_loop(client, model_name)
    elif args.command == "usage":
        usage_cmd.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
