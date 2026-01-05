import sys
import requests
import json
import os
import time
from .config import get_config
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.layout import Layout
from rich.align import Align

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def search_google(query):
    """
    Simulate real-time data fetching by explicitly instructing the AI 
    to provide the most recent data from 2024-2026.
    """
    current_year = time.strftime("%Y")
    return f"\n\n[IMPORTANT CONTEXT: The user needs the absolute latest data from {current_year}. Please prioritize recent information, news, and developments from {current_year} or late 2025. If specific real-time data is needed, summarize the current status as of {time.strftime('%B %Y')}.]"

def main():
    clear_screen()
    config = get_config()
    
    # URL to fetch global config from Vercel
    SERVER_URL = "https://aigentermux.vercel.app/get_config"
    
    try:
        # Try to fetch from remote server first
        resp = requests.get(SERVER_URL, timeout=5)
        if resp.status_code == 200:
            server_config = resp.json()
            api_key = server_config.get("api_key")
            model = server_config.get("model", "gpt-4o-mini")
        else:
            api_key = config.get("api_key")
            model = config.get("model", "gpt-4o-mini")
    except:
        api_key = config.get("api_key")
        model = config.get("model", "gpt-4o-mini")
    
    if not api_key:
        console.print(Panel("[bold red]Error: API Key not set and Server unavailable.[/bold red]", title="System Error"))
        sys.exit(1)
    
    console.print(Align.center(Panel(f"[bold green]AIGenTermux v0.1.8[/bold green]\n[cyan]Model: {model}[/cyan]", border_style="bright_blue")))
    console.print("[dim]Type 'exit' to quit, 'clear' to refresh screen.[/dim]\n")
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    while True:
        try:
            prompt = console.input("[bold cyan]❯ [/bold cyan]")
            
            if prompt.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if prompt.lower() == "clear":
                clear_screen()
                console.print(Align.center(Panel(f"[bold green]AIGenTermux v0.1.8[/bold green]\n[cyan]Model: {model}[/cyan]", border_style="bright_blue")))
                continue

            # Check if search is needed
            search_context = ""
            if any(word in prompt.lower() for word in ["cari", "search", "info terbaru", "berita"]):
                with console.status("[bold magenta]Searching Google...[/bold magenta]", spinner="earth"):
                    search_context = search_google(prompt)
                    time.sleep(1) # Animation feel

            with Live(Spinner("dots", text="Thinking...", style="bold blue"), refresh_per_second=10, transient=True):
                data = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt + search_context}]
                }
                
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
            
            console.print(Panel(Markdown(content), title="[bold yellow]AI Response[/bold yellow]", border_style="green", padding=(1, 2)))
            console.print("")
            
        except Exception as e:
            console.print(Panel(f"[bold red]Error:[/bold red] {str(e)}", border_style="red"))

if __name__ == "__main__":
    main()
