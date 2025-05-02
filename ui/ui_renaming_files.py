import tkinter as tk
from tkinter import ttk, messagebox
import re
from core.utils import generate_custom_name, generate_random_name
from ui.ui_renaming_progress import open_renaming_progress_interface

def validate_numeric_input(text):
    return text.isdigit() or text == ""

def validate_filename_input(text):
    return re.match(r'^[\w\- ]*$', text) is not None

def update_rename_files_preview(file_list, original_listbox, new_listbox):
    original_listbox.delete(0, tk.END)
    new_listbox.delete(0, tk.END)
    for file in file_list:
        original_listbox.insert(tk.END, file['original_name'])
        new_listbox.insert(tk.END, file['new_name'])

def open_renaming_interface(root, files_info):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("File Renamer - Renaming Option")

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

    # Warning label for displaying messages if no files
    warning_label = tk.Label(root, text="", font=("Arial", 10), fg="red")
    warning_label.pack(pady=(5, 0))

    # Container to put custom_input
    custom_input_container = tk.Frame(root)
    custom_input_container.pack(pady=5)

    # Frame for custom input (hidden by default)
    custom_input_frame = tk.Frame(root)

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
            custom_input_frame.pack(in_=custom_input_container)
        else:
            custom_input_frame.pack_forget()

    selected_option.trace_add("write", update_inputs)

    # Call once to ensure correct initial state
    update_inputs()

    # Select Button
    def on_select():
        if selected_option.get() == "Custom name with index" and base_name_entry.get().strip() == "":
            warning_label.config(text="Please type at least one character in base name", fg="red")
            return
        warning_label.config(text="")

        if selected_option.get() == "Random names":
            for file in files_info:
                random_name = generate_random_name()
                file['new_name'] = random_name + file['extension']
        
        elif selected_option.get() == "Custom name with index":
            base_name = base_name_entry.get().strip()
            start_index = int(index_entry.get().strip() or 1)
            for idx, file in enumerate(files_info, start=start_index):
                custom_name = generate_custom_name(base_name, idx)
                file['new_name'] = custom_name + file['extension']
        
        print("Selected:", selected_option.get())
        update_rename_files_preview(files_info, original_listbox, new_listbox)

    select_button = ttk.Button(root, text="Select", command=on_select)
    select_button.pack(pady=20)

    # Preview files
    preview_label = tk.Label(root, text="Preview selected files :", font=("Arial", 10, "bold"))
    preview_label.pack(pady=(10, 0))

    columns_frame = tk.Frame(root)
    columns_frame.pack(pady=5)

    # Titles for columns
    original_name_label = tk.Label(columns_frame, text="Original Name", font=("Arial", 10, "bold"))
    original_name_label.grid(row=0, column=0, padx=20)

    new_name_label = tk.Label(columns_frame, text="New Name", font=("Arial", 10, "bold"))
    new_name_label.grid(row=0, column=1, padx=20)

    # Frames for listboxes
    listboxes_frame = tk.Frame(root)
    listboxes_frame.pack(pady=5)

    # Scrollbar shared between the two listboxes
    shared_scrollbar = tk.Scrollbar(listboxes_frame)
    shared_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Left listbox (original names)
    original_listbox = tk.Listbox(listboxes_frame, height=20, width=40, font=("Courier New", 10), yscrollcommand=lambda *args: on_scroll(*args))
    original_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

    # Right listbox (new names)
    new_listbox = tk.Listbox(listboxes_frame, height=20, width=40, font=("Courier New", 10), yscrollcommand=lambda *args: on_scroll(*args))
    new_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

    # Function to synchronize scrolling from original and new listbox
    def on_scroll(*args):
        if args[0] == "moveto":
            original_listbox.yview_moveto(args[1])
            new_listbox.yview_moveto(args[1])
        elif args[0] == "scroll":
            original_listbox.yview_scroll(int(args[1]), args[2])
            new_listbox.yview_scroll(int(args[1]), args[2])

    # Connect the scrollbar to the scrolling function
    original_listbox.config(yscrollcommand=shared_scrollbar.set)
    new_listbox.config(yscrollcommand=shared_scrollbar.set)
    shared_scrollbar.config(command=on_scroll)

    def confirm_renaming():
        if any(file.get("new_name", "") == "" for file in files_info):
            messagebox.showwarning("No Rename Applied", "Please apply a renaming mode before confirming.")
            return
    
        confirm = messagebox.askyesno("Confirm Renaming", "Are you sure you want to rename the files?")
        if confirm:
            print("Renaming confirmed")
            open_renaming_progress_interface(root, files_info)
        else:
            print("Renaming canceled")

    # Confirm Button
    confirm_button = tk.Button(root, text="Confirm", width=15, bg="#2196F3", fg="white", command=confirm_renaming)
    confirm_button.place(relx=0.95, rely=0.95, anchor="se")

    # Back Button
    def on_back_click():
        root.destroy()

        from ui.ui_select_files import open_file_selection_interface
        open_file_selection_interface(files_info=files_info)

    back_button = tk.Button(root, text="Back", width=15, bg="#ff0000", fg="white", command=on_back_click)
    back_button.place(relx=0.05, rely=0.95, anchor="sw")