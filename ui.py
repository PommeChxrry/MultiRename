import tkinter as tk
import os
from tkinter import filedialog
from core.file_selection import collect_files, files_preview

# Global list for storing selected raw paths
selected_paths = []

def select_files():
    # Select files and add into selected_paths
    files = filedialog.askopenfilenames(title="Select files")
    selected_paths.extend(files)

def select_folder():
    # Select folder and add files from folder into selected_paths
    folder = filedialog.askdirectory(title="Select folder")
    if folder:
        selected_paths.append(folder)

def validate_selection():
    # Validate the selection
    if not selected_paths:
        print("No path selected.")
        return
    
    # File collection and processing
    collected_files = collect_files(selected_paths)
    
    # Displays in console for debugging
    files_preview(collected_files)
    
    # Clear and update listbox
    file_listbox.delete(0, tk.END)
    for file_path in collected_files:
        filename = os.path.basename(file_path)
        file_listbox.insert(tk.END, filename)

def launch_ui():
    global file_listbox

    root = tk.Tk()
    root.title("File Renamer - Selection")
    root.geometry("1000x700")

    label = tk.Label(root, text="Adds files and/or folders to be renamed :", font=("Arial", 12))
    label.pack(pady=10)

    btn_files = tk.Button(root, text="Add files", command=select_files, width=30)
    btn_files.pack(pady=5)

    btn_folder = tk.Button(root, text="Add folder", command=select_folder, width=30)
    btn_folder.pack(pady=5)

    btn_validate = tk.Button(root, text="Validate selection", command=validate_selection, width=30, bg="#4CAF50", fg="white")
    btn_validate.pack(pady=10)

    preview_label = tk.Label(root, text="Preview selected files :", font=("Arial", 10, "bold"))
    preview_label.pack(pady=(10, 0))

    # Frame for listbox + scrollbar
    listbox_frame = tk.Frame(root)
    listbox_frame.pack(pady=5)

    # Scrollbar
    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Listbox with fixed width and height
    file_listbox = tk.Listbox(listbox_frame, height=20, width=80, yscrollcommand=scrollbar.set, font=("Courier New", 10))
    file_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=file_listbox.yview)
    
    root.mainloop()
