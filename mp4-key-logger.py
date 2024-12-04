import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
import time
import threading
import os
from pydub import AudioSegment
import simpleaudio as sa

class MP4PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 Player")
        self.is_playing = False
        self.log_file_path = ""
        self.video_thread = None
        self.audio_thread = None
        self.audio_object = None
        self.audio_start_time = 0  # 音声再生開始時刻
        self.current_key = ""  # 表示するキー
        self.key_timestamp = 0  # キーが押された時間（秒）
        self.selected_file = ""  # 選択されたファイルパス
        self.default_video_path = os.path.expanduser("~/Videos")  # 動画選択のデフォルトパス
        self.default_log_path = os.path.expanduser("~/Documents")  # ログ保存先のデフォルトパス
        self.start_time = 0  # 動画再生開始時刻
        self.frame_count = 0  # フレーム数カウンタ
        self.total_duration = 0  # 動画の全体時間（秒）
        self.current_time = 0  # 現在の再生時間（秒）

        # UI設定
        self.open_button = tk.Button(root, text="MP4を開く", command=self.open_file)
        self.open_button.pack(pady=10)

        self.file_label = tk.Label(root, text="選択されたファイル: なし", wraplength=400, justify="left")
        self.file_label.pack(pady=10)

        self.play_button = tk.Button(root, text="再生開始", command=self.start_playback, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.progress_label = tk.Label(root, text="再生時間: 00:00:00 / 00:00:00")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.reset_button = tk.Button(root, text="初期化", command=self.reset_app)
        self.reset_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="終了", command=self.exit_app)
        self.exit_button.pack(pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.default_video_path,
            filetypes=[("MP4 files", "*.mp4")]
        )
        if file_path:
            self.selected_file = file_path
            # ラベルにファイルパスを表示
            self.file_label.config(text=f"選択されたファイル: {file_path}")
            self.play_button.config(state=tk.NORMAL)  # 再生ボタンを有効化

    def start_playback(self):
        if self.selected_file:
            folder_path = filedialog.askdirectory(initialdir=self.default_log_path, title="ログフォルダを選択")
            if folder_path:
                # 前回の再生を停止し、リソースを解放
                self.stop_playback()

                # ログファイル生成
                video_filename = os.path.basename(self.selected_file)
                base_filename = os.path.splitext(video_filename)[0]  # 拡張子を除去
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                self.log_file_path = os.path.join(folder_path, f"{base_filename}_{timestamp}.log")
                with open(self.log_file_path, "w") as log_file:
                    log_file.write("フレーム数,経過時間,キー入力\n")

                # 動画の全体時間を取得
                cap = cv2.VideoCapture(self.selected_file)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                cap.release()
                if frame_count > 0 and fps > 0:
                    self.total_duration = frame_count / fps  # 動画の総再生時間（秒）

                # プログレスバー初期化
                self.progress_bar["value"] = 0
                self.progress_bar["maximum"] = self.total_duration

                # 再生開始状態をリセット
                self.is_playing = True
                self.audio_start_time = time.time()
                self.frame_count = 0

                # スレッド作成
                self.video_thread = threading.Thread(target=self.play_video, args=(self.selected_file,))
                self.audio_thread = threading.Thread(target=self.play_audio)

                # スレッド開始
                self.audio_thread.start()
                self.video_thread.start()

    def play_audio(self):
        """音声を再生"""
        audio = AudioSegment.from_file(self.selected_file)
        self.audio_object = sa.play_buffer(
            audio.raw_data,
            num_channels=audio.channels,
            bytes_per_sample=audio.sample_width,
            sample_rate=audio.frame_rate
        )
        self.audio_object.wait_done()  # 再生完了を待つ

    def play_video(self, file_path):
        cap = cv2.VideoCapture(file_path)
        fps = cap.get(cv2.CAP_PROP_FPS)  # フレームレートを取得
        if fps > 0:
            frame_time = 1 / fps  # フレーム間の時間（秒単位）
        else:
            frame_time = 1 / 25  # デフォルト値（25fps相当）

        while self.is_playing and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 現在の音声再生時間を基準に映像を調整
            elapsed_time = time.time() - self.audio_start_time

            # フレームの再生タイミングを調整
            if elapsed_time < self.frame_count * frame_time:
                time.sleep((self.frame_count * frame_time) - elapsed_time)

            # フレーム数をカウント
            self.frame_count += 1
            self.current_time = self.frame_count * frame_time
            self.update_progress()

            # フレームに現在のキーを表示（2秒以内の場合）
            if self.current_key and time.time() - self.key_timestamp < 2:
                font = cv2.FONT_HERSHEY_SIMPLEX
                position = (10, 50)  # 左上
                font_scale = 2
                color = (0, 0, 255)  # 赤 (BGR)
                thickness = 3
                cv2.putText(frame, self.current_key, position, font, font_scale, color, thickness, cv2.LINE_AA)
            else:
                self.current_key = ""  # 2秒経過したら表示を消去

            cv2.imshow("MP4 Player", frame)

            # フレーム間の待機とキー入力検出
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Escキーで停止可能
                self.is_playing = False
                break
            elif key != 255:  # 何らかのキーが押された場合
                self.handle_key_event(key)

        # 再生終了後の処理
        self.is_playing = False
        cap.release()
        cv2.destroyAllWindows()
        self.video_thread = None  # スレッドをリセット

    def stop_playback(self):
        """映像と音声の再生を停止"""
        self.is_playing = False
        if self.audio_object:
            self.audio_object.stop()
            self.audio_object = None  # オブジェクトをリセット
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join()  # 自スレッドでない場合のみjoin
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()
        # OpenCVウィンドウを確実に閉じる
        cv2.destroyAllWindows()

    def update_progress(self):
        """プログレスバーと時間ラベルを更新"""
        elapsed_hms = time.strftime("%H:%M:%S", time.gmtime(self.current_time))
        total_hms = time.strftime("%H:%M:%S", time.gmtime(self.total_duration))
        self.progress_label.config(text=f"再生時間: {elapsed_hms} / {total_hms}")
        self.progress_bar["value"] = self.current_time

    def handle_key_event(self, key):
        # OpenCVのキーイベントを文字に変換
        key_char = chr(key) if 32 <= key <= 126 else f"[{key}]"
        self.current_key = key_char  # 表示するキーを更新
        self.key_timestamp = time.time()  # キーが押された時刻を記録

        if self.log_file_path:
            # ログに記録
            elapsed_time = time.time() - self.audio_start_time
            elapsed_hms = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            elapsed_ms = int((elapsed_time - int(elapsed_time)) * 1000)
            formatted_time = f"{elapsed_hms}.{elapsed_ms:03d}"
            with open(self.log_file_path, "a") as log_file:
                log_file.write(f"{self.frame_count:06d},{formatted_time},{key_char}\n")

    def reset_app(self):
        """初期化ボタンの動作"""
        self.stop_playback()
        self.selected_file = ""
        self.file_label.config(text="選択されたファイル: なし")
        self.play_button.config(state=tk.DISABLED)
        self.log_file_path = ""
        self.current_key = ""
        self.progress_bar["value"] = 0
        self.progress_label.config(text="再生時間: 00:00:00 / 00:00:00")

    def exit_app(self):
        self.stop_playback()
        self.root.destroy()

# アプリ起動
if __name__ == "__main__":
    root = tk.Tk()
    app = MP4PlayerApp(root)
    root.mainloop()
