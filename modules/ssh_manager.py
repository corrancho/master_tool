"""
Módulo SSH Manager: conexión y ejecución de comandos en VPS remotas.
Usa subprocess/ssh nativo o Paramiko si está disponible.
"""

import subprocess
from pathlib import Path
from app.colors import Colors, success, error, warning, info
from app.config import load_servers, pick_server
from app.utils import require_input


def list_servers():
    """Muestra los servidores configurados en config/servers.json."""
    servers = load_servers()
    if not servers:
        return

    print(f"\n{Colors.BOLD}Servidores configurados:{Colors.RESET}\n")
    for s in servers:
        alias = f" ({s['alias']})" if s.get("alias") else ""
        user = s.get("user", "root")
        port = s.get("port", 22)
        key = s.get("key", "~/.ssh/id_ed25519")
        print(f"  {Colors.CYAN}•{Colors.RESET} {Colors.BOLD}{s['name']}{alias}{Colors.RESET}")
        print(f"      Host: {s['host']}  |  Usuario: {user}  |  Puerto: {port}")
        print(f"      Clave: {key}")
        if s.get("description"):
            print(f"      {Colors.GRAY}{s['description']}{Colors.RESET}")
        print()


def connect_to_server():
    """Abre una sesión SSH interactiva a un servidor seleccionado."""
    server = pick_server()
    if not server:
        return

    cmd = _build_ssh_cmd(server)
    name, host = server["name"], server["host"]
    print(f"\n{info(f'Conectando a {name} ({host})...')}\n")
    print(f"{Colors.GRAY}Comando: {' '.join(cmd)}{Colors.RESET}\n")
    subprocess.run(cmd)


def run_remote_command():
    """Ejecuta un comando en un servidor remoto y muestra la salida."""
    server = pick_server()
    if not server:
        return

    command = require_input("Comando a ejecutar en el servidor remoto")

    cmd = _build_ssh_cmd(server, command=command)
    sname = server["name"]
    print(f"\n{info(f'Ejecutando en {sname}...')}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print(f"{Colors.GREEN}{result.stdout}{Colors.RESET}")
    if result.stderr:
        print(f"{Colors.YELLOW}{result.stderr}{Colors.RESET}")

    if result.returncode == 0:
        print(success("Comando ejecutado correctamente."))
    else:
        print(error(f"El comando terminó con código {result.returncode}."))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_ssh_cmd(server: dict, command: str = None) -> list[str]:
    """Construye la lista de argumentos para un comando ssh."""
    host = server["host"]
    user = server.get("user", "root")
    port = str(server.get("port", 22))
    key = server.get("key") or str(Path.home() / ".ssh" / "id_ed25519")

    cmd = [
        "ssh",
        "-p", port,
        "-i", str(Path(key).expanduser()),
        "-o", "StrictHostKeyChecking=accept-new",
        f"{user}@{host}",
    ]

    if command:
        cmd.append(command)

    return cmd
