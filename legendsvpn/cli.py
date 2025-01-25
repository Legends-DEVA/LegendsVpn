import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from .core import ProxyManager

class VpnCLI:
    def __init__(self):
        self.console = Console(force_terminal=True, legacy_windows=True)
        self.proxy_manager = ProxyManager()

    def display_logo(self):
        """Display ASCII art logo."""
        logo = """
        +----------------------------------+
        |          LegendsVPN              |
        |  Your Proxy Management Tool      |
        +----------------------------------+
        """
        self.console.print(Panel(logo, style="bold blue"))

    def display_proxy_comparison(self, proxy_speeds):
        """Display a table comparing proxy speeds."""
        if not proxy_speeds:
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Proxy")
        table.add_column("Speed (ms)")
        table.add_column("Status")
        
        fastest_proxy = proxy_speeds[0][1]  # First proxy is fastest due to sorting
        
        for speed, proxy in proxy_speeds:
            table.add_row(
                proxy,
                f"{speed:.0f}ms",
                "[green]Fastest[/green]" if proxy == fastest_proxy else ""
            )
        
        self.console.print("\nSpeed Test Results:")
        self.console.print(table)

    def connect_to_proxy(self, proxy):
        """Display connection information for a proxy."""
        try:
            # Get original IP info
            original_ip = self.proxy_manager.get_current_ip_info()
            
            # Get proxy IP info
            proxy_ip_info = self.proxy_manager.get_proxy_location(proxy)
            
            if proxy_ip_info:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Status")
                table.add_column("Original Location")
                table.add_column("Proxy Location")
                
                table.add_row(
                    "[green]Connected[/green]",
                    f"{original_ip.get('city', 'Unknown')}, {original_ip.get('country', 'Unknown')}",
                    f"{proxy_ip_info.get('city', 'Unknown')}, {proxy_ip_info.get('country', 'Unknown')}"
                )
                
                self.console.print(table)
                return True
                
        except Exception as e:
            self.console.print(f"[red]Failed to connect to proxy: {str(e)}[/red]")
            return False

    def run(self):
        """Run the main CLI interface."""
        while True:
            self.display_logo()
            menu = """
            [1] Fetch new proxies
            [2] Connect to fastest proxy
            [3] Exit
            """
            self.console.print(Panel(menu, title="Menu", style="cyan"))
            
            try:
                choice = input("Enter your choice (1-3): ").strip()
                
                if choice == "1":
                    with self.console.status("[bold green]Fetching proxies..."):
                        proxies = self.proxy_manager.fetch_proxies()
                    self.console.print(f"[green]Successfully fetched {len(proxies)} proxies[/green]")
                
                elif choice == "2":
                    with self.console.status("[bold green]Finding fastest proxy..."):
                        working_proxies = self.proxy_manager.find_working_proxies(min_working=3)
                    
                    if working_proxies:
                        self.display_proxy_comparison(working_proxies)
                        fastest_proxy = working_proxies[0][1]
                        self.connect_to_proxy(fastest_proxy)
                    else:
                        self.console.print("[red]No working proxies found[/red]")
                
                elif choice == "3":
                    self.console.print("[yellow]Goodbye![/yellow]")
                    break
                
                else:
                    self.console.print("[red]Invalid choice. Please enter 1, 2, or 3.[/red]")
                    continue
                
                input("\nPress Enter to continue...")
                self.console.clear()
            
            except EOFError:
                break
            except KeyboardInterrupt:
                self.console.print("[yellow]\nGoodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]An error occurred: {str(e)}[/red]")

def main():
    cli = VpnCLI()
    cli.run()

if __name__ == "__main__":
    main()
