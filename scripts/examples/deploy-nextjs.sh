#!/usr/bin/env bash
# scripts/examples/deploy-nextjs.sh
# Ejemplo de script de despliegue Next.js para ejecutar en el servidor remoto.
# Uso: bash deploy-nextjs.sh /ruta/al/proyecto nombre-pm2

set -euo pipefail

APP_DIR="${1:-/var/www/mi-app}"
PM2_NAME="${2:-mi-app}"
BRANCH="${3:-main}"

echo "▶ Actualizando código en $APP_DIR..."
git -C "$APP_DIR" pull origin "$BRANCH"

echo "▶ Instalando dependencias..."
npm --prefix "$APP_DIR" install --production=false

echo "▶ Compilando..."
npm --prefix "$APP_DIR" run build

echo "▶ Reiniciando proceso PM2: $PM2_NAME"
pm2 restart "$PM2_NAME" || pm2 start npm --name "$PM2_NAME" -- --prefix "$APP_DIR" start

echo "✓ Despliegue completado."
