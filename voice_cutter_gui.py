import os
import sys
import traceback

# 日誌檔路徑
base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
LOG = os.path.join(base_dir, 'run_debug.log')

def log(msg):
    try:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
    except:
        pass

log(f"==== START {'EXE' if getattr(sys, 'frozen', False) else 'SCRIPT'} ====")

# 捕獲未處理例外
sys.excepthook = lambda t, v, tb: (log('----- UNCAUGHT -----'), traceback.print_exception(t, v, tb, file=open(LOG, 'a', encoding='utf-8')))

log('Importing modules...')
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
from moviepy.editor import VideoFileClip, concatenate_videoclips
log('Imports done')

class VoiceCutterGUI:
    def __init__(self, root):
        root.title("VoiceCutter GUI")
        tk.Button(root, text="選資料夾", command=self.select_folder).pack(pady=10)
        tk.Button(root, text="開始處理", command=self.start).pack(pady=10)
        self.status = tk.Label(root, text="尚未選擇")
        self.status.pack(pady=10)
        self.folder = None
        log('Loading Whisper model...')
        self.model = whisper.load_model("base")
        log('Model loaded')

    def select_folder(self):
        f = filedialog.askdirectory()
        if f:
            self.folder = f
            self.status['text'] = f
            log(f"Folder selected: {f}")

    def start(self):
        if not self.folder:
            messagebox.showwarning("警告", "請選擇資料夾！")
            return
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        log(f"Processing {self.folder}")
        out = os.path.join(self.folder, 'output')
        os.makedirs(out, exist_ok=True)
        for fn in os.listdir(self.folder):
            if fn.lower().endswith('.mp4'):
                log(f"File: {fn}")
                self.status['text'] = fn
                clip = VideoFileClip(os.path.join(self.folder, fn))
                tmp = os.path.join(self.folder, '_tmp.wav')
                clip.audio.write_audiofile(tmp, logger=None)
                try:
                    r = self.model.transcribe(tmp)
                except Exception as e:
                    log(f"Transcribe error: {e}")
                    continue
                os.remove(tmp)
                segs = [clip.subclip(s['start'], s['end']) for s in r.get('segments', [])]
                if segs:
                    final = concatenate_videoclips(segs)
                    final.write_videofile(os.path.join(out, fn), codec="libx264", audio_codec="aac", logger=None)
        self.status['text'] = "完成"
        log('Done')
        messagebox.showinfo("完成", f"輸出: {out}")

if __name__ == '__main__':
    log('Launching GUI')
    tk.Tk().mainloop()
