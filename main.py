import subprocess
import time

def run_backend():
    backend_process = subprocess.Popen(["python", "backend/main.py"])
    return backend_process

def run_frontend():
    frontend_process = subprocess.Popen(["streamlit", "run", "frontend/main.py"])
    return frontend_process

if __name__ == "__main__":
    backend_process = run_backend()
    time.sleep(5)  # Give the backend some time to start
    frontend_process = run_frontend()

    # Keep the script running
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        backend_process.terminate()
        frontend_process.terminate()
