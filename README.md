# ShadowFight2 简易转换器（中文版）
## 摘要
&emsp;&emsp;一个简单的Python项目，可帮助您完成文件转换，为《ShadowFight2》提供更佳的游戏体验。
## 项目介绍
### 代码说明
&emsp;&emsp;此处提供了一个EXE文件和一些源代码。若您希望直接使用本程序，只需下载EXE文件并运行它（注意：程序将在其所在目录中新建三个文件夹）。
&emsp;&emsp;若您希望通过源代码运行程序，需下载所有源码文件（.py、.txt、.ui），随后有两种选择：
1. 基于Qt框架的GUI程序（推荐）：
您需要运行`main_page.py`程序。在此之前，请通过终端执行以下命令安装PyQt6库：`pip install PyQt6`接着运行Python入口脚本`main_page.py`，并通过界面控件选择所需功能。
2. 直接接口程序（不推荐，已废弃）：
您需根据需求修改当前目录下的`config.txt`文件中的功能与参数，然后运行`main_command.py`脚本。此方法无需安装任何第三方库（所有依赖均为Python标准库），但建议在 Python 3.8及以上环境 中使用。仅当您处于不支持PyQt6的平台（如Android）时推荐此方式。
### 功能1：模型转换
#### 第一个按钮：.obj 转 .xml
&emsp;&emsp;通过此功能，您可将常见的Wavefront模型（.obj文件）便捷地转换为《ShadowFight2》专用模型（.xml文件）。
### 功能2：动作文件（.bin、.bytes）转换
#### 第二个按钮：.obj 转 .csv
&emsp;&emsp;将您的动作文件（大量.obj文件）反序列化，并以csv格式存储。
### 功能3：动作文件解码与编码
#### 最后两个按钮
&emsp;&emsp;将二进制动作文件解码为csv表格存储格式，或将csv表格中的动作信息编码为《ShadowFight2》可识别的二进制文件。
***
# ShadowFight2 Easy Switch(English Version)
## Abstract
&ensp;&ensp;&ensp;&ensp;A simple Python project that can help you complete file conversion will provide you with a better gaming experience in ShadowFight2
## Introduction
### Code Introduction
&ensp;&ensp;&ensp;&ensp;Here is an EXE file and some source code.If you want to use the program directly, simply download the EXE file and run it (note that it will create three new folders in its directory). 
&ensp;&ensp;&ensp;&ensp;If you prefer to run the program from the source code, you need to download all the source code(.py)(.txt)(.ui). And then, there are two options:
  1. GUI Application Built with Qt (Recommended): 
You need to run the  `main_page.py`  program. Before doing so, install the PyQt6 library by running the following command in your terminal:`pip install PyQt6`
Then, run the Python entry script  `main_page.py`  and use the widgets to select your desired feature.
  2. Direct Interface Program (Not Recommended, Deprecated): 
You need to modify the functions and parameters in the  `config.txt`  file located in the current directory according to your needs, then run the  `main_command.py`  script. This method requires no third-party libraries, as all dependencies are part of the Python standard library. However, it is advised to use Python 3.8 or higher. This approach is only recommended if you are working on platforms that lack PyQt6 support (e.g., Android).
### Function1: Model Transformation
#### The First Button: .obj to .xml
&ensp;&ensp;&ensp;&ensp;You can transform your Wavefont model(.obj) which is usually seen on the internet into ShadowFight2 model(.xml) conveniently by this function.
### Function2: Movement Files(.bin, .bytes) Transformation
#### The Second Button: .obj to .csv
&ensp;&ensp;&ensp;&ensp;Deserialize your action files (a large number of. obj files) and store them as a csv file.
### Function3: Movement Files Decode and Encode
#### The Last Two Buttons
&ensp;&ensp;&ensp;&ensp;Decode your binary action file into the storage format of a csv table, or encode the action information stored in csv table format into a binary file that ShadowFight2 can recognize
