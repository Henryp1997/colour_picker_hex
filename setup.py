import cx_Freeze
import os

executables = [
    cx_Freeze.Executable(
        f"{os.path.dirname(os.path.realpath(__file__))}/app.py",
        base="Win32GUI",
        target_name="colourPicker.exe",
        icon=f"{os.path.dirname(os.path.realpath(__file__))}/icon.ico"
    )
]

cx_Freeze.setup(
    name="pyTerminal",
    executables=executables,
    options={
        "build_exe": {
            "includes": ["pynput", "pynput.keyboard._win32", "pynput.mouse._win32"]
        }
    }
)