import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import time
import yt_dlp

window = tk.Tk()
window.title("YouTube Downloader")
window.rowconfigure(2, weight=1)
window.columnconfigure([0, 1, 2], weight=1)

url_var = tk.StringVar()
destination_var = tk.StringVar()
progress_var = tk.DoubleVar()
speed_var = tk.StringVar()
remaining_var = tk.StringVar()
current_download_var = tk.StringVar()
completed_videos = []
stop_flag = False
start_time = None

folder_icon = Image.open('carpeta.png')
folder_icon = folder_icon.resize((15, 15), Image.Resampling.LANCZOS)
folder_icon = ImageTk.PhotoImage(folder_icon)

def choose_directory():
    directory = filedialog.askdirectory(title="Seleccionar destino")
    if directory:
        destination_var.set(directory)

def update_completed_list():
    completed_list.delete(0, tk.END)
    for video in completed_videos:
        completed_list.insert(tk.END, video)

def progress_hook(status_data):
    global stop_flag, start_time
    if stop_flag:
        return
    if status_data['status'] == 'downloading':
        now = time.time()
        if start_time is None:
            start_time = now
        downloaded = status_data.get('downloaded_bytes', 0)
        total = status_data.get('total_bytes', 0) or status_data.get('total_bytes_estimate', 0)
        speed = status_data.get('speed', 0)
        eta = status_data.get('eta', None)
        filename = status_data.get('filename', '...')
        if total > 0:
            progress_percent = downloaded / total * 100
        else:
            progress_percent = 0
        progress_var.set(progress_percent)
        if speed:
            speed_var.set(f"{speed / 1024**2:.2f} MB/s")
        else:
            speed_var.set("")
        if eta is not None:
            if eta >= 60:
                remaining_var.set(f"{eta / 60:.2f} minutos restantes")
            else:
                remaining_var.set(f"{eta:.0f} segundos restantes")
        else:
            remaining_var.set("Calculando...")
        current_download_var.set(f"Descargando: {filename}")
        window.update_idletasks()
    elif status_data['status'] == 'finished':
        filename = status_data.get('info_dict', {}).get('title', 'Video sin título')
        completed_videos.append(filename)
        update_completed_list()
        progress_var.set(0)
        speed_var.set("")
        remaining_var.set("")
        current_download_var.set(f"Descarga finalizada: {filename}")

def download_video():
    global stop_flag, start_time
    stop_flag = False
    start_time = None
    link = url_entry.get().strip()
    directory = destination_var.get() if destination_var.get() else filedialog.askdirectory(title="Seleccionar destino")
    if not link or not directory:
        messagebox.showerror("Error", "Por favor, ingresa un enlace válido de Youtube y selecciona el destino de la descarga.")
        return
    ydl_opts = {
        'outtmpl': f'{directory}/%(playlist_index)s. %(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'progress_hooks': [progress_hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        messagebox.showinfo("Completado", f"Descarga completa! Videos guardados en: {directory}")
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

def start_download_thread():
    global download_thread
    download_thread = threading.Thread(target=download_video)
    download_thread.start()

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
