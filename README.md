# Rename File Project

A simple Python application that allows users to rename multiple files (images, documents...) at once based on different criteria.  
This tool is designed to be easy to use, with a clean interface and customizable renaming options.

## Features

- Select one or more folders and/or individual files
- Choose between two renaming modes:
  - Random names (letters and numbers)
  - Custom names with sequential numbering
- Preview before renaming (old name → new name)
- Preserve original file properties (creation date, size, type)
- Add a visual progress indicator during file renaming

## Usage

### To launch the application:

From the project folder, run in the terminal :
```bash
python main.py
```
### Into the application

- Select folders and/or files as it says then confirm
- Choose a renaming mode (random or custom name with index).
- Preview the changes.
- Click Confirm to rename.

### Important

Files are renamed directly - make backups if needed.  
Currently tested only on Windows.  
Linux/macOS support not guaranteed yet.

## Future Features

Planned improvements for upcoming versions:

- Allow users to remove unwanted files before starting the renaming process
- Improve the preview display (with information about the file (localisation, creation date etc.))

## Notes

This is a personal project, currently functional and tested on **Windows**.  
It is still under development and may evolve in future versions.  
**Use at your own risk** – always back up your files before renaming.  
