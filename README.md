# screen

# exe 실행파일 만들기
1. .venv 가상환경 만들기
```
python3 -m venv .venv // 가상환경 생성
.\.venv\Scripts\activate // 가상환경 실행 window
# source .venv/bin/activate // mac & linux
pip install -r requirements.txt // 라이브러리 설치
```


2. .hook/hook-streamlit.py 파일 생성
```python
from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata("streamlit")
```
3. app.py
```python
import streamlit as st

x = st.slider("Select a value")
st.write(x, "squared is", x * x)
```
4. run.py
```python
import streamlit

import streamlit.web.cli as stcli
import os, sys


def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    run_path = os.path.join('src', '메인페이지.py')
    sys.argv = [
        "streamlit",
        "run",
        resolve_path(run_path),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
```
5. pyinstaller 명령어 1
```
pyinstaller --onefile --additional-hooks-dir=./hooks run.py --clean
```
6. run.spec 수정
```python
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [(".venv/Lib/site-packages/streamlit/runtime", "./streamlit/runtime")]
datas += collect_data_files("streamlit")
datas += copy_metadata("streamlit")

block_cipher = None

a = Analysis(
    ["run.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='VR DTx by WHATs LAB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```
7. pyinstaller 명령어 2
```
pyinstaller run.spec --clean
```
8. dist 폴더에서 exe파일 부모 폴더로 옮기기
```
+----dist
+--run.exe
```

[참고자료](https://ploomber.io/blog/streamlit_exe/)