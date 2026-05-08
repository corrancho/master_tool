"""
Módulo Deploy: despliegue de aplicaciones (Next.js, scripts personalizados).
"""

import os
import subprocess
from pathlib import Path
from app.colors import Colors, success, error, warning, info
from app.runner import run, run_interactive
from app.config import pick_server
from app.utils import require_input, confirm, command_exists
from modules.ssh_manager import _build_ssh_cmd


def deploy_nextjs():
    """
    Despliega una aplicación Next.js.
    Comprueba si hay commits nuevos antes de buildear.
    git fetch → ¿hay cambios? → pull → npm install → npm run build → pm2 restart
    """
    print(f"\n{Colors.BOLD}Despliegue de aplicación Next.js{Colors.RESET}\n")

    mode = input(
        f"{Colors.CYAN}¿Despliegue local [L] o remoto [R]? [L]: {Colors.RESET}"
    ).strip().upper() or "L"

    if mode == "R":
        _deploy_nextjs_remote()
    else:
        _deploy_nextjs_local()


def _has_new_commits(app_path: Path, branch: str) -> bool:
    """Devuelve True si el remoto tiene commits que no están en local."""
    import subprocess as sp
    # Descarga info del remoto sin modificar el working tree
    sp.run(["git", "-C", str(app_path), "fetch", "origin"], capture_output=True)
    result = sp.run(
        ["git", "-C", str(app_path), "rev-list", "--count", f"HEAD..origin/{branch}"],
        capture_output=True, text=True,
    )
    try:
        return int(result.stdout.strip()) > 0
    except ValueError:
        return True  # si no se puede determinar, build por seguridad


def _deploy_nextjs_local():
    app_dir = require_input("Ruta del proyecto Next.js")
    branch = input(f"{Colors.CYAN}Rama [main]: {Colors.RESET}").strip() or "main"
    pm2_name = input(f"{Colors.CYAN}Nombre de proceso PM2 (dejar vacío para omitir): {Colors.RESET}").strip()

    app_path = Path(app_dir).expanduser()
    if not app_path.exists():
        print(error(f"No existe el directorio: {app_path}"))
        return

    # Comprobar si hay commits nuevos en remoto
    print(f"\n{info('Comprobando si hay cambios en el repositorio...')}")
    if not _has_new_commits(app_path, branch):
        print(success("Ya tienes la última versión. No hay nada que buildear."))
        return

    print(info("Hay commits nuevos. Iniciando despliegue..."))

    if not confirm(f"¿Desplegar {app_path}?"):
        return

    steps = [
        (f"git -C {app_path} pull origin {branch}", "Actualizando código"),
        (f"npm --prefix {app_path} install --production=false", "Instalando dependencias"),
        (f"npm --prefix {app_path} run build", "Compilando"),
    ]

    for cmd, label in steps:
        print(f"\n{info(label + '...')}")
        try:
            run(cmd)
            print(success(label))
        except Exception:
            print(error(f"Error en: {label}"))
            return

    if pm2_name:
        if command_exists("pm2"):
            try:
                run(f"pm2 restart {pm2_name}")
                print(success(f"PM2: proceso '{pm2_name}' reiniciado."))
            except Exception:
                print(warning("No se pudo reiniciar el proceso PM2."))
        else:
            print(warning("pm2 no está instalado. Reinicia manualmente."))

    print(f"\n{success('Despliegue completado.')}")


def _deploy_nextjs_remote():
    server = pick_server()
    if not server:
        return

    app_dir = require_input("Ruta del proyecto en el servidor remoto")
    branch = input(f"{Colors.CYAN}Rama [main]: {Colors.RESET}").strip() or "main"
    pm2_name = input(f"{Colors.CYAN}Nombre de proceso PM2 (vacío para omitir): {Colors.RESET}").strip()

    pm2_cmd = f" && pm2 restart {pm2_name}" if pm2_name else ""

    # El check de commits se ejecuta en el servidor remoto
    remote_script = (
        f"cd {app_dir}"
        f" && git fetch origin"
        f" && COMMITS=$(git rev-list --count HEAD..origin/{branch})"
        f" && if [ \"$COMMITS\" -eq 0 ]; then echo 'UP_TO_DATE'; exit 0; fi"
        f" && git pull origin {branch}"
        f" && npm install --production=false"
        f" && npm run build"
        f"{pm2_cmd}"
        f" && echo 'DEPLOY_OK'"
    )

    if not confirm(f"¿Ejecutar despliegue en {server['name']}?"):
        return

    cmd = _build_ssh_cmd(server, command=remote_script)
    print(f"\n{info('Comprobando cambios y ejecutando despliegue remoto...')}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    if "UP_TO_DATE" in output:
        print(success("Ya tienes la última versión en el servidor. No hay nada que buildear."))
    elif result.returncode == 0:
        print(success("Despliegue remoto completado."))
    else:
        print(error("El despliegue remoto falló."))
        if output.strip():
            print(f"{Colors.GRAY}{output.strip()}{Colors.RESET}")


def run_deploy_script():
    """Ejecuta un script de despliegue personalizado (local o remoto)."""
    print(f"\n{Colors.BOLD}Ejecutar script de despliegue{Colors.RESET}\n")

    scripts_dir = Path(__file__).parent.parent / "scripts"
    scripts = list(scripts_dir.rglob("*.sh")) + list(scripts_dir.rglob("*.py"))

    if scripts:
        print(f"{Colors.BOLD}Scripts disponibles:{Colors.RESET}")
        for i, s in enumerate(scripts, 1):
            rel = s.relative_to(scripts_dir.parent)
            print(f"  {Colors.CYAN}[{i}]{Colors.RESET} {rel}")
        print(f"  {Colors.CYAN}[0]{Colors.RESET} Introducir ruta manualmente")

        choice = input(f"\n{Colors.CYAN}Elige un script: {Colors.RESET}").strip()
        if choice == "0" or not choice.isdigit():
            script_path = Path(require_input("Ruta del script"))
        else:
            idx = int(choice) - 1
            script_path = scripts[idx] if 0 <= idx < len(scripts) else None
    else:
        print(warning("No hay scripts en la carpeta scripts/"))
        script_path = Path(require_input("Ruta del script"))

    if not script_path or not script_path.exists():
        print(error("Script no encontrado."))
        return

    if not confirm(f"¿Ejecutar {script_path}?"):
        return

    script_path.chmod(script_path.stat().st_mode | 0o111)

    if script_path.suffix == ".py":
        run_interactive(f"python3 {script_path}")
    else:
        run_interactive(str(script_path))
