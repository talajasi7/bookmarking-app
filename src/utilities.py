import os

# A function for clearing the screen (OS-agnostic).
def clear_screen():
    clear = "cls" if os.name == "nt" else "clear"
    os.system(clear)
