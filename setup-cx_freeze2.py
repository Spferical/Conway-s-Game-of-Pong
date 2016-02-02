from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

executables = [
    Executable('main.py', 'Win32GUI', targetName = 'ConwayPong')
]

setup(name="Conway's Game of Pong",
      version = '1.0',
      description = "A mashup of Conway's Game of Life and Pong.",
      options = dict(build_exe = buildOptions),
      executables = executables)
