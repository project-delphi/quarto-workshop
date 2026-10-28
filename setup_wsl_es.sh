#!/usr/bin/env bash
set -e

# Actualiza los índices de paquetes y los paquetes instalados.
sudo apt update && sudo apt upgrade -y

# Instala las herramientas básicas para el taller.
sudo apt install -y curl wget git python3 python3-pip python3-venv nodejs npm

# Descarga el paquete de Quarto para Linux de 64 bits.
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.10.19/quarto-1.10.19-linux-amd64.deb

# Instala Quarto y resuelve las dependencias pendientes.
sudo dpkg -i quarto-1.10.19-linux-amd64.deb
sudo apt-get install -f -y

# Elimina el instalador descargado después de instalarlo.
rm quarto-1.10.19-linux-amd64.deb

# Instala Claude Code para todos los usuarios del sistema.
sudo npm install -g @anthropic-ai/claude-code

# Descarga los materiales del taller.
git clone https://github.com/project-delphi/quarto-workshop.git

# Entra al repositorio e inicia Claude Code para preparar la sesión.
cd quarto-workshop && claude
