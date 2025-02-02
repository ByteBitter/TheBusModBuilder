import json
import tkinter as tk
from tkterminal import Terminal
from tkinter import ttk, messagebox, filedialog, simpledialog
from pathlib import Path
import subprocess
import os

MODS_FOLDER = Path.home() / 'Documents' / 'The Bus' / 'Mods'
print(MODS_FOLDER)
CONFIG_FILE = "mod_config.json"

def get_available_mods():
    if not os.path.exists(MODS_FOLDER):
        return []
    return [f for f in os.listdir(MODS_FOLDER) if os.path.isdir(os.path.join(MODS_FOLDER, f))]

def build_mod():
    mod_name = mod_var.get()
    version_key = version_var.get()
    
    if not mod_name or version_key not in config["versions"]:
        messagebox.showerror("Error", "Invalid selection!")
        return
    
    version_data = config["versions"][version_key]
    base_path = version_data["path"]
    extra_args = version_data.get("extra_args", "")
    
    exe_path = os.path.join(base_path, "Engine/Binaries/Win64/UnrealEditor-Cmd.exe")
    uproject = os.path.join(base_path, "Fernbus.uproject")
    
    command = f'"{exe_path}" "{uproject}" -activemod={mod_name} -run=CookModCommandlet {extra_args}'
    print(command)
    terminal.clear()
    terminal.run_command(command)

def update_mod_dropdown():
    mods = get_available_mods()
    mod_dropdown["values"] = mods
    if mods:
        mod_var.set(mods[0])

def update_version_dropdown():
    versions = list(config["versions"].keys())
    version_dropdown["values"] = versions
    if versions:
        version_var.set(versions[0])

def add_version():
    version_name = simpledialog.askstring("Add Version", "Enter custom version name:")
    if version_name:
        folder_selected = filedialog.askdirectory(title="Select Base Folder for Version")
        if folder_selected:
            config["versions"][version_name] = {"path": folder_selected, "extra_args": ""}
            save_config()
            update_version_list()
            update_version_dropdown()

def remove_version(version_name):
    if version_name in config["versions"]:
        del config["versions"][version_name]
        save_config()
        update_version_list()
        update_version_dropdown()

def edit_version(version_name):
    new_extra_args = simpledialog.askstring("Edit Extra Arguments", f"Enter extra arguments for {version_name}:", initialvalue=config["versions"].get(version_name, {}).get("extra_args", ""))
    if new_extra_args is not None:
        config["versions"][version_name]["extra_args"] = new_extra_args
        save_config()
        update_version_list()

def open_folder(path):
    if os.path.exists(path):
        os.system(f"explorer {path}")

def update_version_list():
    for widget in config_frame.winfo_children():
        widget.destroy()
    
    for version_name, version_data in config["versions"].items():
        frame = tk.Frame(config_frame)
        frame.pack(fill="x", pady=2)
        
        tk.Label(frame, text=version_name, width=20, anchor="w").pack(side="left")
        tk.Label(frame, text=version_data["path"], anchor="w").pack(side="left")
        tk.Button(frame, text="Edit", command=lambda v=version_name: edit_version(v)).pack(side="right", padx=5)
        tk.Button(frame, text="Delete", command=lambda v=version_name: remove_version(v)).pack(side="right")
        tk.Button(frame, text="Open Folder", command=lambda p=version_data["path"]: open_folder(p)).pack(side="right", padx=5)

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def create_tabs():
    global config_frame
    global terminal
    notebook = ttk.Notebook(root)
    main_tab = ttk.Frame(notebook)
    config_tab = ttk.Frame(notebook)
    config_frame = tk.Frame(config_tab)
    
    notebook.add(main_tab, text="Main")
    notebook.add(config_tab, text="Configuration")
    notebook.pack(expand=True, fill="both")
    
    tk.Label(main_tab, text="Select Mod:").pack()
    global mod_var, mod_dropdown
    mod_var = tk.StringVar()
    mod_dropdown = ttk.Combobox(main_tab, textvariable=mod_var)
    mod_dropdown.pack()
    update_mod_dropdown()
    
    tk.Label(main_tab, text="Select Version:").pack()
    global version_var, version_dropdown
    version_var = tk.StringVar()
    version_dropdown = ttk.Combobox(main_tab, textvariable=version_var)
    version_dropdown.pack()
    update_version_dropdown()
    
    tk.Button(main_tab, text="Build Mod", command=build_mod).pack(pady=5)

    terminal = Terminal(main_tab, pady=5, padx=5, background="black")
    terminal.pack(expand=True, fill='both')
    
    tk.Button(config_tab, text="Add Version", command=add_version).pack(pady=5)
    config_frame.pack(fill="both", expand=True)
    update_version_list()

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"versions": {}}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()
root = tk.Tk()
root.title("The Bus Mod Builder")
root.geometry("1500x700")
create_tabs()
root.mainloop()
