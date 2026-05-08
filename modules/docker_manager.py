"""
Módulo Docker: gestión de contenedores y Docker Compose.
"""

from app.colors import Colors, success, error, warning, info
from app.runner import run, run_output
from app.utils import require_input, confirm, command_exists


def _check_docker():
    if not command_exists("docker"):
        print(error("Docker no está instalado o no está en el PATH."))
        return False
    return True


def list_containers():
    """Lista todos los contenedores (activos e inactivos)."""
    if not _check_docker():
        return
    print(f"\n{Colors.BOLD}Contenedores Docker:{Colors.RESET}\n")
    try:
        run("docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'")
    except Exception:
        print(error("Error al listar contenedores."))


def start_container():
    """Inicia un contenedor detenido."""
    if not _check_docker():
        return
    name = require_input("Nombre del contenedor")
    try:
        run(f"docker start {name}")
        print(success(f"Contenedor '{name}' iniciado."))
    except Exception:
        print(error(f"No se pudo iniciar '{name}'."))


def stop_container():
    """Detiene un contenedor en ejecución."""
    if not _check_docker():
        return
    name = require_input("Nombre del contenedor")
    if not confirm(f"¿Detener el contenedor '{name}'?"):
        return
    try:
        run(f"docker stop {name}")
        print(success(f"Contenedor '{name}' detenido."))
    except Exception:
        print(error(f"No se pudo detener '{name}'."))


def restart_container():
    """Reinicia un contenedor."""
    if not _check_docker():
        return
    name = require_input("Nombre del contenedor")
    try:
        run(f"docker restart {name}")
        print(success(f"Contenedor '{name}' reiniciado."))
    except Exception:
        print(error(f"No se pudo reiniciar '{name}'."))


def show_logs():
    """Muestra los últimos logs de un contenedor."""
    if not _check_docker():
        return
    name = require_input("Nombre del contenedor")
    lines = input(f"{Colors.CYAN}Número de líneas [50]: {Colors.RESET}").strip() or "50"
    print(f"\n{info(f'Últimas {lines} líneas de logs de {name}:')}\n")
    try:
        run(f"docker logs --tail {lines} {name}")
    except Exception:
        print(error(f"No se pudieron obtener logs de '{name}'."))


def compose_up():
    """Ejecuta docker compose up en un directorio."""
    if not _check_docker():
        return
    compose_dir = input(
        f"{Colors.CYAN}Directorio con docker-compose.yml [.]: {Colors.RESET}"
    ).strip() or "."
    detach = input(f"{Colors.CYAN}¿Modo detach -d? [S/n]: {Colors.RESET}").strip().lower()
    flag = "" if detach == "n" else "-d"
    print(f"\n{info('Levantando servicios...')}\n")
    try:
        run(f"docker compose -f {compose_dir}/docker-compose.yml up {flag} --build")
        print(success("Servicios levantados."))
    except Exception:
        print(error("Error al levantar los servicios."))


def compose_down():
    """Detiene y elimina los contenedores de un docker-compose."""
    if not _check_docker():
        return
    compose_dir = input(
        f"{Colors.CYAN}Directorio con docker-compose.yml [.]: {Colors.RESET}"
    ).strip() or "."
    if not confirm("¿Detener y eliminar los contenedores?"):
        return
    try:
        run(f"docker compose -f {compose_dir}/docker-compose.yml down")
        print(success("Servicios detenidos y eliminados."))
    except Exception:
        print(error("Error al detener los servicios."))
