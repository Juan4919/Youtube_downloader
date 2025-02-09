# YouTube Downloader

Esta aplicación permite descargar videos o listas de reproducción de YouTube directamente a tu PC, usando una interfaz gráfica construida con Tkinter y la librería [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Características

- Descarga de videos individuales de YouTube.  
- Descarga de listas de reproducción completas.  
- Descarga en la mejor calidad disponible (combina mejor video + mejor audio).  
- Visualización en tiempo real del progreso de descarga.  
- Muestra la velocidad de descarga y el tiempo restante.  
- Lista las descargas completadas en la misma sesión.

## Requisitos Previos

- **Python** (3.x recomendado)  
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**  
- **[Pillow (PIL)](https://pillow.readthedocs.io/)**  
- **Tkinter** (generalmente incluido por defecto en Windows y macOS; en algunas distribuciones de Linux se instala con su gestor de paquetes)  
- **threading** (parte de la biblioteca estándar de Python)
- **ffmpeg** (recomendado para unir mejor video y audio en un solo archivo, aunque no obligatorio si usas formatos progresivos)


## Instalación

Clona este repositorio en tu máquina local usando:

git clone URL_DEL_REPOSITORIO

Instala las dependencias necesarias con:

pip install yt-dlp
pip install Pillow

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando en la terminal:

python youtube_downloader.py

Una vez iniciada, introduce la URL del video o lista de reproducción de YouTube que deseas descargar y selecciona el directorio donde se guardarán los archivos. Presiona el botón "Descargar" para comenzar el proceso.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes alguna mejora o corrección, por favor, siéntete libre de clonar el repositorio y abrir un pull request.


