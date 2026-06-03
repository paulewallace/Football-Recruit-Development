import subprocess
import sys


def main() -> None:
    cmd = [sys.executable, "-m", "streamlit", "run", "app/main.py"]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
