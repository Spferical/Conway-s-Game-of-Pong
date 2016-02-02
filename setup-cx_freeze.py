import sys
from cx_Freeze import setup, Executable
from config import VERSION

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": [],
                     "excludes": [],
                     "compressed": True,
                     "include_files": [("README.txt", "README.txt"),
                                       ("README-SDL.txt", "README-SDL.txt"),
                                       ("arial12x12.png", "arial12x12.png"),
		                       ("LIBTCOD-LICENSE.txt",
					"LIBTCOD_LICENSE.txt")],
                     }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
    windows_libs = [("SDL.dll", "SDL.dll"),
                    ("libtcod-gui-mingw.dll", "libtcod-gui-mingw.dll"),
                    ("libtcod-mingw.dll", "libtcod-mingw.dll")]

    build_exe_options["include_files"].extend(windows_libs)
elif sys.platform.startswith("linux"):
    linux_libs = [("libSDL.so", "libSDL.so"),
                  ("libtcod.so", "libtcod.so")]
    build_exe_options["include_files"].extend(linux_libs)
else: print "add options for " + sys.platform; sys.exit()


setup(name="Conway's Game of Pong",
      version=VERSION,
      description="A mashup of Pong and Conway's Game of Life",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
