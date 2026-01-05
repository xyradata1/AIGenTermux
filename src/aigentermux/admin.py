import sys
from .config import get_config, save_config
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def main():
    console.print("[bold blue]AIGenTermux Admin Configuration[/bold blue]")
    config = get_config()
    
    api_key = Prompt.ask("Enter OpenAI API Key", default=config.get("api_key", ""))
    model = Prompt.ask("Enter Model", default=config.get("model", "gpt-4o-mini"))
    
    config["api_key"] = api_key
    config["model"] = model
    
    # Sync with remote server (Cloudflare)
    # SERVER_URL = "https://your-cloudflare-pages-url.com/set_config"
    # try:
    #     requests.post(SERVER_URL, json=config, timeout=5)
    #     console.print("[bold green]Configuration synced to Cloudflare![/bold green]")
    # except:
    #     console.print("[yellow]Note: Could not sync to server, saved locally only.[/yellow]")

if __name__ == "__main__":
    main()
