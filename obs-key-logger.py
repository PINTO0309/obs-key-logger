import time
from pynput import keyboard
from obswebsocket import obsws, requests
from datetime import datetime
import sys  # プログラム終了用
import threading  # メインループの制御用

# OBS WebSocket設定
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = ""  # 必要ならパスワードを設定

# フレーム周期
FRAME_INTERVAL = 1 / 30  # 30 FPSに対応

# ログファイル関連
current_log_file = None
key_log = []
running = True  # プログラムの動作状態を管理


def generate_log_filename():
    """現在時刻を元にログファイル名を生成"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
    return f"{timestamp}_key_log.txt"


def write_to_logfile():
    """キー入力をログファイルに書き込む"""
    global current_log_file
    if current_log_file is None:
        return  # ログファイルが未設定の場合は何もしない
    with open(current_log_file, "a") as file:
        for timestamp, key in key_log:
            file.write(f"{timestamp}: {key}\n")
    key_log.clear()


def on_press(key):
    """キーが押されたときに記録"""
    global running  # ESCキー押下時にプログラムを終了するため
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    try:
        if key == keyboard.Key.esc:
            print("ESC pressed. Exiting program.")
            running = False  # メインループ終了フラグを設定
            return False  # リスナーを停止
        else:
            key_log.append([timestamp, f"Key pressed: {key.char}"])
            print(f"Key pressed: {key.char}")
    except AttributeError:
        key_log.append([timestamp, f"Special key pressed: {key}"])
        print(f"Special key pressed: {key}")


def main_loop():
    global current_log_file, running
    ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
    ws.connect()
    print("Connected to OBS WebSocket")

    recording_active = False  # 現在の録画状態を保持
    try:
        while running:
            # 録画状態を取得
            recording_status = ws.call(requests.GetRecordStatus())
            is_recording = recording_status.datain.get("outputActive", False)

            if is_recording and not recording_active:
                # 録画が開始された場合、新しいログファイルを生成
                current_log_file = generate_log_filename()
                print(f"Recording started. New log file: {current_log_file}")
            elif not is_recording and recording_active:
                # 録画が停止した場合、現在のログファイルを閉じる（必要に応じて通知）
                print(f"Recording stopped. Log file: {current_log_file}")

            # 録画中の場合のみログを更新
            if is_recording:
                write_to_logfile()

            # 現在の録画状態を更新
            recording_active = is_recording

            # フレーム周期に合わせて待機
            time.sleep(FRAME_INTERVAL)
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        ws.disconnect()


if __name__ == "__main__":
    # キーボードリスナーを別スレッドで起動
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # メインループを実行
    main_loop()

    # プログラム終了時にリスナーを停止
    listener.join()
    print("Program terminated.")
