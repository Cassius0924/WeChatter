import signal
import subprocess
import sys
import threading

# 创建一个列表来存储所有的子进程
processes = []


def run_command(command, working_directory):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=working_directory)
    # 将子进程添加到列表中
    processes.append(process)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip().decode('utf-8'))
    return process.poll()


def signal_handler(signal, frame):
    # 当接收到Ctrl+C信号时，关闭所有的子进程
    for process in processes:
        process.terminate()
    sys.exit(0)


if __name__ == '__main__':
    # 设置信号处理器
    signal.signal(signal.SIGINT, signal_handler)

    backend_command = "uvicorn main:app --host 0.0.0.0 --reload"
    frontend_command = "npm start"

    backend_directory = "/myproject/WeChatter/configweb"
    frontend_directory = "/myproject/WeChatter/configweb"

    backend_thread = threading.Thread(target=run_command, args=(backend_command, backend_directory))
    frontend_thread = threading.Thread(target=run_command, args=(frontend_command, frontend_directory))

    backend_thread.start()
    print("backend started")
    frontend_thread.start()
    print("frontend started")

    backend_thread.join()
    frontend_thread.join()

# import subprocess
# import threading
#
#
# def run_command(command, working_directory):
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=working_directory)
#     while True:
#         output = process.stdout.readline()
#         if output == '' and process.poll() is not None:
#             break
#         if output:
#             print(output.strip().decode('utf-8'))
#     return process.poll()
#
#
# if __name__ == '__main__':
#     # backend_command = "uvicorn main:app --reload"
#     backend_command = "uvicorn main:app --host 0.0.0.0 --reload"
#     frontend_command = "npm start"
#
#     backend_directory = "/myproject/WeChatter/configweb"
#     frontend_directory = "/myproject/WeChatter/configweb"
#
#     backend_thread = threading.Thread(target=run_command, args=(backend_command, backend_directory))
#     frontend_thread = threading.Thread(target=run_command, args=(frontend_command, frontend_directory))
#
#     backend_thread.start()
#     print("backend started")
#     frontend_thread.start()
#     print("frontend started")
#
#     backend_thread.join()
#     frontend_thread.join()
#
