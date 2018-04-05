import sys,os
from cx_Freeze import setup, Executable

# set TCL_LIBRARY='C:\Program Files\python36\tcl\tcl8.6'
# set TK_LIBRARY='C:\Program Files\python36\tcl\tk8.6'
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'includes':[],'packages': ["tkinter",'xlwings'],'excludes':['numpy','pillow','test'],'include_files':[
            'huba3.gif',
            r"C:\Program Files\python36\DLLs\tcl86t.dll", r"C:\Program Files\python36\DLLs\tk86t.dll"
            # os.path.join('C:\Program Files\python36\Lib\site-packages\pywin32_system32\pythoncom36.dll'),
            # os.path.join('C:\Program Files\python36\Lib\site-packages\pywin32_system32\pywintypes36.dll')
         ]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = "Win32GUI"
# if sys.platform == "win32":
    # base = "Win32GUI"

setup(  name = "ginical",
        version = "0.1",
        description = "gini cal",
        options = {"build_exe": build_exe_options},
        executables = [Executable("ui.py", base=base)])