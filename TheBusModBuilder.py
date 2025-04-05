#### Class to manage a version

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import webbrowser


class ModBuilderVersion(object):
    def __init__(self, id, tkinterRoot:tk.Frame, updateView, removeVersion, saveSettings, updateVersionDropdown, settings:dict={}):
        self.uuid = id
        self.Name = settings.get("name", id)
        self.Path = settings.get("path", "")
        self.ExtraArgs = settings.get("extra_args", "")

        self.UpdateView = updateView
        self.RemoveVersion = removeVersion
        self.SaveSettings = saveSettings
        self.UpdateVersionDropdown = updateVersionDropdown

        ## Build Roadmap
        self.BuildRoadmapVar = tk.BooleanVar(value=settings.get("build_roadmap", False))

        ## Build Environment (0 == Only Client, 1 = Only Server, 2 = Both)
        self.BuildEvironmentVar = tk.IntVar(value=settings.get("build_environment", 0))

    def GetSettingsDict(self):
        settings = {
            "name": self.Name,
            "path": self.Path,
            "extra_args": self.ExtraArgs,
            "build_roadmap":self.BuildRoadmapVar.get(),
            "build_environment":self.BuildEvironmentVar.get()
        }
        return settings
    
    def GetBuildModCommand(self, mod_name:str):
        exe_path = os.path.join(self.Path, "Engine/Binaries/Win64/UnrealEditor-Cmd.exe")
        uproject = os.path.join(self.Path, "Fernbus.uproject")

        command = f'"{exe_path}" "{uproject}" -activemod={mod_name} -run=CookModCommandlet {self.GetBuildEnv()} {self.GetBuildRoadmap()} {self.ExtraArgs}'

        return command
    

    def GetBuildEnv(self):

        match self.BuildEvironmentVar.get():
            case 0:
                return "-environment=client"
            case 1:
                return "-environment=server"
            case 2:
                return "-environment=clientandserver"
            case _:
                return ""
            
    def getNameWithEnviroment(self):

        env = ""
        match self.BuildEvironmentVar.get():
            case 0:
                return f"{self.Name}  [Client]"
            case 1:
                return f"{self.Name}  [Server]"
            case 2:
                return f"{self.Name}  [Client + Server]"
            case _:
                return f"{self.Name}"
            
            
    def GetBuildRoadmap(self):
        if(self.BuildRoadmapVar.get()):
            return "-buildroadmap"
        return ""
    

    def BuildVersionFrame(self, config_frame:tk.Frame):
        frame = tk.Frame(config_frame)
        frame.pack(fill="x", pady=2)
        
        tk.Label(frame, text=self.Name, width=20, anchor="w").pack(side="left")
        tk.Label(frame, text="\tBuild Environment:", anchor="w").pack(side="left")
        tk.Radiobutton(frame, text="Only Client", variable=self.BuildEvironmentVar, value=0, padx=5, command=lambda : self.VersionUpdated()).pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Only Server", variable=self.BuildEvironmentVar, value=1, padx=5, command=lambda : self.VersionUpdated()).pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Client + Server", variable=self.BuildEvironmentVar, value=2, padx=5, command=lambda : self.VersionUpdated()).pack(side=tk.LEFT)
        tk.Label(frame, text="\tSpecial:", anchor="w").pack(side="left")
        tk.Checkbutton(frame, text="Build Roadmap", variable=self.BuildRoadmapVar, command=lambda : self.VersionUpdated()).pack(side=tk.LEFT)
        tk.Label(frame, text=f"\t{self.Path}", anchor="w").pack(side="left")
        tk.Button(frame, text="Delete", command=lambda v=self.Name: self.RemoveVersion(v)).pack(side="right")
        tk.Button(frame, text="Open Folder", command=lambda p=self.Path: self.OpenFolder(p)).pack(side="right", padx=5)
        tk.Button(frame, text="Custom Args", command=lambda : self.EditExtraArgs()).pack(side="right", padx=5)
        tk.Button(frame, text="Change Name", command=lambda : self.EditName()).pack(side="right", padx=5)


    def VersionUpdated(self):
        self.UpdateVersionDropdown()
        self.SaveSettings()


    def EditExtraArgs(self):
        new_extra_args = simpledialog.askstring("Edit Extra Arguments", f"Enter extra arguments for {self.Name}:", initialvalue=self.ExtraArgs)
        if new_extra_args is not None:
            self.ExtraArgs = new_extra_args

        self.UpdateView()
        self.SaveSettings()

    def EditName(self):
        new_Name = simpledialog.askstring("Edit Name", f"Rename: {self.Name}:", initialvalue=self.Name)
        if new_Name is not None:
            self.Name = new_Name

        self.VersionUpdated()
        self.UpdateView()


    def OpenFolder(self, path):
        if os.path.exists(path):
            webbrowser.open(path)
            