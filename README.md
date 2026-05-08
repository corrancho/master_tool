# Master Tool

CLI modular en Python para administrar VPS y automatizar tareas de despliegue.

---

## Características

- Menú interactivo con colores ANSI
- Gestión de claves SSH y conexión con GitHub
- Conexión SSH a servidores remotos
- Despliegue de aplicaciones Next.js (local y remoto)
- Gestión de contenedores Docker
- Estado del servidor: uptime, disco, memoria, servicios
- Configuración de servidores mediante JSON
- Estructura modular y fácil de ampliar

---

## Estructura del proyecto

```
master-tool/
├── main.py                  # Punto de entrada
├── app/
│   ├── colors.py            # Colores ANSI y helpers de salida
│   ├── menu.py              # Menú principal e interactivo
│   ├── runner.py            # Ejecución de comandos locales
│   ├── config.py            # Carga de configuración (servers.json)
│   └── utils.py             # Utilidades compartidas
├── modules/
│   ├── github.py            # Claves SSH, clonar, pull
│   ├── deploy.py            # Despliegue Next.js y scripts custom
│   ├── ssh_manager.py       # Conexión y comandos remotos SSH
│   ├── docker_manager.py    # Contenedores y Docker Compose
│   └── server_status.py     # Uptime, disco, RAM, servicios
├── config/
│   └── servers.json         # Lista de servidores VPS
├── scripts/
│   └── examples/
│       ├── deploy-nextjs.sh
│       └── server-setup.sh
├── requirements.txt
└── README.md
```

---

## Instalación

### Requisitos

- Python 3.11+
- Git
- `ssh` disponible en el PATH
- Docker (opcional, para el módulo Docker)
- PM2 (opcional, para reinicio automático de procesos Node)

### Pasos

```bash
# 1. Clona o copia el proyecto
cd ~/master_tool

# 2. (Opcional) Crea un entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instala dependencias opcionales si las necesitas
pip install -r requirements.txt

# 4. Lanza la herramienta
python3 main.py
```

### Acceso directo desde cualquier directorio (opcional)

```bash
chmod +x main.py
sudo ln -s "$(pwd)/main.py" /usr/local/bin/master-tool
# A partir de aquí puedes ejecutar: master-tool
```

---

## Configuración de servidores

Edita `config/servers.json` con tus VPS:

```json
{
  "servers": [
    {
      "name": "vps-produccion",
      "alias": "prod",
      "host": "123.45.67.89",
      "user": "ubuntu",
      "port": 22,
      "key": "~/.ssh/github_ed25519",
      "description": "Servidor de producción"
    }
  ]
}
```

| Campo         | Obligatorio | Descripción                              |
|---------------|-------------|------------------------------------------|
| `name`        | Sí          | Identificador único del servidor         |
| `host`        | Sí          | IP o dominio                             |
| `user`        | No          | Usuario SSH (por defecto: `root`)        |
| `port`        | No          | Puerto SSH (por defecto: `22`)           |
| `key`         | No          | Ruta a la clave privada SSH              |
| `alias`       | No          | Nombre corto alternativo                 |
| `description` | No          | Descripción libre                        |

---

## Uso paso a paso

### 1. Configurar GitHub con clave SSH nueva

```
Menú → [1] GitHub → [1] Crear clave SSH para GitHub
```

Introduce tu email de GitHub. La clave se guardará en `~/.ssh/github_ed25519`.

```
→ [2] Mostrar clave pública
```

Copia la clave y pégala en: **GitHub → Settings → SSH and GPG keys → New SSH key**

```
→ [3] Configurar ~/.ssh/config
→ [4] Probar conexión SSH con GitHub
```

Deberías ver: `Hi usuario! You've successfully authenticated...`

---

### 2. Clonar y actualizar repositorios

```
Menú → [1] GitHub → [5] Clonar repositorio
```

Usa la URL SSH: `git@github.com:tu-usuario/tu-repo.git`

```
→ [6] Actualizar repositorio (git pull)
```

---

### 3. Conectar a una VPS

Asegúrate de tener `config/servers.json` configurado, luego:

```
Menú → [2] SSH / VPS → [1] Listar servidores
→ [2] Conectar a un servidor
```

Selecciona el servidor de la lista para abrir una sesión SSH interactiva.

---

### 4. Desplegar una app Next.js

```
Menú → [3] Despliegue → [1] Desplegar app Next.js
```

Elige modo local (en la máquina actual) o remoto (en una VPS).  
El proceso realiza: `git pull → npm install → npm run build → pm2 restart`

---

### 5. Gestionar Docker

```
Menú → [4] Docker → [1] Listar contenedores
```

Opciones disponibles: iniciar, detener, reiniciar, ver logs, `compose up/down`.

---

### 6. Ver estado del servidor

```
Menú → [5] Estado del servidor → [5] Resumen completo
```

Elige local o remoto para obtener uptime, RAM, disco y servicios activos.

---

## Añadir un nuevo módulo

1. Crea `modules/mi_modulo.py` con tus funciones.
2. En `app/menu.py`, añade un nuevo submenú siguiendo el patrón de `_menu_docker()`.
3. Añade la opción al menú principal en `_show_main_options()`.

Ejemplo mínimo de módulo:

```python
# modules/mi_modulo.py
from app.colors import success, error

def mi_funcion():
    print("Haciendo algo...")
    print(success("Hecho."))
```

---

## Seguridad

- No se almacenan contraseñas en ningún archivo.
- Toda la autenticación SSH usa claves privadas.
- Las claves privadas nunca se muestran ni se loguean.
- Se solicita confirmación antes de acciones destructivas.
- `servers.json` solo contiene rutas a claves, no las claves en sí.

---

## Licencia

MIT — libre para uso personal y comercial.