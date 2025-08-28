import os
import uuid
from tkinter import messagebox

def rename_files(files_info, progress_callback=None, final_callback=None):
    total = len(files_info)
    renamed_count = 0
    processed = 0

    new_names_map = {}
    used_targets = set()

    for file in files_info:
        old_path = file["original_path"]
        directory = os.path.dirname(old_path)
        base_new_name = file.get("new_name", "")

        if not base_new_name:
            print(f"Skipping file with no new name: {old_path}")
            continue

        name, ext = os.path.splitext(base_new_name)
        new_name = base_new_name
        counter = 1

        new_full_path = os.path.join(directory, new_name)
        while new_full_path in used_targets:
            new_name = f"{name}({counter}){ext}"
            new_full_path = os.path.join(directory, new_name)
            counter += 1

        new_names_map[old_path] = new_full_path
        used_targets.add(new_full_path)

    pending = dict(new_names_map)

    def make_temp_for(path):
        d = os.path.dirname(path)
        base, ext = os.path.splitext(os.path.basename(path))
        while True:
            tmp = os.path.join(d, f"{base}.__tmp__{uuid.uuid4().hex}__{ext}")
            if not os.path.exists(tmp) and tmp not in pending and tmp not in pending.values():
                return tmp

    while pending:
        progress_made = False

        for src, dst in list(pending.items()):
            if src == dst:
                del pending[src]
                processed += 1
                if progress_callback:
                    progress_callback(processed, total)
                progress_made = True
                continue

            if dst in pending.keys():
                continue

            final_dst = dst
            if os.path.exists(final_dst):
                d = os.path.dirname(final_dst)
                b, e = os.path.splitext(os.path.basename(final_dst))
                c = 1
                candidate = os.path.join(d, f"{b}({c}){e}")
                while os.path.exists(candidate) or candidate in pending.values() or candidate in used_targets:
                    c += 1
                    candidate = os.path.join(d, f"{b}({c}){e}")
                used_targets.discard(dst)
                used_targets.add(candidate)
                pending[src] = candidate
                final_dst = candidate

            try:
                os.rename(src, final_dst)
                renamed_count += 1
                print(f"Renamed: {src} -> {final_dst}")
                del pending[src]
                processed += 1
                if progress_callback:
                    progress_callback(processed, total)
                progress_made = True
            except Exception as e:
                print(f"Error renaming {src} to {final_dst}: {e}")

        if progress_made:
            continue

        src, dst = next(iter(pending.items()))
        try:
            tmp = make_temp_for(src)
            os.rename(src, tmp)
            print(f"Staged (cycle break): {src} -> {tmp}")
            del pending[src]
            pending[tmp] = dst
        except Exception as e:
            print(f"Error staging {src} to temporary path: {e}")
            
    if final_callback:
        final_callback(renamed_count)

def show_remaining_progress(current, total):
    print(f"Renaming files: {current}/{total}")

def final_confirmation_message(renamed_file):
    messagebox.showinfo("Renaming Complete", f"Renaming finished. {renamed_file} files were successfully renamed.")