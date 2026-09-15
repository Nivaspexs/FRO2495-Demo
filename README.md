Autor: Cristobal Suarez 

Demo para FRO2495. Prueba de latencia con WebRTC en red local (ej. cámara Ricoh Theta X).

## Guía Rápida de Inicio

1. **Servidor MediaMTX:**
   * Entra a la carpeta `docker-mediamtx` y levanta el servidor ejecutando: `docker compose up -d`.

2. **Configurar IP:**
   * En `emisor.html` y `receptor.html`, actualiza la variable `MEDIAMTX_URL` con la IP real de tu servidor Docker.

3. **Ejecutar la Demo:**
   * **Emisor:** Levanta un servidor local en esta carpeta (ej. `python3 -m http.server 8000`). Entra a `http://localhost:8000/emisor.html` desde la máquina que tiene la cámara (requiere localhost para permitir acceso a la cámara).
   * **Receptor:** En la segunda máquina, abre `receptor.html` directamente en tu navegador.
   * **Test de latencia:** Ejecuta `python3 reloj.py` para visualizar el cronómetro de milisegundos.
