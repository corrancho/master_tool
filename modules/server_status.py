"""
Módulo Server Status: información del sistema local o remoto.
"""

import subprocess
from app.colors import Colors, success, error, info
from app.runner import run, run_output
from app.config import pick_server
from modules.ssh_manager import _build_ssh_cmd


def _run_cmd(cmd: str, server: dict = None) -> str:
    """Ejecuta un comando local o remoto y devuelve su salida."""
    if server:
        ssh_cmd = _build_ssh_cmd(server, command=cmd)
        result = subprocess.run(ssh_cmd, capture_output=True, text=True)
        return (result.stdout + result.stderr).strip()
    else:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return (result.stdout + result.stderr).strip()


def _pick_target() -> dict | None:
    """Pregunta si el usuario quiere info local o de un servidor remoto."""
    mode = input(
        f"{Colors.CYAN}¿Local [L] o remoto [R]? [L]: {Colors.RESET}"
    ).strip().upper() or "L"
    if mode == "R":
        return pick_server()
    return None


def show_uptime():
    """Muestra uptime del sistema."""
    server = _pick_target()
    label = server["name"] if server else "local"
    print(f"\n{info(f'Uptime — {label}')}\n")
    output = _run_cmd("uptime -p 2>/dev/null || uptime", server)
    print(f"  {Colors.GREEN}{output}{Colors.RESET}")


def show_disk():
    """Muestra el uso de disco."""
    server = _pick_target()
    label = server["name"] if server else "local"
    print(f"\n{info(f'Uso de disco — {label}')}\n")
    output = _run_cmd("df -h --output=source,size,used,avail,pcent,target | head -20", server)
    _print_block(output)


def show_memory():
    """Muestra el uso de memoria RAM."""
    server = _pick_target()
    label = server["name"] if server else "local"
    print(f"\n{info(f'Memoria — {label}')}\n")
    output = _run_cmd("free -h", server)
    _print_block(output)


def show_services():
    """Muestra los servicios activos."""
    server = _pick_target()
    label = server["name"] if server else "local"
    print(f"\n{info(f'Servicios activos — {label}')}\n")
    cmd = (
        "systemctl list-units --type=service --state=running "
        "--no-pager --no-legend | head -30"
    )
    output = _run_cmd(cmd, server)
    _print_block(output)


def show_all():
    """Muestra un resumen completo del servidor."""
    server = _pick_target()
    label = server["name"] if server else "local"

    sections = {
        "Uptime": "uptime -p 2>/dev/null || uptime",
        "Memoria": "free -h",
        "Disco": "df -h --output=source,size,used,avail,pcent,target | grep -v tmpfs | head -10",
        "Servicios activos": (
            "systemctl list-units --type=service --state=running "
            "--no-pager --no-legend | head -15"
        ),
    }

    print(f"\n{Colors.BOLD}Resumen de {label}{Colors.RESET}\n")
    print(f"  {Colors.GRAY}{'─' * 60}{Colors.RESET}")

    for title, cmd in sections.items():
        print(f"\n  {Colors.CYAN}{Colors.BOLD}{title}:{Colors.RESET}")
        output = _run_cmd(cmd, server)
        _print_block(output, indent=4)


def _print_block(text: str, indent: int = 2):
    prefix = " " * indent
    for line in text.splitlines():
        print(f"{prefix}{Colors.WHITE}{line}{Colors.RESET}")
