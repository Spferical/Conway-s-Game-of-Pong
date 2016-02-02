from distutils.core import setup
import py2exe

target_file = 'main.py'

include_files = ["README.txt", "README-SDL.txt", "arial12x12.png", "LIBTCOD-LICENSE.txt"]

opts = { 'py2exe': {
	'ascii':True,
	'excludes':['_ssl', '_hashlib', 'tcl', 'tzdata'],
	'bundle_files':'1',
	'optimize':True,
	'compressed':True}}

setup(windows=[target_file],
      data_files=include_files,
      zipfile=None,
      options=opts)
