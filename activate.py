import subprocess
import threading
# import logging
#
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def run_command(command, working_directory):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=working_directory)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip().decode('utf-8'))
            # logging.info(output.strip().decode('utf-8'))
    return process.poll()


if __name__ == '__main__':
    # backend_command = "uvicorn main:app --reload"
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

