import subprocess
import threading


def run_command(command, working_directory):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=working_directory)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()


if __name__ == '__main__':
    # backend_command = "uvicorn main:app --reload"
    backend_command = "uvicorn main:app --host 0.0.0.0 --reload"
    frontend_command = "npm start"
    # main_command = "python main.py"  # 添加这一行
    backend_directory = "WeChatter/configweb"
    frontend_directory = "configweb"
    # main_directory = "."  # 添加这一行，假设 main.py 在当前目录下

    backend_thread = threading.Thread(target=run_command, args=(backend_command, backend_directory))
    frontend_thread = threading.Thread(target=run_command, args=(frontend_command, frontend_directory))
    # main_thread = threading.Thread(target=run_command, args=(main_command, main_directory))  # 添加这一行

    backend_thread.start()
    print("backend started")
    frontend_thread.start()
    print("frontend started")
    # main_thread.start()  # 添加这一行
    # print("main started")  # 添加这一行

    backend_thread.join()
    frontend_thread.join()
    # main_thread.join()  # 添加这一行
