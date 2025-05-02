import tkinter as tk
from tkinter import ttk, messagebox
import threading
from core.renaming import *

def open_renaming_progress_interface(root, files_info):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("File Renamer - Renaming Files")
    root.geometry("400x200")
    root.resizable(False, False)

    root.protocol("WM_DELETE_WINDOW", lambda: messagebox.showwarning("Renaming in progress", "Please wait until the process is finished."))

    label_title = tk.Label(root, text="Renaming in progress...", font=("Arial", 14))
    label_title.pack(pady=20)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, maximum=100, variable=progress_var, length=300)
    progress_bar.pack(pady=10)

    label_status = tk.Label(root, text="0 / {}".format(len(files_info)), font=("Arial", 12))
    label_status.pack(pady=10)

    def update_progress(current, total):
        percent = (current / total) * 100
        progress_var.set(percent)
        label_status.config(text=f"{current} / {total}")
        root.update_idletasks()

    def finish_callback(success_count):
        # Réactiver la fermeture
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        messagebox.showinfo("Renaming Complete", f"{success_count} files renamed successfully.")
        root.destroy()

    def threaded_rename():
        rename_files(files_info, progress_callback=update_progress, final_callback=finish_callback)

    threading.Thread(target=threaded_rename, daemon=True).start()