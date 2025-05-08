# -*- coding: utf-8 -*-
import sys
import os
import threading
import logging

# 全局錯誤日誌設定
logging.basicConfig(
    filename='voice_cutter_gui.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(message)s'
)

try:
    from tkinter import Tk, Label, Button, filedialog
    import whisper
    import moviepy.editor as mp
except Exception:
    logging.error("初始化模組載入失敗", exc_info=True)
    sys.exit(1)


class App:
    def __init__(self, root):
        self.root = root
        root.title("Voice Cutter GUI")
        self.folder = None

        self.status = Label(root, text="請選擇要處理的資料夾")
        self.status.pack(padx=20, pady=10)

        btn = Button(root, text="選擇資料夾", command=self.choose_folder)
        btn.pack(pady=5)

    def choose_folder(self):
        self.folder = filedialog.askdirectory()
        if not self.folder:
            return
        self.status.config(text=f"已選擇：{self.folder}")
        threading.Thread(target=self.process).start()

    def process(self):
        try:
            model = whisper.load_model("base")
            for fn in os.listdir(self.folder):
                if fn.lower().endswith((".mp3", ".wav")):
                    path = os.path.join(self.folder, fn)
                    result = model.transcribe(path)
                    txt_path = os.path.splitext(path)[0] + ".txt"
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(result["text"])
            self.status.config(text="處理完成")
        except Exception:
            logging.error("處理過程發生錯誤", exc_info=True)
            self.status.config(text="處理失敗，請查看 voice_cutter_gui.log")


def main():
    try:
        root = Tk()
        App(root)
        root.mainloop()
    except Exception:
        logging.error("主程式未捕獲異常", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
