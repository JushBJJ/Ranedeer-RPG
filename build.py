import PyInstaller.__main__
import subprocess
import sys

run_flags=[
        "--name=Ranedeer-RPG",
        "--console",
        "--clean",
        "--onefile",
        "main.py",
        "Input.py",
        "Map.py",
        "Player.py",
        "Position.py"
    ]
if sys.platform=="linux":
    PyInstaller.__main__.run(run_flags)

elif sys.platform=="win32":
    PyInstaller.__main__.run(run_flags)
else:
    print("Unsupported.")
