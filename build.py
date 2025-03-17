import subprocess
import os
import shutil

APP_NAME = "tiresias"


def build():
    subprocess.run(
        [
            "pyinstaller",
            "--onefile",
            "--noconfirm",
            "--windowed",
            "--name",
            APP_NAME,
            "--distpath",
            "dist",
            "--workpath",
            "build",
            "--specpath",
            "spec",
            "./tiresias/main.py",
        ],
        check=True,
    )

    os.makedirs(f"AppDir/usr/bin", exist_ok=True)
    os.makedirs(f"AppDir/usr/share/icons", exist_ok=True)

    shutil.copy(f"dist/{APP_NAME}", f"AppDir/usr/bin/{APP_NAME}")

    with open("AppDir/AppRun", "w") as f:
        f.write(f"#!/bin/bash\nexec $APPDIR/usr/bin/{APP_NAME}")
    os.chmod("AppDir/AppRun", 0o755)

    with open(f"AppDir/{APP_NAME}.desktop", "w") as f:
        f.write(
            f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Exec={APP_NAME}
Icon={APP_NAME}
Categories=Utility;"""
        )

    # Adicionar o ícone (opcional)
    icon_path = f"./tiresias/icon.png"
    if os.path.exists(icon_path):
        shutil.copy(icon_path, f"AppDir/usr/share/icons/{APP_NAME}.png")

    if not os.path.exists("appimagetool-x86_64.AppImage"):
        subprocess.run(
            [
                "wget",
                "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage",
            ],
            check=True,
        )
        os.chmod("appimagetool-x86_64.AppImage", 0o755)
    else:
        os.chmod("appimagetool-x86_64.AppImage", 0o755)

    subprocess.run(
        ["./appimagetool-x86_64.AppImage", "AppDir", f"{APP_NAME}-x86_64.AppImage"],
        check=True,
    )


if __name__ == "__main__":
    build()
