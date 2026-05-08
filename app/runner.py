"""
Ejecución de comandos locales con manejo de errores y salida formateada.
"""

import subprocess
import shlex
from app.colors import Colors


def run(cmd: str, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """
    Ejecuta un comando en el shell local.

    Args:
        cmd: Comando como string.
        capture: Si True, captura stdout/stderr en lugar de imprimirlos.
        check: Si True, lanza excepción en caso de error.

    Returns:
        CompletedProcess con returncode, stdout, stderr.
    """
    args = shlex.split(cmd)
    try:
        result = subprocess.run(
            args,
            capture_output=capture,
            text=True,
            check=check,
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"{Colors.ERROR}Error ejecutando: {cmd}{Colors.RESET}")
        if e.stderr:
            print(f"{Colors.GRAY}{e.stderr.strip()}{Colors.RESET}")
        raise
    except FileNotFoundError:
        print(f"{Colors.ERROR}Comando no encontrado: {args[0]}{Colors.RESET}")
        raise


def run_output(cmd: str) -> str:
    """Ejecuta un comando y devuelve su stdout como string."""
    result = run(cmd, capture=True, check=False)
    return result.stdout.strip()


def run_interactive(cmd: str):
    """Ejecuta un comando con stdin/stdout/stderr heredados (interactivo)."""
    args = shlex.split(cmd)
    subprocess.run(args, check=False)
