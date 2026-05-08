"""
Módulo GitHub: gestión de claves SSH y repositorios.
"""

import os
import subprocess
from pathlib import Path
from app.colors import Colors, success, error, warning, info
from app.runner import run, run_output, run_interactive
from app.utils import require_input, confirm, command_exists


SSH_DIR = Path.home() / ".ssh"


def create_ssh_key():
    """Genera un par de claves SSH Ed25519 para GitHub."""
    print(f"\n{Colors.BOLD}Crear clave SSH para GitHub{Colors.RESET}\n")

    email = require_input("Email de GitHub")
    key_name = input(f"{Colors.CYAN}Nombre del archivo de clave [github_ed25519]: {Colors.RESET}").strip()
    if not key_name:
        key_name = "github_ed25519"

    key_path = SSH_DIR / key_name

    if key_path.exists():
        print(warning(f"Ya existe una clave en {key_path}"))
        if not confirm("¿Sobreescribir?"):
            return

    SSH_DIR.mkdir(mode=0o700, exist_ok=True)

    try:
        run(f'ssh-keygen -t ed25519 -C "{email}" -f {key_path} -N ""')
        print(success(f"Clave generada en {key_path}"))
        print(info("Añade la clave pública a GitHub → Settings → SSH keys"))
        _print_public_key(key_path.with_suffix(".pub"))
    except Exception:
        print(error("No se pudo generar la clave SSH."))


def show_public_key():
    """Muestra la clave pública de una clave SSH existente."""
    print(f"\n{Colors.BOLD}Claves SSH disponibles:{Colors.RESET}\n")

    pub_keys = list(SSH_DIR.glob("*.pub"))
    if not pub_keys:
        print(warning("No se encontraron claves públicas en ~/.ssh/"))
        return

    for i, k in enumerate(pub_keys, 1):
        print(f"  {Colors.CYAN}[{i}]{Colors.RESET} {k.name}")

    try:
        idx = int(require_input("Elige una clave [número]")) - 1
        _print_public_key(pub_keys[idx])
    except (ValueError, IndexError):
        print(error("Selección inválida."))


def _print_public_key(pub_path: Path):
    if pub_path.exists():
        content = pub_path.read_text().strip()
        print(f"\n{Colors.GREEN}{content}{Colors.RESET}\n")
        print(info("Copia la línea anterior y pégala en GitHub → SSH keys"))
    else:
        print(error(f"No se encontró: {pub_path}"))


def configure_ssh_config():
    """Añade una entrada para GitHub en ~/.ssh/config."""
    print(f"\n{Colors.BOLD}Configurar ~/.ssh/config para GitHub{Colors.RESET}\n")

    key_name = input(f"{Colors.CYAN}Nombre del archivo de clave [github_ed25519]: {Colors.RESET}").strip()
    if not key_name:
        key_name = "github_ed25519"

    key_path = SSH_DIR / key_name
    config_path = SSH_DIR / "config"

    entry = f"""
Host github.com
    HostName github.com
    User git
    IdentityFile {key_path}
    IdentitiesOnly yes
"""

    if config_path.exists():
        existing = config_path.read_text()
        if "Host github.com" in existing:
            print(warning("Ya existe una entrada para github.com en ~/.ssh/config"))
            if not confirm("¿Reemplazar bloque existente?"):
                return
            # Eliminar bloque anterior
            lines = existing.splitlines(keepends=True)
            new_lines = []
            skip = False
            for line in lines:
                if line.strip() == "Host github.com":
                    skip = True
                elif skip and line.startswith("Host "):
                    skip = False
                if not skip:
                    new_lines.append(line)
            existing = "".join(new_lines)
            config_path.write_text(existing + entry)
        else:
            with open(config_path, "a") as f:
                f.write(entry)
    else:
        config_path.write_text(entry)
        config_path.chmod(0o600)

    print(success(f"Configuración guardada en {config_path}"))


def test_github_connection():
    """Prueba la conexión SSH con GitHub."""
    print(f"\n{Colors.BOLD}Probando conexión SSH con GitHub...{Colors.RESET}\n")
    result = subprocess.run(
        ["ssh", "-T", "git@github.com"],
        capture_output=True,
        text=True,
    )
    # GitHub devuelve código 1 aunque la autenticación sea correcta
    output = result.stdout + result.stderr
    if "successfully authenticated" in output:
        print(success("Conexión exitosa con GitHub."))
        print(f"{Colors.GRAY}{output.strip()}{Colors.RESET}")
    else:
        print(error("No se pudo autenticar con GitHub."))
        print(f"{Colors.GRAY}{output.strip()}{Colors.RESET}")


def clone_repo():
    """Clona un repositorio de GitHub."""
    print(f"\n{Colors.BOLD}Clonar repositorio{Colors.RESET}\n")

    if not command_exists("git"):
        print(error("Git no está instalado."))
        return

    repo = require_input("URL SSH del repositorio (git@github.com:usuario/repo.git)")
    dest = input(f"{Colors.CYAN}Directorio destino [directorio actual]: {Colors.RESET}").strip() or "."

    try:
        run(f"git clone {repo} {dest}")
        print(success("Repositorio clonado correctamente."))
    except Exception:
        print(error("Error al clonar el repositorio."))


def pull_repo():
    """Actualiza un repositorio local con git pull."""
    print(f"\n{Colors.BOLD}Actualizar repositorio (git pull){Colors.RESET}\n")

    if not command_exists("git"):
        print(error("Git no está instalado."))
        return

    repo_dir = input(f"{Colors.CYAN}Ruta del repositorio [directorio actual]: {Colors.RESET}").strip() or "."
    branch = input(f"{Colors.CYAN}Rama [main]: {Colors.RESET}").strip() or "main"

    try:
        run(f"git -C {repo_dir} pull origin {branch}")
        print(success("Repositorio actualizado."))
    except Exception:
        print(error("Error al actualizar el repositorio."))
