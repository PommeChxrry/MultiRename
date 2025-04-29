import os
from tkinter import messagebox

def rename_files(files_info):
    for file in files_info:
        old_path = file["original_path"]
        directory = os.path.dirname(old_path)
        extension = file["extension"]
        base_new_name = file["new_name"]

        if not new_name:
            print(f"Skipping file with no new name: {old_path}")
            continue

        new_name = base_new_name
        counter = 1
        new_path = os.path.join(directory, new_name + extension)

        while os.path.exists(new_name):
            new_name = f"{base_new_name}({counter})"
            new_path = os.path.join(directory, new_name + extension)
            counter += 1

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")
        except Exception as e:
            print(f"Error renaming {old_path} to {new_path}: {e}")

def disable_exit():
    # Shows only the warning
    messagebox.showwarning("Action blocked", "Renaming in progress. Please wait until it finishes.")

def show_remaining_progress(current, total):
    print(f"Renaming files: {current}/{total}")

def final_confirmation_message(renamed_file):
    messagebox.showinfo("Renaming Complete", f"Renaming finished. {renamed_file} files were successfully renamed.")