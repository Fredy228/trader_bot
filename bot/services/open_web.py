import time
import webbrowser

from config import IP_PY_SERVER


def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://{IP_PY_SERVER}:8080")
