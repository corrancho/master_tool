#!/usr/bin/env python3
"""
Master Tool - CLI para administrar VPS y automatizar despliegues.
Punto de entrada principal.
"""

import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.colors import Colors
from app.menu import main_menu


def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Saliendo de Master Tool...{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
