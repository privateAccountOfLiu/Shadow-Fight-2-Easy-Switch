# ShadowFight2 Easy Switch(English Version)
## Abstract
&ensp;&ensp;&ensp;&ensp;A simple Python project that can help you complete file conversion will provide you with a better gaming experience in ShadowFight2
## Introduction
### Code Introduction
&ensp;&ensp;&ensp;&ensp;Here is an EXE file and some source code.If you want to use the program directly, simply download the EXE file and run it (note that it will create three new folders in its directory). 
&ensp;&ensp;&ensp;&ensp;If you prefer to run the program from the source code, you need to download all the source code(.py)(.txt)(.ui).And then, there are two options:
  1. GUI Application Built with Qt (Recommended): You need to run the  `main_page.py`  program. Before doing so, install the PyQt6 library by running the following command in your terminal:`pip install PyQt6`
Then, run the Python entry script  `main_page.py`  and use the widgets to select your desired feature.
  2. Direct Interface Program (Not Recommended, Deprecated): You need to modify the functions and parameters in the  `config.txt`  file located in the current directory according to your needs, then run the  `main_command.py`  script. This method requires no third-party libraries, as all dependencies are part of the Python standard library. However, it is advised to use Python 3.8 or higher. This approach is only recommended if you are working on platforms that lack PyQt6 support (e.g., Android).
### Function1: Model Transformation
#### The First Button: .obj to .xml
&ensp;&ensp;&ensp;&ensp;You can transform your Wavefont model(.obj) which is usually seen on the internet into ShadowFight2 model(.xml) conveniently by this function.
### Function2: Movement Files(.bin, .bytes) Transformation
#### The Second Button: .obj to .csv
&ensp;&ensp;&ensp;&ensp;Deserialize your action files (a large number of. obj files) and store them as a csv file.
### Function3: Movement Files Decode and Encode
#### The Last Two Buttons
&ensp;&ensp;&ensp;&ensp;Decode your binary action file into the storage format of a csv table, or encode the action information stored in csv table format into a binary file that ShadowFight2 can recognize