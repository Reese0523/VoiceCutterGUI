# ─── 在文件最顶部插入 ───────────────────────
import os, traceback, sys

LOG = os.path.join(os.path.dirname(__file__), "build_debug.log")
with open(LOG, "w", encoding="utf-8") as f:
    f.write(f"===== STARTING EXE at {__file__} =====\n")
    f.flush()

def log_exc_and_reraise(exc_type, exc_value, tb):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("----- EXCEPTION -----\n")
        traceback.print_exception(exc_type, exc_value, tb, file=f)
    # 让原本的控制台也能看到（attach 模式时）
    sys.__excepthook__(exc_type, exc_value, tb)

sys.excepthook = log_exc_and_reraise
# ─────────────────────────────────────────────
