import tkinter as tk
from tkinter import filedialog
from core.file_selection import collect_files, files_preview
from ui.ui_renaming_files import open_renaming_interface

def open_file_selection_interface(files_info=None):
    global file_listbox

    if files_info is None:
        files_info = []

    root = tk.Tk()
    root.title("File Renamer - Selection")
    root.geometry("1400x900")

    def update_listbox():
        # Update the preview without duplicates
        current_displayed_files = [file_listbox.get(i) for i in range(file_listbox.size())]
        for file in files_info:
            if file['original_name'] not in current_displayed_files:
                file_listbox.insert(tk.END, file['original_name'])

    def select_files():
        # Select files and add into mixed_paths
        files = filedialog.askopenfilenames(title="Select files")
        if files:
            mixed_paths = [file for file in files]
            files_info.extend(collect_files(mixed_paths))
            files_preview(files_info)
            update_listbox()

    def select_folder():
        # Select folder and add files from folder into selected_paths
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            mixed_paths = [folder]
            files_info.extend(collect_files(mixed_paths))
            files_preview(files_info)
            update_listbox()

    title = tk.Label(root, text="Select Files", font=("Arial", 18))
    title.pack(pady=20)

    label = tk.Label(root, text="Adds files and/or folders to be renamed :", font=("Arial", 12, "bold"))
    label.pack(pady=10)

    select_files_folder_frame = tk.Frame(root)
    select_files_folder_frame.pack(pady=5)

    btn_files = tk.Button(select_files_folder_frame, text="Add files", command=select_files, width=30)
    btn_files.pack(side=tk.LEFT, padx=10)

    btn_folder = tk.Button(select_files_folder_frame, text="Add folder", command=select_folder, width=30)
    btn_folder.pack(side=tk.RIGHT, padx=10)

    def on_next_click():
        if not files_info:
            warning_label.config(text="Please select at least one file or folder.", fg="red")
        else:
            # Sort by modified time
            files_info.sort(key=lambda x: x["modified_time"])
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

    if files_info:
        files_preview(files_info)
        update_listbox()
    
    root.mainloop()
