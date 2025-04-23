import tkinter as tk
from tkinter import ttk

def open_renaming_interface(root, selected_paths):
    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root, text="Rename Files", font=("Arial", 18))
    title.pack(pady=20)

    # Selection box for different renaming option
    selection_label = ttk.Label(root, text="Please select a renaming option:", font=("Arial", 10, "bold"))
    selection_label.pack(pady=(10, 0))

    selection_frame = tk.Frame(root)
    selection_frame.pack(pady=10)

    selected_option = tk.StringVar()
    renaming_options = ttk.Combobox(selection_frame, textvariable=selected_option, state="readonly")

    # Values options
    renaming_options['values'] = ("Random names", "Custom name with index")
    renaming_options.current(0)
    renaming_options.pack(pady=5)

    # Just a placeholder for confirmation button (for now it does nothing)
    confirm_button = ttk.Button(root, text="Confirm", command=lambda: print("Selected:", selected_option.get()))
    confirm_button.pack(pady=20)

    # Preview files
    preview_label = tk.Label(root, text="Preview selected files :", font=("Arial", 10, "bold"))
    preview_label.pack(pady=(10, 0))

    listbox_frame = tk.Frame(root)
    listbox_frame.pack(pady=5)

    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    file_listbox = tk.Listbox(listbox_frame, height=20, width=80, yscrollcommand=scrollbar.set, font=("Courier New", 10))
    file_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=file_listbox.yview)

    # Confirm Button
    confirm_button = tk.Button(root, text="Confirm", width=15, bg="#2196F3", fg="white")
    confirm_button.place(relx=0.95, rely=0.95, anchor="se")

    # Back Button
    back_button = tk.Button(root, text="Back", width=15, bg="#ff0000", fg="white")
    back_button.place(relx=0.05, rely=0.95, anchor="sw")