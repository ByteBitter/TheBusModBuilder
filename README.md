# The Bus Mod Builder

A tool to quickly rebuild mods for the game "The Bus".


## DISCLAIMER - USE AT YOUR OWN RISK

This software was made with my last 3 braincells and a little help of ChatGPT...

**Use at your own risk** — if anything goes wrong, I am not responsible. Your computer, your problem. Happy Modding!


## So how does this work ?

This tool allows you to build any mods you created inside the The Bus Modding Editor. It also enables you to use multible build versions (like 'stable' or 'beta')


## Requirements

You need the [The Bus Modding Editor](https://store.epicgames.com/de/p/the-bus-modding-editor) installed on your PC.

Check out the developers dicord server, there you can find all the information you need:

[TML Studios Discord Server](https://discord.gg/tml-studios-224563159631921152)


## Config

![](/media/Config.png)

When using the tool for the first time, you need to configure at least one "Version":

1. Switch to the "Configuration" tab and click on "Add version"

2. Enter a Name for the version - this can be anything you want ('stable', 'beta', ...)

3. After entering the name, the tool will open a folder selection dialog - now navigate to the root folder of your modding editor installation and click "select folder", for me it is: `V:\Epic\TheBusModdingEditor`

4. Now you should see the config in the "Configuration" tab and there should be a `mod_config.json` file inside the folder where the tool is stored 

5. (optional) you can add custom build arguments: click on the "Custom Args" button next to a config and write the arguments into the popup. - build arguments are stored separatly inside the 


## How to use the tool

![](/media/BuildDone.png)

1. Select the Mod
2. Select the Version
3. Hit the "Build Mod" Button
4. Wait - building a mod can take a while

The Build is done, when you see the red-ish `tkterminal$` at the bottom of the console window.


## Nerd stuff - whats inside?

- tkinter
- tkterminal



