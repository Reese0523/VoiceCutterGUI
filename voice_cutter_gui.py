import os
import sys
import traceback

# 設定日誌檔路徑（one-dir 模式使用 sys.executable 所在目錄）
base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
LOG = os.path.join(base_dir, 'build_debug.log')

def log(msg):
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except Exception:
        pass

# 啟動日誌
log(f"==== STARTING: {'EXE' if getattr(sys, 'frozen', False) else 'SCRIPT'} ====")

# 全域例外勾掛，將未捕捉例外記錄到日誌並顯示
def excepthook(exc_type, exc_value, exc_tb):
    log('----- UNCAUGHT EXCEPTION -----')
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
    except Exception:
        pass
    sys.__excepthook__(exc_type, exc_value, exc_tb)
sys.excepthook = excepthook

log('Imports now...')
# 正式引用套件
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
from moviepy.editor import VideoFileClip, concatenate_videoclips

log('Initializing GUI...')
class VoiceCutterGUI:
    def __init__(self, root):
        self.root = root
        root.title("VoiceCutter GUI")
        tk.Button(root, text="選資料夾", command=self.select_folder).pack(pady=10)
        tk.Button(root, text="開始處理", command=self.start_processing).pack(pady=10)
        self.status = tk.Label(root, text="尚未選擇資料夾")
        self.status.pack(pady=10)
        self.folder = None
        log('Loading Whisper model...')
        self.model = whisper.load_model("base")
        log('Model loaded')

    def select_folder(self):
        self.folder = filedialog.askdirectory(title="選擇資料夾")
        if self.folder:
            self.status.config(text=f"已選：{self.folder}")
            log(f"Folder: {self.folder}")

    def start_processing(self):
        if not self.folder:
            messagebox.showwarning("警告", "請先選擇資料夾！")
            return
        threading.Thread(target=self.process_folder, daemon=True).start()

    def process_folder(self):
        log(f"Processing: {self.folder}")
        out_dir = os.path.join(self.folder, "output")
        os.makedirs(out_dir, exist_ok=True)
        files = [f for f in os.listdir(self.folder) if f.lower().endswith(".mp4")]
        for f in files:
            log(f"File: {f}")
            self.status.config(text=f"處理：{f}")
            clip = VideoFileClip(os.path.join(self.folder, f))
            audio = clip.audio
            tmp = os.path.join(self.folder, "__tmp.wav")
            audio.write_audiofile(tmp, logger=None)
            try:
                res = self.model.transcribe(tmp)
            except Exception as e:
                log(f"Transcribe error: {e}")
                continue
            os.remove(tmp)
            segs = [clip.subclip(s['start'], s['end']) for s in res.get('segments', [])]
            if segs:
                final = concatenate_videoclips(segs)
                final.write_videofile(
                    os.path.join(out_dir, f), codec="libx264", audio_codec="aac", logger=None
                )
        self.status.config(text="完成！")
        log('All done')
        messagebox.showinfo("完成", f"輸出於：{out_dir}")

if __name__ == '__main__':
    log('Entering mainloop')
    root = tk.Tk()
    app = VoiceCutterGUI(root)
    root.mainloop()
