import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from pytube import YouTube, Playlist
import threading
import time

# Ventana principal
window = tk.Tk()
window.title("YouTube Downloader")

# Configuración de columnas y filas
window.rowconfigure(2, weight=1)
window.columnconfigure([0, 1, 2], weight=1)

# Variables
url_var = tk.StringVar()
destination_var = tk.StringVar() 
progress_var = tk.DoubleVar()
speed_var = tk.StringVar()
remaining_var = tk.StringVar()
current_download_var = tk.StringVar()
completed_videos = []
stop_flag = False
current_video_stream = None
start_time = None

# Cargar el icono de la carpeta
folder_icon = Image.open('carpeta.png')
folder_icon = folder_icon.resize((15, 15), Image.Resampling.LANCZOS) 
folder_icon = ImageTk.PhotoImage(folder_icon)

# Función para seleccionar el directorio
def choose_directory():
    directory = filedialog.askdirectory(title="Seleccionar destino")
    if directory: 
        destination_var.set(directory)

# Función para actualizar la lista de descargas completadas
def update_completed_list():
    completed_list.delete(0, tk.END)
    for video in completed_videos:
        completed_list.insert(tk.END, video)

# Función para mostrar el progreso de la descarga
def on_progress(stream, chunk, bytes_remaining, yt, download_count, total_videos):
    global start_time
    if stop_flag:
        return
    current_time = time.time()
    bytes_downloaded = stream.filesize - bytes_remaining
    download_speed = bytes_downloaded / (current_time - start_time)
    percentage_of_completion = (bytes_downloaded / stream.filesize) * 100
    progress_var.set(percentage_of_completion)
    speed_var.set(f"{download_speed / 1024**2:.2f} MB/s")
    remaining_var.set(f"{bytes_remaining / download_speed:.2f} minutos restantes" if bytes_remaining / download_speed >= 60 else f"{bytes_remaining / download_speed:.0f} segundos restantes")
    current_download_var.set(f"Descargando ({download_count}/{total_videos}): {yt.title}")
    window.update_idletasks()

# Función para gestionar la descarga de vídeos
def download_video():
    global stop_flag, current_video_stream, start_time
    stop_flag = False
    current_video_stream = None
    start_time = time.time()

    link = url_entry.get()
    directory = destination_var.get() if destination_var.get() else filedialog.askdirectory(title="Seleccionar destino")
    if not link or not directory:
        messagebox.showerror("Error", "Por favor, ingresa un enlace válido de Youtube y selecciona el destino de la descarga.")
        return

    try:
        download_count = 1
        if "playlist" in link:
            playlist = Playlist(link)
            total_videos = len(playlist.video_urls)
            for video in playlist.videos:
                if stop_flag:
                    break
                video.register_on_progress_callback(lambda stream, chunk, bytes_remaining, video=video, total_videos=total_videos: on_progress(stream, chunk, bytes_remaining, video, download_count, total_videos))
                stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                if stream:
                    filename = f"{download_count}. {video.title}.mp4"
                    current_video_stream = stream
                    current_video_stream.download(output_path=directory, filename=filename)
                    completed_videos.append(filename)
                    update_completed_list()
                    download_count += 1
        else:
            yt = YouTube(link)
            yt.register_on_progress_callback(lambda stream, chunk, bytes_remaining, yt=yt, total_videos=1: on_progress(stream, chunk, bytes_remaining, yt, 1, 1))
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if stream:
                filename = f"1. {yt.title}.mp4"
                current_video_stream = stream
                current_video_stream.download(output_path=directory, filename=filename)
                completed_videos.append(filename)
                update_completed_list()

        messagebox.showinfo("Completado", "Descarga completa! Videos guardados en " + directory)
    except Exception as e:
        if stop_flag:
            messagebox.showinfo("Cancelado", "Descarga cancelada por el usuario.")
        else:
            messagebox.showerror("Error", str(e))
    finally:
        progress_var.set(0)
        speed_var.set("")
        remaining_var.set("")
        current_download_var.set("")
        if current_video_stream:
            current_video_stream.close()

def start_download_thread():
    global download_thread
    download_thread = threading.Thread(target=download_video)
    download_thread.start()

# UI para la URL y el botón de carpeta
url_label = tk.Label(window, text="YouTube URL:")
url_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

url_entry = tk.Entry(window, textvariable=url_var, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

folder_button = tk.Button(window, image=folder_icon, command=choose_directory)
folder_button.grid(row=0, column=2, padx=10, pady=10, sticky='w')

download_button = tk.Button(window, text="Descargar", command=start_download_thread)
download_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate", variable=progress_var)
progress_bar.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

speed_label = tk.Label(window, textvariable=speed_var)
speed_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')

remaining_label = tk.Label(window, textvariable=remaining_var)
remaining_label.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

current_download_label = tk.Label(window, textvariable=current_download_var)
current_download_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

completed_label = tk.Label(window, text="Descargas completadas:")
completed_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')

scrollbar = tk.Scrollbar(window, orient="vertical")
completed_list = tk.Listbox(window, yscrollcommand=scrollbar.set)
scrollbar.config(command=completed_list.yview)
scrollbar.grid(row=5, column=2, sticky='ns')
completed_list.grid(row=5, column=1, padx=10, pady=10, sticky='ew')

window.mainloop()
