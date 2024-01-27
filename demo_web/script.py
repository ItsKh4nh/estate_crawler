import subprocess
import os


def run_script(script_name, folder_name):
    script_path = os.path.join(folder_name, script_name)
    subprocess.run(["python", script_path])


if __name__ == "__main__":
    folders_and_scripts = [
        ("khanh", "convert-khanh.py"),
        ("quan", "convert-quan.py"),
        ("VietAnh", "convert-vanh.py"),
        ("LaDat", "convert-la.py"),
    ]

    for folder, script in folders_and_scripts:
        run_script(script, folder)
