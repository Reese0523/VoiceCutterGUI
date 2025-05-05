# hook-moviepy.py
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# 把所有 moviepy 的子模組都當 hiddenimports
hiddenimports = collect_submodules('moviepy')
# 把所有 moviepy 的原始碼 (.py) 與資源都當 datas
datas = collect_data_files('moviepy', include_py_files=True)
