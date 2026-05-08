"""
Menú interactivo principal de Master Tool.
"""

import os
from app.colors import Colors, header, info
from app.utils import clear_screen, print_banner, print_separator


def main_menu():
    """Bucle principal del menú."""
    while True:
        clear_screen()
        print_banner()
        _show_main_options()

        choice = input(f"\n{Colors.CYAN}Elige una opción: {Colors.RESET}").strip()

        if choice == "1":
            _menu_github()
        elif choice == "2":
            _menu_ssh()
        elif choice == "3":
            _menu_deploy()
        elif choice == "4":
            _menu_docker()
        elif choice == "5":
            _menu_server_status()
        elif choice == "0":
            print(f"\n{Colors.YELLOW}¡Hasta luego!{Colors.RESET}\n")
            break
        else:
            print(f"\n{Colors.ERROR}Opción no válida.{Colors.RESET}")
            input(f"{Colors.GRAY}Presiona Enter para continuar...{Colors.RESET}")


def _show_main_options():
    print(f"\n{Colors.BOLD}  MENÚ PRINCIPAL{Colors.RESET}")
    print_separator()
    options = [
        ("1", "GitHub", "Claves SSH, clonar y actualizar repos"),
        ("2", "SSH / VPS", "Conectar y ejecutar comandos remotos"),
        ("3", "Despliegue", "Desplegar aplicaciones (Next.js, etc.)"),
        ("4", "Docker", "Gestionar contenedores y servicios"),
        ("5", "Estado del servidor", "Uptime, disco, memoria, servicios"),
        ("0", "Salir", ""),
    ]
    for key, label, desc in options:
        desc_str = f"  {Colors.GRAY}{desc}{Colors.RESET}" if desc else ""
        print(f"  {Colors.CYAN}[{key}]{Colors.RESET} {Colors.WHITE}{label}{Colors.RESET}{desc_str}")


# ── Submenús ─────────────────────────────────────────────────────────────────

def _menu_github():
    from modules.github import (
        create_ssh_key, show_public_key,
        configure_ssh_config, test_github_connection,
        clone_repo, pull_repo,
    )

    options = {
        "1": ("Crear clave SSH para GitHub", create_ssh_key),
        "2": ("Mostrar clave pública", show_public_key),
        "3": ("Configurar ~/.ssh/config", configure_ssh_config),
        "4": ("Probar conexión SSH con GitHub", test_github_connection),
        "5": ("Clonar repositorio", clone_repo),
        "6": ("Actualizar repositorio (git pull)", pull_repo),
    }
    _run_submenu("GITHUB", options)


def _menu_ssh():
    from modules.ssh_manager import (
        list_servers, connect_to_server, run_remote_command,
    )

    options = {
        "1": ("Listar servidores configurados", list_servers),
        "2": ("Conectar a un servidor", connect_to_server),
        "3": ("Ejecutar comando remoto", run_remote_command),
    }
    _run_submenu("SSH / VPS", options)


def _menu_deploy():
    from modules.deploy import (
        deploy_nextjs, run_deploy_script,
    )

    options = {
        "1": ("Desplegar app Next.js", deploy_nextjs),
        "2": ("Ejecutar script de despliegue personalizado", run_deploy_script),
    }
    _run_submenu("DESPLIEGUE", options)


def _menu_docker():
    from modules.docker_manager import (
        list_containers, start_container, stop_container,
        restart_container, show_logs, compose_up, compose_down,
    )

    options = {
        "1": ("Listar contenedores", list_containers),
        "2": ("Iniciar contenedor", start_container),
        "3": ("Detener contenedor", stop_container),
        "4": ("Reiniciar contenedor", restart_container),
        "5": ("Ver logs de contenedor", show_logs),
        "6": ("Docker Compose up", compose_up),
        "7": ("Docker Compose down", compose_down),
    }
    _run_submenu("DOCKER", options)


def _menu_server_status():
    from modules.server_status import (
        show_uptime, show_disk, show_memory, show_services, show_all,
    )

    options = {
        "1": ("Uptime del sistema", show_uptime),
        "2": ("Uso de disco", show_disk),
        "3": ("Uso de memoria", show_memory),
        "4": ("Servicios activos", show_services),
        "5": ("Resumen completo", show_all),
    }
    _run_submenu("ESTADO DEL SERVIDOR", options)


def _run_submenu(title: str, options: dict):
    """Renderiza y ejecuta un submenú genérico."""
    while True:
        clear_screen()
        print_banner()
        print(f"\n{Colors.BOLD}  {title}{Colors.RESET}")
        print_separator()

        for key, (label, _) in options.items():
            print(f"  {Colors.CYAN}[{key}]{Colors.RESET} {Colors.WHITE}{label}{Colors.RESET}")
        print(f"  {Colors.CYAN}[0]{Colors.RESET} {Colors.WHITE}Volver{Colors.RESET}")

        choice = input(f"\n{Colors.CYAN}Elige una opción: {Colors.RESET}").strip()

        if choice == "0":
            break
        elif choice in options:
            print()
            options[choice][1]()
            input(f"\n{Colors.GRAY}Presiona Enter para continuar...{Colors.RESET}")
        else:
            print(f"\n{Colors.ERROR}Opción no válida.{Colors.RESET}")
            input(f"{Colors.GRAY}Presiona Enter para continuar...{Colors.RESET}")
