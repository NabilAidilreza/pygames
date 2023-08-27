from cx_Freeze import setup, Executable

base = None    

executables = [Executable("PySpaceShooter .py", base=base)]

packages = ["idna","pygame","os","random","math"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Game",
    options = options,
    version = "1",
    description = "Game",
    executables = executables
)
