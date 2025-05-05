import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import whisper

class VoiceCutterGUI:
    def __init__(self, root):
        self.root = root
        root.title("VoiceCutter 批次無人聲剪輯")
        tk.Button(root, text="選擇資料夾", command=self.select_folder).pack(padx=20, pady=10)
        tk.Button(root, text="開始處理", command=self.start_processing).pack(padx=20, pady=10)
        self.status = tk.Label(root, text="尚未選擇資料夾")
        self.status.pack(padx=20, pady=10)
        self.folder = None
        self.model = whisper.load_model("base")  # 可改成 small/medium/large
    
    def select_folder(self):
        self.folder = filedialog.askdirectory(title="請選擇影片資料夾")
        if self.folder:
            self.status.config(text=f"已選擇：{self.folder}")
    
    def start_processing(self):
        if not self.folder:
            messagebox.showwarning("警告", "請先選擇資料夾！")
            return
        threading.Thread(target=self.process_folder, daemon=True).start()
    
    def process_folder(self):
        out_dir = os.path.join(self.folder, "output")
        os.makedirs(out_dir, exist_ok=True)
        files = [f for f in os.listdir(self.folder) if f.lower().endswith(".mp4")]
        for fname in files:
            self.status.config(text=f"處理：{fname}")
            in_path = os.path.join(self.folder, fname)
            clip = VideoFileClip(in_path)
            audio = clip.audio
            # 臨時存檔，讓 Whisper 辨識
            tmp_wav = os.path.join(self.folder, "__tmp.wav")
            audio.write_audiofile(tmp_wav, logger=None)
            result = self.model.transcribe(tmp_wav, word_timestamps=False)
            os.remove(tmp_wav)
            # 將有聲段落合併
            segments = []
            for seg in result["segments"]:
                start, end = seg["start"], seg["end"]
                segments.append(clip.subclip(start, end))
            if segments:
                final = concatenate_videoclips(segments)
                out_path = os.path.join(out_dir, fname)
                final.write_videofile(out_path, codec="libx264", audio_codec="aac", threads=4, logger=None)
        self.status.config(text="全部完成！")
        messagebox.showinfo("完成", f"所有影片已輸出到：{out_dir}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceCutterGUI(root)
    root.mainloop()
