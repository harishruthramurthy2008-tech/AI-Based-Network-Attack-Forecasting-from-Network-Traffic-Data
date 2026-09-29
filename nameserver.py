import os
import shutil
import signal
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"


def run_command(command, cwd, env=None, name="process"):
    print(f"Starting {name}: {command}")
    return subprocess.Popen(
        command,
        cwd=str(cwd),
        env=env,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )


def build_env(extra=None):
    env = os.environ.copy()
    if extra:
        env.update(extra)
    return env


def main():
    if not BACKEND_DIR.exists():
        raise FileNotFoundError(f"Backend folder not found: {BACKEND_DIR}")
    if not FRONTEND_DIR.exists():
        raise FileNotFoundError(f"Frontend folder not found: {FRONTEND_DIR}")

    python_exe = sys.executable
    npm_exe = (
        shutil.which("npm")
        or shutil.which("npm.cmd")
        or shutil.which("C:/Program Files/nodejs/npm.cmd")
        or shutil.which("C:/Program Files/nodejs/npm")
    )
    if not npm_exe:
        raise FileNotFoundError(
            "Node.js and npm are not installed or not on PATH. Install Node.js LTS from https://nodejs.org/, restart your terminal, and then run this script again."
        )

    backend_command = f'"{python_exe}" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload'
    frontend_command = f'"{npm_exe}" run dev -- --host 0.0.0.0 --port 5173'

    backend_process = run_command(backend_command, BACKEND_DIR, name="backend")
    time.sleep(2)

    frontend_process = run_command(frontend_command, FRONTEND_DIR, name="frontend")

    url = "http://localhost:5173"
    print("\nWhetherGPT is starting...")
    print(f"Frontend: {url}")
    print(f"Backend: http://localhost:8000/docs")
    time.sleep(3)
    webbrowser.open(url)

    def shutdown(signum, frame):
        print("\nStopping WhetherGPT services...")
        for proc in (frontend_process, backend_process):
            if proc.poll() is None:
                proc.terminate()
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
            if backend_process.poll() is not None and frontend_process.poll() is not None:
                break
    except KeyboardInterrupt:
        print("Stopped.")
        for proc in (frontend_process, backend_process):
            if proc.poll() is None:
                proc.terminate()


if __name__ == "__main__":
    main()
