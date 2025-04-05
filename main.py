import json
import tkinter as tk
from tkterminal import Terminal
from tkinter import ttk, messagebox, filedialog, simpledialog
from pathlib import Path
from uuid import uuid4
import os
from TheBusModBuilder import ModBuilderVersion

CONFIG_FILE = "mod_config.json"

def getAviableMods():
    MODS_FOLDER = config.get("modsFolder","")
    if not os.path.exists(MODS_FOLDER):
        return []
    return [f for f in os.listdir(MODS_FOLDER) if os.path.isdir(os.path.join(MODS_FOLDER, f))]

def buildMod():
    mod_name = mod_var.get()
    version_index = version_dropdown.current()

    version_key = list(versions.keys())[version_index]
    
    if not mod_name or version_key not in versions:
        messagebox.showerror("Error", "Invalid selection!")
        return
    
    version = versions[version_key]

    command = version.GetBuildModCommand(mod_name)
    
    print(command)
    terminal.clear()
    terminal.run_command(command)

def updateModsFolder():
    folder_selected = filedialog.askdirectory(title="Select Base Folder for Mods")
    if folder_selected:
        config["modsFolder"] = folder_selected
        updateAviableModsDropdown()
        saveConfig()

def updateAviableModsDropdown():
    mods = getAviableMods()
    mod_dropdown["values"] = mods
    if mods:
        mod_var.set(mods[0])

def updateVersionsDropdown():
    version_names = []
    for version_name, version in versions.items():
        version_names.append(version.getNameWithEnviroment())
    version_dropdown["values"] = version_names
    if version_names:
        version_var.set(version_names[0])

def addVersion():
    version_name = simpledialog.askstring("Add Version", "Enter custom version name:")
    if version_name:
        folder_selected = filedialog.askdirectory(title="Select Base Folder for Version")
        if folder_selected:
            newid = str(uuid4())
            newVersion = ModBuilderVersion(id=newid, tkinterRoot=root, updateView=updateVersionView, removeVersion=removeVersion, saveSettings=saveConfig, updateVersionDropdown=updateVersionsDropdown, settings={"name":version_name, "path":folder_selected})
            versions[newid] = newVersion
            saveConfig()
            updateVersionView()
            updateVersionsDropdown()

def removeVersion(version_id):
    if version_id in config["versions"]:
        del config["versions"][version_id]
        if version_id in versions:
            del versions[version_id]
        updateVersionView()
        updateVersionsDropdown()
        saveConfig()

def updateVersionView():
    for widget in config_frame.winfo_children():
        widget.destroy()
    
    for version_name, version in versions.items():
        version.BuildVersionFrame(config_frame)

def saveConfig():
    with open(CONFIG_FILE, "w") as f:
        for versionID, versionData in versions.items():
            config["versions"][versionID] = versionData.GetSettingsDict()
        json.dump(config, f, indent=4)

def createTabs():
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
    updateAviableModsDropdown()
    
    tk.Label(main_tab, text="Select Version:").pack()
    global version_var, version_dropdown
    version_var = tk.StringVar()
    version_dropdown = ttk.Combobox(main_tab, textvariable=version_var)
    version_dropdown.pack()
    updateVersionsDropdown()
    
    tk.Button(main_tab, text="Build Mod", command=buildMod).pack(pady=5)

    terminal = Terminal(main_tab, pady=5, padx=5, background="black")
    terminal.pack(expand=True, fill='both')
    
    tk.Button(config_tab, text="Select Mods Folder", command=updateModsFolder).pack(pady=5)
    tk.Button(config_tab, text="Add Version", command=addVersion).pack(pady=5)
    config_frame.pack(fill="both", expand=True)
    updateVersionView()


def loadVersionsandSettings():
    if not os.path.exists(CONFIG_FILE):
        return {"versions": {}, "modsFolder":str('Documents/The Bus/Mods')}, {}
    
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

        versions = {}
        for versionID, versionData in data["versions"].items():
            newVersionObject = ModBuilderVersion(id=versionID, tkinterRoot=root, updateView=updateVersionView, removeVersion=removeVersion, saveSettings=saveConfig, updateVersionDropdown=updateVersionsDropdown, settings=versionData)
            versions[versionID] = newVersionObject

        if 'modsFolder' not in data:
            data["modsFolder"] = str('Documents/The Bus/Mods')
            print(data)

        return data, versions
    


root = tk.Tk()
config, versions = loadVersionsandSettings()
root.title("The Bus Mod Builder")
root.geometry("1500x700")
createTabs()
saveConfig()
root.mainloop()
