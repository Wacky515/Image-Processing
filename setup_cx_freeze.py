# coding: utf-8

import sys
import os
from cx_Freeze import setup, Executable

file_path = input("guitplmatching.py")

if sys.platform == "win32":
    # "Win32GUI"
    base = None

    path_mcon = "C:\\tools\\miniconda3\\envs\\image_processing\\tcl\\"
    os.environ['TCL_LIBRARY'] = path_mcon + "\\tcl8.6"
    os.environ['TK_LIBRARY'] = path_mcon + "\\tk8.6"
else:
    # "Win32GUI"
    base = None

# import して使っているライブラリを記載
packages = []

# import して使っているライブラリを記載（こちらの方が軽くなるという噂）
includes = [
    "os",
    "sys",
    "cv2",
    "time",
    "pickle",
    "pprint",
    "importlib",
]

# excludes では、パッケージ化しないライブラリやモジュールを指定する。
# numpy, pandas, lxmlは非常に重いので使わないなら除く
# 他にも、PIL(5MB)など
excludes = [
    "pandas",
    "lxml"
    ]

exe = Executable(
    script=file_path,
    base=base
    )

# セットアップ
setup(name='main',
      options={
          "build_exe": {
              "packages": packages,
              "includes": includes,
              "excludes": excludes,
          }
      },
      version='0.1',
      description='converter',
      executables=[exe])
