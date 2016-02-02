# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['/home/matthew/Dropbox/ConwayPong'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'main'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
