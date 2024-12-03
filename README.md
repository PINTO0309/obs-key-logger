# obs-key-logger
Linking OBS and Python code, the values entered on the keyboard are simply recorded in a text log only when the OBS side is recording. Connecting OBS and Python via WebSocket to hook keyboard input and logging input values as soon as recording starts.

## 0. Environment

1. OBS 30.2.3
2. input-overlay 5.0.6 (optional)
3. pynput==1.7.7
4. obs-websocket-py==1.0
5. pyinstaller==6.11.1
6. [dotnet 8.0.404](https://learn.microsoft.com/ja-jp/dotnet/core/install/windows#install-with-visual-studio-code) (optional)

## 1. Environment setting

- OBS

  https://obsproject.com/ja/download

- Additional Packages

  ```bash
  # Optional
  # Windows
  https://github.com/univrsal/input-overlay/releases/download/5.0.6/input-overlay-5.0.6-windows-x64-Installer.exe
  # Ubuntu
  wget https://github.com/univrsal/input-overlay/releases/download/5.0.6/input-overlay-5.0.6-x86_64-linux-gnu.deb
  sudo dpkg -i input-overlay-5.0.6-x86_64-linux-gnu.deb

  # Required
  # Windows / Ubuntu
  pip install pynput==1.7.7 obs-websocket-py==1.0 pyinstaller==6.11.1
  or
  pip install pynput==1.7.7 obs-websocket-py==1.0 PyInstaller
  # Windows
  https://github.com/obsproject/obs-websocket/releases/download/4.9.1-compat/obs-websocket-4.9.1-compat-Qt6-Windows-Installer.exe
  # Ubuntu
  wget https://github.com/obsproject/obs-websocket/releases/download/4.9.1-compat/obs-websocket-4.9.1-compat-Ubuntu64.deb
  sudo dpkg -i obs-websocket-4.9.1-compat-Ubuntu64.deb
  ```

- OBS settings

  ![スクリーンショット 2024-12-03 111933](https://github.com/user-attachments/assets/42a56116-46f7-479b-94ac-2830f3a3dc0e)

  ![スクリーンショット 2024-12-03 111811](https://github.com/user-attachments/assets/a514478e-63cf-401e-86b5-02b345c15863)

## 2. Result

https://github.com/user-attachments/assets/624f8dcf-a362-4de1-a6e7-778c104179dc

## 3. Executable file

```bash
# Windows / Ubuntu
pyinstaller --onefile obs-key-logger.py
# Ubuntu
chmod +x dist/obs-key-logger
```
