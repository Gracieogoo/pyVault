import getpass
import sys
import click
from rich.console import Console
from rich.table import Table

def getpass_asterisk(prompt="Password: "):
    if sys.platform == "win32":
        import msvcrt
        sys.stdout.write(prompt)
        sys.stdout.flush()
        pw = []
        while True:
            c = msvcrt.getch()
            if c in (b'\r', b'\n'):
                sys.stdout.write('\n')
                break
            if c == b'\x03':
                raise KeyboardInterrupt
            if c == b'\x08':
                if len(pw) > 0:
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                    pw.pop()
            elif c >= b' ' and c <= b'~':
                sys.stdout.write('*')
                sys.stdout.flush()
                pw.append(c.decode('utf-8', errors='ignore'))
        return "".join(pw)
    else:
        return getpass.getpass(prompt)


from src.config import SALT_PATH
from src.utils.crypto_utils import get_or_create_salt, derive_key
from src.password_manager.manager import VaultManager, generate_password
from src.file_encryption.crypto import encrypt_file, decrypt_file
from src.network_tools.scanner import port_scan, get_ip_info
from src.utils.security_analysis import analyze_password_strength, get_file_hash

console = Console()

@click.group()
def cli():
    """pyVault - A comprehensive python security tool kit."""
    pass

def get_vault_manager():
    salt = get_or_create_salt(SALT_PATH)
    master_password = getpass_asterisk("Enter Master Password: ")
    key = derive_key(master_password, salt)
    return VaultManager(key)

# -----------------
# PASSWORD COMMANDS
# -----------------
@cli.group()
def vault():
    """Manage passwords in secure vault."""
    pass

@vault.command("add")
@click.argument("service")
@click.argument("username")
@click.option("--password", "-p", help="Password (leave blank to generate)", default=None)
def add_password_cmd(service, username, password):
    if not password:
        password = generate_password()
        console.print(f"[green]Generated secure password: {password}[/green]")
    try:
        manager = get_vault_manager()
        manager.add_password(service, username, password)
        console.print(f"[bold green]Successfully added {service} to vault.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

@vault.command("get")
@click.argument("service")
def get_password_cmd(service):
    try:
        manager = get_vault_manager()
        entry = manager.get_password(service)
        if entry:
            table = Table(title=f"Credentials for {service}")
            table.add_column("Username", style="cyan")
            table.add_column("Password", style="magenta")
            table.add_row(entry["username"], entry["password"])
            console.print(table)
        else:
            console.print(f"[yellow]No entry found for {service}[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

@vault.command("list")
def list_cmd():
    try:
        manager = get_vault_manager()
        services = manager.list_services()
        if not services:
            console.print("[yellow]Vault is empty.[/yellow]")
        else:
            for s in services:
                console.print(f"- [cyan]{s}[/cyan]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

# -----------------
# CRYPTO COMMANDS
# -----------------
@cli.group()
def crypto():
    """File encryption and decryption."""
    pass

@crypto.command("encrypt")
@click.argument("filepath")
def encrypt_cmd(filepath):
    salt = get_or_create_salt(SALT_PATH)
    password = getpass_asterisk("Enter encryption password: ")
    key = derive_key(password, salt)
    try:
        out = encrypt_file(filepath, key)
        console.print(f"[green]Successfully encrypted to: {out}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@crypto.command("decrypt")
@click.argument("filepath")
def decrypt_cmd(filepath):
    salt = get_or_create_salt(SALT_PATH)
    password = getpass_asterisk("Enter decryption password: ")
    key = derive_key(password, salt)
    try:
        out = decrypt_file(filepath, key)
        console.print(f"[green]Successfully decrypted to: {out}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

# -----------------
# NETWORK COMMANDS
# -----------------
@cli.group()
def network():
    """Network scanning tools."""
    pass

@network.command("scan")
@click.argument("target")
@click.option("--start", default=1, help="Start port")
@click.option("--end", default=1024, help="End port")
def scan_cmd(target, start, end):
    console.print(f"[cyan]Scanning {target} from port {start} to {end}...[/cyan]")
    ports = port_scan(target, start, end)
    if ports:
        console.print(f"[green]Open ports: {', '.join(map(str, ports))}[/green]")
    else:
        console.print("[yellow]No open ports found.[/yellow]")

@network.command("ipinfo")
@click.argument("ip")
def ipinfo_cmd(ip):
    info = get_ip_info(ip)
    if info:
        for k, v in info.items():
            console.print(f"[bold]{k}:[/bold] {v}")
    else:
        console.print("[red]Could not retrieve info.[/red]")

# -----------------
# SECURITY ANALYSIS
# -----------------
@cli.group()
def check():
    """Security analysis tools."""
    pass

@check.command("password")
@click.argument("password")
def check_pwd(password):
    result = analyze_password_strength(password)
    color = "green" if result["strength"] == "Strong" else "yellow" if result["strength"] == "Moderate" else "red"
    console.print(f"Strength: [{color}]{result['strength']}[/{color}] ({result['score']}/{result['max_score']})")
    for f in result["feedback"]:
        console.print(f"- [yellow]{f}[/yellow]")

@check.command("hash")
@click.argument("filepath")
def check_hash(filepath):
    file_hash = get_file_hash(filepath)
    if file_hash:
        console.print(f"[cyan]SHA-256:[/cyan] {file_hash}")
    else:
        console.print(f"[red]Could not read file: {filepath}[/red]")

if __name__ == "__main__":
    cli()
