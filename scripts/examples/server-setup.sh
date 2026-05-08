#!/usr/bin/env bash
# scripts/examples/server-setup.sh
# Configuración inicial de un servidor Ubuntu/Debian.
# Uso: bash server-setup.sh

set -euo pipefail

echo "▶ Actualizando paquetes..."
sudo apt update && sudo apt upgrade -y

echo "▶ Instalando Node.js (LTS)..."
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

echo "▶ Instalando PM2..."
sudo npm install -g pm2
pm2 startup

echo "▶ Instalando Docker..."
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"

echo "✓ Servidor configurado. Reinicia la sesión SSH para aplicar los cambios."
