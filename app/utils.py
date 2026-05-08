"""
Funciones de utilidad general compartidas entre módulos.
"""

import os
import sys
from app.colors import Colors


BANNER = f"""{Colors.CYAN}{Colors.BOLD}
  ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗     ████████╗ ██████╗  ██████╗ ██╗
  ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
  ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝       ██║   ██║   ██║██║   ██║██║
  ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗       ██║   ██║   ██║██║   ██║██║
  ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
{Colors.RESET}{Colors.GRAY}  Gestión de VPS y automatización de despliegues  •  v1.0.0{Colors.RESET}
"""


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def print_banner():
    print(BANNER)


def print_separator(char: str = "─", width: int = 72):
    print(f"  {Colors.GRAY}{char * width}{Colors.RESET}")


def confirm(prompt: str = "¿Estás seguro?") -> bool:
    """Pide confirmación al usuario antes de una acción peligrosa."""
    answer = input(f"\n{Colors.WARNING}{prompt} [s/N]: {Colors.RESET}").strip().lower()
    return answer in ("s", "si", "sí", "y", "yes")


def require_input(prompt: str, allow_empty: bool = False) -> str:
    """Solicita un valor obligatorio al usuario."""
    while True:
        value = input(f"{Colors.CYAN}{prompt}: {Colors.RESET}").strip()
        if value or allow_empty:
            return value
        print(f"{Colors.ERROR}Este campo es obligatorio.{Colors.RESET}")


def command_exists(cmd: str) -> bool:
    """Comprueba si un comando está disponible en el PATH."""
    import shutil
    return shutil.which(cmd) is not None
