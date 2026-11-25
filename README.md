Autores: 
Cristobal Suarez 
Nicolás Vásquez 

Demo para FRO2495. Prueba de latencia con WebRTC usando una cámara 360° Ricoh Theta X y una cámara intraoral MouthWatch.

# Arquitectura

- `index.html`: receptor web único. Abre **dos conexiones WHEP en paralelo**, una al stream `theta` (vista principal) y otra a `mouthwatch` (transmisión secundaria).
- `docker-mediamtx/`: servidor MediaMTX. Publica y sirve ambos streams de forma simultánea.
- `nginx`: sirve la página por HTTPS y hace de proxy WHEP hacia MediaMTX (`127.0.0.1:8889`).
- `reloj.py`: reloj con milisegundos para medir latencia vidrio a vidrio.

En la interfaz, el botón **MouthWatch** de la barra de controles (modo 2D) o del HUD flotante (modo VR) activa un cuadro con la transmisión `mouthwatch`. Los botones **Solo MouthWatch** y **Paralelo** permiten alternar la vista exclusiva entre ambas cámaras o mostrar las dos transmisiones lado a lado en un layout plano. Las dos transmisiones se mantienen conectadas aunque no estén visibles. Si Theta deja de transmitir y MouthWatch está en vivo, la vista principal pasa automáticamente a MouthWatch para no quedar sin imagen.

# Local

## Guía rápida

1. **Servidor MediaMTX:**
   * Entra a la carpeta `docker-mediamtx` y levanta el servidor: `docker compose up -d`.

2. **Publicar ambas cámaras en MediaMTX:**
   * Stream principal (Ricoh Theta X): `rtsp://<IP_SERVIDOR>:8554/theta`
   * Stream secundario (MouthWatch): `rtsp://<IP_SERVIDOR>:8554/mouthwatch`

   Ejemplo si MouthWatch se captura con una cámara USB conectada al servidor (ajusta el dispositivo):

   ```bash
   ffmpeg -f v4l2 -i /dev/video2 \
     -c:v libx264 -preset veryfast -tune zerolatency -pix_fmt yuv420p \
     -f rtsp rtsp://127.0.0.1:8554/mouthwatch
   ```

3. **Servir la página con nginx/HTTPS:**
   * `index.html` debe abrirse por HTTPS. WebXR (modo inmersivo) y Wake Lock no funcionan por HTTP.
   * nginx debe redirigir `/<stream>/whep` a MediaMTX. El despliegue usa el mismo origen para `theta` y `mouthwatch`.

4. **Ejecutar la demo:**
   * Abre `https://<IP_SERVIDOR>/` en el navegador del Meta Quest 2 o en un computador.
   * La vista principal carga `theta`. Usa **Solo MouthWatch** para ver únicamente la cámara intraoral (y el mismo botón para volver a Theta), **Paralelo** para mostrar ambas en pantalla dividida, o **MouthWatch** para el cuadro flotante.
   * **Test de latencia:** ejecuta `python3 reloj.py` en la escena remota para visualizar el cronómetro de milisegundos.

## Modos de visualización

- **Solo MouthWatch / Solo Theta:** alterna la vista exclusiva entre ambos streams. Es un botón de ida y vuelta: si estás viendo MouthWatch, el mismo control dice **Solo Theta**.
- **Paralelo:** muestra Theta y MouthWatch lado a lado en un layout plano, tanto en la vista 2D como en dos paneles dentro de VR. Vuelve a pulsar **Cerrar paralelo** para regresar a la vista exclusiva seleccionada.
- **MouthWatch:** mantiene el modo de cuadro flotante (PiP en 2D y panel junto al HUD en VR). Solo aplica a la vista exclusiva de Theta; si se pulsa desde otro modo, vuelve a Theta y activa el cuadro.
- **Fallback automático:** si Theta queda sin enlace o sin cuadros y MouthWatch está en vivo, la vista exclusiva cambia automáticamente a **Solo MouthWatch** (de inmediato ante un fallo de enlace, o tras 5 s sin cuadros). Al recuperarse Theta, vuelve a la vista principal, salvo que se haya elegido otra vista manualmente. El botón **Solo Theta** permite mantener la vista de Theta aunque no transmita, suspendiendo el fallback durante esa interrupción.
- MouthWatch se reproduce sin audio; el audio disponible corresponde al stream principal `theta`.

## Streams paralelos

MediaMTX ya está configurado con ambos paths en `docker-mediamtx/mediamtx.yml`:

```yaml
paths:
  theta:
    publishUser: ""
    readUser: ""
  mouthwatch:
    publishUser: ""
    readUser: ""
```

Cada navegador abre dos sesiones WHEP independientes (`/theta/whep` y `/mouthwatch/whep`). Los puertos son compartidos: no se necesita un puerto adicional para el segundo stream.

### Proxy nginx de referencia

El `location` debe cubrir también las rutas con identificador de sesión que MediaMTX usa para cerrar la sesión WHEP con `DELETE` (`/<stream>/whep/<id>`). El siguiente patrón sirve para ambos streams:

```nginx
server {
    listen 443 ssl;
    server_name teleodontologia.example.cl;

    root /var/www/FRO2495-Demo;
    index index.html;

    location ~ ^/(theta|mouthwatch)/whep(/.*)?$ {
        proxy_pass http://127.0.0.1:8889;
        proxy_http_version 1.1;
        proxy_request_buffering off;
        proxy_buffering off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Parámetros de URL útiles

- `?stream=theta`: cambia el stream principal.
- `?auxStream=mouthwatch` o `?aux=mouthwatch`: cambia el stream secundario.
- `?view=sphere|flat`: vista inicial en VR.
- `?rotation=-90`: orientación de la esfera 360°.
- `?preview360=1`: abre la vista 360° en el navegador 2D.

# Servidor

## Guía rápida

1. **Primero debes abrir los siguientes puertos**
   - udp:8189 EXTERNO Salida de media WebRTC para ambos streams
   - tcp:8554 EXTERNO Entrada de publicaciones RTSP (`theta` y `mouthwatch`)
   - tcp:8889 INTERNO Gestión del WHEP (solo nginx debe acceder)
   - tcp:443 EXTERNO HTTPS de la página y WHEP

2. Instalar Docker Compose y git
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

# Instalar docker desde repo
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Instalar git
sudo apt install git
```

3. **Levantar MediaMTX**

```bash
cd docker-mediamtx
docker compose up -d
```

4. **Ajustar la IP pública**

   En `docker-mediamtx/mediamtx.yml`, reemplaza `webrtcAdditionalHosts` por la IP pública o la IP de la red local del servidor:

```yaml
webrtcAdditionalHosts: [<IP_SERVIDOR>]
```

   Si usas `network_mode: host`, no necesitas mapear puertos en `docker-compose.yml`.
