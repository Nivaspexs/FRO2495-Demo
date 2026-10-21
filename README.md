Autores: 
Cristobal Suarez 
Nicolás Vásquez 

Demo para FRO2495. Prueba de latencia con WebRTC en red local (ej. cámara Ricoh Theta X).

# Local

## Guía Rápida de Inicio

1. **Servidor MediaMTX:**
   * Entra a la carpeta `docker-mediamtx` y levanta el servidor ejecutando: `docker compose up -d`.

2. **Configurar IP:**
   * En `emisor.html` y `receptor.html`, actualiza la variable `MEDIAMTX_URL` con la IP real de tu servidor Docker.

3. **Ejecutar la Demo:**
   * **Emisor:** Levanta un servidor local en esta carpeta (ej. `python3 -m http.server 8000`). Entra a `http://localhost:8000/emisor.html` desde la máquina que tiene la cámara (requiere localhost para permitir acceso a la cámara).
   * **Receptor:** En la segunda máquina, abre `receptor.html` directamente en tu navegador.
   * **Test de latencia:** Ejecuta `python3 reloj.py` para visualizar el cronómetro de milisegundos.


# Servidor

## Guía Rápida

1. **Primero debes abrir los siguientes puertos**
  - udp:8189 EXTERNO Salida stream webrtc
  - tcp:8554 EXTERNO Entrada stream rtsp
  - tcp:8889 INTERNO Gestión del WHEP

2. Instalar el docker compose y git
  - Instalar con el siguiente comando:
```bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

#Instalar docker desde repo
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

#Instalar git
sudo apt install git
```

