import streamlit
import sklearn
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