# PandaFPS
An FPS controller made in Panda3D

# System Requirements
A Windows PC (XP+)
Panda3D installed properly (the PIP version)
Linux or MacOS are currrently NOT supported although this can be changed by changing the model path in the source code (See the bottom of this Readme). If you don't know what you're doing, don't do it!

# About
This is a simple FPS controller made by a one-person development studio. Raycast bullets/advanced object collision will be added soon!

# How to install
You need the latest version of Panda3D from the official website. The PIP version was used in development so it is reccomended that you use that. As Panda3D is bundled with a special version of Python with PATH requirements satisfied, you only need Python for downloading with PIP. Releases with custom development features are hosted on mega.nz. You can pick a up a release from here, unzip it, and move the models directly from the models folder to the models folder in the Panda3D files on the root of your "C:" drive. If you want a stable or beta release, pick the package up from GitHub releases and follow the same installation steps.
# More
This movement controller is most likely very buggy. Please report bugs in the issues tab.
When the game starts you may notice significant frame drops/skips. This is COMPLETELY normal and is because of PyAutoGUI (which manages the cursor) callibrating its clock and active times with that of Panda3D.

# Linux/macOS?
This engine currently doesn't support Linux and macOS for around 2 main reasons: 

1. Some lines of code in the source code require Windows-only libraries for mouse position-detection. Yes... Panda3D also supports these callouts on Linux but I am too lazy to actually implement them (don't worry I'll add them in the near future!). I would tell you exactly which lines but again, I am too lazy. Just go and try to run on Linux. Once you get errors about some sort of function that was called out in the code which was missing, you must refer to the Panda3D documentation and find a replacement.

2. Currently, the model importing system requires you to go to the root of your "C:" drive, into the Panda3D folder, and putting the necessary models in. The game then imports them as actor (rigged player-models). This is not a "problem" per se, but you must put your models in a different path (somewhere in your usr/ folder where the program files are located). This can easily be fixed and will be automatically implemented in a future update.

# Buy me a coffee!
Being a developer is hard work and requires a lot of time. Supporting me on Patreon really means a lot and will also allow me to release more updates/bugfixes to this project.

# Thanks for using and subscribe to PANDA_REAPER on Youtube for more!

