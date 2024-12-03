# obs-key-logger
Linking OBS and Python code, the values entered on the keyboard are simply recorded in a text log only when the OBS side is recording. Connecting OBS and Python via WebSocket to hook keyboard input and logging input values as soon as recording starts.

## 1. Environment setting

- OBS　30.2.3

  https://obsproject.com/ja/download

- Additional Packages

  ```bash
  # Option
  wget https://github.com/univrsal/input-overlay/releases/download/5.0.6/input-overlay-5.0.6-x86_64-linux-gnu.deb
  sudo dpkg -i input-overlay-5.0.6-x86_64-linux-gnu.deb
  
  # Required
  wget https://github.com/obsproject/obs-websocket/releases/download/4.9.1-compat/obs-websocket-4.9.1-compat-Ubuntu64.deb
  sudo dpkg -i obs-websocket-4.9.1-compat-Ubuntu64.deb
  pip install pynput==1.7.7 obs-websocket-py==1.0
  ```
