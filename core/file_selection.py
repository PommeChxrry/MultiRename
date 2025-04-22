import os

def collect_files(mixed_paths=[]):
    # Retrieves a list of paths (files and folders)
    # Returns all files found (Level 1 if in a document)
    files = set()

    for path in mixed_paths:
        if os.path.isfile(path):
            files.add(path)
        elif os.path.isdir(path):
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isfile(full_path):
                    files.add(full_path)

    return list(files)

def remove_unwanted_file(file_list, file_to_remove):
    pass

def files_preview(file_list):
    # Displays files collected by collect_files
    print("\n--- Files Collected ---")
    for file_path in file_list:
        print(f"- {os.path.basename(file_path)} ({file_path})")
