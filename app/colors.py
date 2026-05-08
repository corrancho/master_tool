"""
Definición de colores ANSI para la interfaz CLI.
"""


class Colors:
    # Colores de texto
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"

    # Estilos
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Reset
    RESET = "\033[0m"

    # Combos útiles
    SUCCESS = "\033[92m"   # Verde
    ERROR = "\033[91m"     # Rojo
    WARNING = "\033[93m"   # Amarillo
    INFO = "\033[94m"      # Azul
    HEADER = "\033[95m"    # Magenta


def success(msg: str) -> str:
    return f"{Colors.SUCCESS}✓ {msg}{Colors.RESET}"


def error(msg: str) -> str:
    return f"{Colors.ERROR}✗ {msg}{Colors.RESET}"


def warning(msg: str) -> str:
    return f"{Colors.WARNING}⚠ {msg}{Colors.RESET}"


def info(msg: str) -> str:
    return f"{Colors.INFO}ℹ {msg}{Colors.RESET}"


def header(msg: str) -> str:
    return f"{Colors.BOLD}{Colors.HEADER}{msg}{Colors.RESET}"
