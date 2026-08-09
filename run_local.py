"""
ARPI Local Launcher
====================
این فایل برای اجرای برنامه به‌صورت یک فایل اجرایی مستقل (exe) استفاده می‌شود.
همان اپلیکیشن FastAPI را روی localhost بالا می‌آورد و مرورگر را
به‌صورت خودکار باز می‌کند.

نکته: کد سرویس (app/) دست‌نخورده باقی می‌ماند؛ این فقط یک لایه‌ی
اجرای محلی روی همان کد است. برای دپلوی سروری همچنان از Dockerfile
و render.yaml استفاده می‌شود.
"""

import sys
import os
import threading
import time
import webbrowser

import uvicorn

# وقتی با PyInstaller به exe تبدیل شده، مسیر فایل‌های بسته‌بندی‌شده
# در sys._MEIPASS قرار دارد. باید به sys.path اضافه شود تا import app.* کار کند.
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS  # type: ignore[attr-defined]
    sys.path.insert(0, base_path)

from app.main import app  # noqa: E402  (باید بعد از تنظیم sys.path باشد)

HOST = os.environ.get("ARPI_LOCAL_HOST", "127.0.0.1")
PORT = int(os.environ.get("ARPI_LOCAL_PORT", "8000"))


def open_browser():
    time.sleep(1.5)
    try:
        webbrowser.open(f"http://{HOST}:{PORT}")
    except Exception:
        pass


if __name__ == "__main__":
    print("========================================")
    print(f"ARPI در حال اجرا روی http://{HOST}:{PORT}")
    print("برای خروج، این پنجره را ببندید یا Ctrl+C بزنید.")
    print("========================================")

    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
