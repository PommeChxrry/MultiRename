import tkinter as tk
from tkinter import ttk
import re

def validate_numeric_input(text):
    return text.isdigit() or text == ""

def validate_filename_input(text):
    return re.match(r'^[\w\- ]*$', text) is not None

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

    # Frame for custom input (hidden by default)
    custom_input_frame = tk.Frame(root)
    # TODO : Essayer de placer entre Combobox et bouton select les label et entry de Custom name with index

    vcmd_filename = root.register(validate_filename_input)
    base_name_label = ttk.Label(custom_input_frame, text="Base name:")
    base_name_entry = ttk.Entry(custom_input_frame, validate="key", validatecommand=(vcmd_filename, "%P"))

    vcmd_numeric = root.register(validate_numeric_input)
    index_label = ttk.Label(custom_input_frame, text="Start index:")
    index_entry = ttk.Entry(custom_input_frame, validate="key", validatecommand=(vcmd_numeric, "%P"))
    index_entry.insert(0, "1")

    base_name_label.grid(row=0, column=0, padx=5)
    base_name_entry.grid(row=0, column=1, padx=5)
    index_label.grid(row=0, column=2, padx=5)
    index_entry.grid(row=0, column=3, padx=5)

    # Function to show/hide custom input
    def update_inputs(*args):
        if selected_option.get() == "Custom name with index":
            custom_input_frame.pack(pady=5)
        else:
            custom_input_frame.pack_forget()

    selected_option.trace_add("write", update_inputs)

    # Call once to ensure correct initial state
    update_inputs()

    # Insert the custom input frame here so it's between combobox and select
    custom_input_frame.pack_forget()  # keep it hidden initially

    # Select button
    select_button = ttk.Button(root, text="Select", command=lambda: print("Selected:", selected_option.get()))
    select_button.pack(pady=20)

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