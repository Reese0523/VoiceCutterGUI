# wrapper.py
import logging
import traceback
import sys

# 日志写到文件，DEBUG 级别记录所有信息
logging.basicConfig(
    filename='voice_cutter_gui.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def main():
    # —— 导入并调用原业务脚本 —— 
    # 假设原脚本中有个入口函数 run()
    from voice_cutter_gui import run
    logging.info("Starting voice_cutter_gui")
    run()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        # 捕获所有未处理异常，写 log 并在控制台和日志文件中留下堆栈
        logging.exception("Unhandled exception in voice_cutter_gui")
        print("程序发生未捕获异常，详细信息请参见 voice_cutter_gui.log：")
        print(traceback.format_exc())
        input("按回车键退出…")
        sys.exit(1)
