"""
Carga y acceso a la configuración del proyecto (servers.json, etc.).
"""

import json
import os
from pathlib import Path
from app.colors import Colors

# Directorio raíz del proyecto (un nivel arriba de app/)
ROOT_DIR = Path(__file__).parent.parent
CONFIG_DIR = ROOT_DIR / "config"
SERVERS_FILE = CONFIG_DIR / "servers.json"


def load_servers() -> list[dict]:
    """Carga la lista de servidores desde config/servers.json."""
    if not SERVERS_FILE.exists():
        print(f"{Colors.WARNING}No se encontró {SERVERS_FILE}.{Colors.RESET}")
        print(f"{Colors.GRAY}Crea el archivo con la estructura de ejemplo del README.{Colors.RESET}")
        return []

    try:
        with open(SERVERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("servers", [])
    except json.JSONDecodeError as e:
        print(f"{Colors.ERROR}Error al leer servers.json: {e}{Colors.RESET}")
        return []


def get_server(name: str) -> dict | None:
    """Devuelve un servidor por su nombre o alias."""
    servers = load_servers()
    for s in servers:
        if s.get("name") == name or s.get("alias") == name:
            return s
    return None


def pick_server() -> dict | None:
    """Muestra la lista de servidores y pide al usuario que elija uno."""
    servers = load_servers()
    if not servers:
        return None

    print(f"\n{Colors.BOLD}Servidores disponibles:{Colors.RESET}")
    for i, s in enumerate(servers, 1):
        alias = f"  ({s['alias']})" if s.get("alias") else ""
        print(f"  {Colors.CYAN}[{i}]{Colors.RESET} {s['name']}{alias}  —  {s['host']}")

    try:
        idx = int(input(f"\n{Colors.CYAN}Selecciona servidor [número]: {Colors.RESET}").strip())
        if 1 <= idx <= len(servers):
            return servers[idx - 1]
    except (ValueError, IndexError):
        pass

    print(f"{Colors.ERROR}Selección inválida.{Colors.RESET}")
    return None
