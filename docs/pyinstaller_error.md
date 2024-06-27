pyinstaller에서 일부 라이브러리 임포트 문제가 생기는 경우가 있음

ex) sklearn의 경우
1. 경로에 파일 생성
```
.venv/Lib/site-packages/pyinstaller/hooks
touch hook-sklearn.py
```
2. hook-sklearn.py
```
from PyInstaller.utils.hooks import collect_submodules
hiddenimports = collect_submodules('sklearn')
```


[참고자료](https://chez-sarah.tistory.com/8)