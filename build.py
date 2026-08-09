"""
اسکریپت build برای تولید فایل اجرایی (exe) از ARPI.
روی هر سیستم‌عاملی که اجرا شود، خروجی مخصوص همان سیستم‌عامل
را می‌سازد (ویندوز -> .exe، لینوکس/مک -> باینری بدون پسوند).

اجرا:
    python build.py

خروجی در پوشه‌ی dist/ قرار می‌گیرد.
"""

import platform
import PyInstaller.__main__

# در ویندوز جداکننده‌ی --add-data ";" است، در لینوکس/مک ":"
SEP = ";" if platform.system() == "Windows" else ":"

PyInstaller.__main__.run([
    "run_local.py",
    "--name=ARPI",
    "--onefile",
    "--noconfirm",
    "--clean",
    f"--add-data=app{SEP}app",

    # ماژول‌های uvicorn که به‌صورت داینامیک import می‌شوند و
    # PyInstaller به‌طور خودکار تشخیصشان نمی‌دهد
    "--hidden-import=uvicorn.logging",
    "--hidden-import=uvicorn.loops",
    "--hidden-import=uvicorn.loops.auto",
    "--hidden-import=uvicorn.protocols",
    "--hidden-import=uvicorn.protocols.http",
    "--hidden-import=uvicorn.protocols.http.auto",
    "--hidden-import=uvicorn.protocols.websockets",
    "--hidden-import=uvicorn.protocols.websockets.auto",
    "--hidden-import=uvicorn.lifespan",
    "--hidden-import=uvicorn.lifespan.on",

    # وابستگی‌های دیگر پروژه که ممکن است نیاز به hidden-import داشته باشند
    "--hidden-import=pydantic",
    "--collect-all=yfinance",
])
