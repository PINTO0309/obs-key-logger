# obs-key-logger
Linking OBS and Python code, the values entered on the keyboard are simply recorded in a text log only when the OBS side is recording. Connecting OBS and Python via WebSocket to hook keyboard input and logging input values as soon as recording starts.

## 0. Environment

1. OBS 30.2.3
2. input-overlay 5.0.6 (optional)
3. pynput==1.7.7
4. obs-websocket-py==1.0
5. pyinstaller==6.11.1

## 1. Environment setting

- OBS

  https://obsproject.com/ja/download

- Additional Packages

  ```bash
  # Optional
  wget https://github.com/univrsal/input-overlay/releases/download/5.0.6/input-overlay-5.0.6-x86_64-linux-gnu.deb
  sudo dpkg -i input-overlay-5.0.6-x86_64-linux-gnu.deb

  # Required
  wget https://github.com/obsproject/obs-websocket/releases/download/4.9.1-compat/obs-websocket-4.9.1-compat-Ubuntu64.deb
  sudo dpkg -i obs-websocket-4.9.1-compat-Ubuntu64.deb
  pip install pynput==1.7.7 obs-websocket-py==1.0 pyinstaller==6.11.1
  ```

## 2. Result

https://github.com/user-attachments/assets/624f8dcf-a362-4de1-a6e7-778c104179dc
