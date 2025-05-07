import os
from tkinter import messagebox

def rename_files(files_info, progress_callback=None, final_callback=None):
    total = len(files_info)
    renamed_count = 0

    for i, file in enumerate(files_info, start=1):
        old_path = file["original_path"]
        directory = os.path.dirname(old_path)
        base_new_name = file["new_name"]

        if not base_new_name:
            print(f"Skipping file with no new name: {old_path}")
            continue

        new_name = base_new_name
        counter = 1
        new_path = os.path.join(directory, new_name)

        while os.path.exists(new_path):
            new_name = f"{base_new_name}({counter})"
            new_path = os.path.join(directory, new_name)
            counter += 1

        try:
            os.rename(old_path, new_path)
            renamed_count += 1
            print(f"Renamed: {old_path} -> {new_path}")
        except Exception as e:
            print(f"Error renaming {old_path} to {new_path}: {e}")

        if progress_callback:
            progress_callback(i, total)

    if final_callback:
        final_callback(renamed_count)

def show_remaining_progress(current, total):
    print(f"Renaming files: {current}/{total}")

def final_confirmation_message(renamed_file):
    messagebox.showinfo("Renaming Complete", f"Renaming finished. {renamed_file} files were successfully renamed.")