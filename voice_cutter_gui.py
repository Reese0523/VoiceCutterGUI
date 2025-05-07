import os
import sys
import traceback

# 設定日誌檔路徑（單檔模式下使用可執行檔路徑）
base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
LOG = os.path.join(base_dir, 'build_debug.log')

def log(msg):
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except Exception:
        pass

# 啟動日誌
log(f"==== STARTING EXE: {os.path.basename(sys.executable if getattr(sys, 'frozen', False) else __file__)} ====")

# 全域例外勾掛，將未捕捉例外記錄到日誌
def excepthook(exc_type, exc_value, exc_tb):
    log('----- UNCAUGHT EXCEPTION -----')
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
    except Exception:
        pass
    # 仍然在控制台顯示
    sys.__excepthook__(exc_type, exc_value, exc_tb)

sys.excepthook = excepthook

# 正式引用套件與邏輯
log('Imports done, loading modules...')
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
from moviepy.editor import VideoFileClip, concatenate_videoclips

log('Initializing GUI...')

class VoiceCutterGUI:
    def __init__(self, root):
        self.root = root
        root.title("VoiceCutter 批次無人聲剪輯")
        tk.Button(root, text="選擇資料夾", command=self.select_folder).pack(padx=20, pady=10)
        tk.Button(root, text="開始處理", command=self.start_processing).pack(padx=20, pady=10)
        self.status = tk.Label(root, text="尚未選擇資料夾")
        self.status.pack(padx=20, pady=10)
        self.folder = None
        log('Loading Whisper model...')
        self.model = whisper.load_model("base")  # small/medium/large
        log('Whisper model loaded')

    def select_folder(self):
        self.folder = filedialog.askdirectory(title="請選擇影片資料夾")
        if self.folder:
            self.status.config(text=f"已選擇：{self.folder}")
            log(f"Folder selected: {self.folder}")

    def start_processing(self):
        if not self.folder:
            messagebox.showwarning("警告", "請先選擇資料夾！")
            return
        threading.Thread(target=self.process_folder, daemon=True).start()

    def process_folder(self):
        log(f"Processing folder: {self.folder}")
        out_dir = os.path.join(self.folder, "output")
        os.makedirs(out_dir, exist_ok=True)
        files = [f for f in os.listdir(self.folder) if f.lower().endswith(".mp4")]
        for fname in files:
            log(f"Processing file: {fname}")
            self.status.config(text=f"處理：{fname}")
            in_path = os.path.join(self.folder, fname)
            clip = VideoFileClip(in_path)
            audio = clip.audio
            tmp_wav = os.path.join(self.folder, "__tmp.wav")
            audio.write_audiofile(tmp_wav, logger=None)
            result = self.model.transcribe(tmp_wav, word_timestamps=False)
            os.remove(tmp_wav)
            segments = []
            for seg in result["segments"]:
                start, end = seg["start"], seg["end"]
                segments.append(clip.subclip(start, end))
            if segments:
                final = concatenate_videoclips(segments)
                out_path = os.path.join(out_dir, fname)
                final.write_videofile(out_path, codec="libx264", audio_codec="aac", threads=4, logger=None)
        self.status.config(text="全部完成！")
        log('All files processed, job done')
        messagebox.showinfo("完成", f"所有影片已輸出到：{out_dir}")

if __name__ == "__main__":
    log('Launching mainloop')
    root = tk.Tk()
    app = VoiceCutterGUI(root)
    root.mainloop()
