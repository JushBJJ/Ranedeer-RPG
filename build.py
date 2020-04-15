import PyInstaller.__main__
import subprocess
import sys

run_flags=[
        "--name=Ranedeer-RPG",
        "--console",
        "--clean",
        "--onefile",
        "RPG_main.py",
        "RPG_Input.py",
        "RPG_Map.py",
        "RPG_Player.py",
        "RPG_Position.py"
    ]

if sys.platform=="linux":
    run_flags.append("--strip")
    PyInstaller.__main__.run(run_flags)

elif sys.platform=="win32":
    PyInstaller.__main__.run(run_flags)
else:
    print("Unsupported.")
