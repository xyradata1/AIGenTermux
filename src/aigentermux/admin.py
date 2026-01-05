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
    
    save_config(config)
    
    console.print("[bold green]Configuration saved successfully![/bold green]")

if __name__ == "__main__":
    main()
