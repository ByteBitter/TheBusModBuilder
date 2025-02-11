# The Bus Mod Builder

This tool allows you to build any mod you created inside the "The Bus Modding Editor" without opening it.

[Download here](https://github.com/ByteBitter/TheBusModBuilder/releases/tag/V002)

## DISCLAIMER - USE AT YOUR OWN RISK

**This tool was created independently and is not affiliated with TML Studios.** 
If you run into any issues, feel free to reach out to me directly here for help. Thanks a bunch!

This software was made with my last 3 braincells and a little help of ChatGPT so... **Use it at your own risk**

If anything goes wrong, I am not responsible. You have been warned.

Happy Modding!


## Requirements

You need the [The Bus Modding Editor](https://store.epicgames.com/de/p/the-bus-modding-editor) installed on your PC.

Check out the developers dicord server, there you can find all the information you need:

[TML Studios Discord Server](https://discord.gg/tml-studios-224563159631921152)


## Config

![](/media/Config.gif)
When using the tool for the first time, you need to configure at least one "Version" and your "Mods" directory:

1. Switch to the "Configuration" tab and click on "Select Mods Folder" to select the Mods Folder and after that on "Add version"

2. Enter a Name for the version - this can be anything you want ('stable', 'beta', ...)

3. After entering the name, the tool will open a folder selection dialog - now navigate to the root folder of your modding editor installation and click "select folder", for me it is: `V:\Epic\TheBusModdingEditor`

4. Now you should see the config in the "Configuration" tab and there should be a `mod_config.json` file inside the folder where the tool is stored 

5. (optional) you can add custom build arguments: click on the "Custom Args" button next to a config and write the arguments into the popup. - build arguments are stored separatly for each created version


#### JSON Example

```
{
    "versions": {
        "Stable": {
            "path": "V:/Epic/TheBusModdingEditor",
            "extra_args": ""
        },
        "Beta": {
            "path": "V:/Epic/PublicBeta",
            "extra_args": ""
        }
    },
    "modsFolder": "C:/Users/User/Documents/The Bus/Mods"
}
```


## How to use the tool

![](/media/Build.gif)

1. Select the Mod
2. Select the Version
3. Hit the "Build Mod" Button
4. Wait - building a mod can take a while

The process is done, when the red-ish `tkterminal$` at the bottom of the console window is shown.

5. Start "The Bus" and test or upload your mod


## Nerd stuff - whats inside?

- tkinter
- tkterminal



