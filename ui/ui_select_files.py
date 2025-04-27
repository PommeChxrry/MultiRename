import tkinter as tk
import os
from tkinter import filedialog
from core.file_selection import collect_files, files_preview
from ui.ui_renaming_files import open_renaming_interface

# Global list to store selected files
files_info = []

def select_files():
    global files_info

    # Select files and add into mixed_paths
    files = filedialog.askopenfilenames(title="Select files")
    if files:
        mixed_paths = [file for file in files]
        files_info.extend(collect_files(mixed_paths))
        files_preview(files_info)
        update_listbox()

def select_folder():
    global files_info

    # Select folder and add files from folder into selected_paths
    folder = filedialog.askdirectory(title="Select folder")
    if folder:
        mixed_paths = [folder]
        files_info.extend(collect_files(mixed_paths))
        files_preview(files_info)
        update_listbox()

def update_listbox():
     # Update the preview without duplicates
    current_displayed_files = [file_listbox.get(i) for i in range(file_listbox.size())]
    for file in files_info:
        if file['original_name'] not in current_displayed_files:
            file_listbox.insert(tk.END, file['original_name'])

def open_file_selection_interface():
    global file_listbox

    root = tk.Tk()
    root.title("File Renamer - Selection")
    root.geometry("1400x900")

    label = tk.Label(root, text="Adds files and/or folders to be renamed :", font=("Arial", 18))
    label.pack(pady=10)

    btn_files = tk.Button(root, text="Add files", command=select_files, width=30)
    btn_files.pack(pady=5)

    btn_folder = tk.Button(root, text="Add folder", command=select_folder, width=30)
    btn_folder.pack(pady=5)

    def on_next_click():
        if not files_info:
            warning_label.config(text="Please select at least one file or folder.", fg="red")
        else:
            open_renaming_interface(root, files_info)

    # Warning label for displaying messages if no files
    warning_label = tk.Label(root, text="", font=("Arial", 10), fg="red")
    warning_label.pack(pady=(5, 0))

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

    # Next Button
    next_button = tk.Button(root, text="Next", width=15, bg="#2196F3", fg="white", command=on_next_click)
    next_button.place(relx=0.95, rely=0.95, anchor="se")

    scrollbar.config(command=file_listbox.yview)
    
    root.mainloop()
