import os

def collect_files(mixed_paths=[]):
    # Retrieves a list of paths (files and folders)
    # Returns all files found (Level 1 if in a document) by creation date
    files = set()

    for path in mixed_paths:
        if os.path.isfile(path):
            files.add(path)
        elif os.path.isdir(path):
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isfile(full_path):
                    files.add(full_path)

    # Convert to structured info list
    files_info = []
    for file in files:
        filename = os.path.basename(file)
        name_without_ext, ext = os.path.splitext(filename)
        files_info.append({
            "original_path": file,
            "original_name": filename,
            "extension": ext,
            "new_name": "",
            "created_time": os.path.getctime(file)
        })

    # Sort by creation date
    files_info.sort(key=lambda x: x["created_time"])

    return files_info

def remove_unwanted_file(files_info, file_to_remove):
    pass

def files_preview(files_info):
    # Displays files collected by collect_files
    print("\n--- Files Collected ---")
    for file in files_info:
        print(f"- {file['original_name']} ({file['original_path']})")
