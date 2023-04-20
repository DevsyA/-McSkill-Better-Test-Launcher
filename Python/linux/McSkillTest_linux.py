import os
import urllib.request
import zipfile
import subprocess
import tkinter as tk
from tkinter import ttk

jdkUrl = "https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jdk/jdk-8u361-linux-x64.tar.gz"
jarUrl = "https://github.com/DevsyA/McSkill-Better-Test-Launcher/blob/master/alt/McSkillTest.jar?raw=true"

tempFolder = "/tmp/McSkill"
jdkFileName = os.path.join(tempFolder, "jdk.tar.gz")
jdkFolder = os.path.join(tempFolder, "jdk")
jarFileName = os.path.join(tempFolder, "McSkillTest.jar")

def download_progress_hook(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    progress['value'] = percent
    progress.update()

def start_launcher():
    if not os.path.exists(tempFolder):
        os.mkdir(tempFolder)

    if not os.path.exists(jdkFolder):
        status_label.config(text="Downloading JDK...")
        urllib.request.urlretrieve(jdkUrl, jdkFileName, reporthook=download_progress_hook)
        status_label.config(text="Extracting JDK...")
        os.system(f"tar -xzf {jdkFileName} -C {jdkFolder}")
        status_label.config(text="Cleaning up...")
        os.remove(jdkFileName)

    if not os.path.exists(jarFileName):
        status_label.config(text="Downloading Launcher...")
        urllib.request.urlretrieve(jarUrl, jarFileName, reporthook=download_progress_hook)
        status_label.config(text="Download completed.")

    javaExe = os.path.join(jdkFolder, "jdk1.8.0_361", "bin", "java")
    jarArgs = "-jar \"" + jarFileName + "\""
    status_label.config(text="Starting Launcher...")
    subprocess.Popen('\"' + javaExe + '\" ' + jarArgs, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    root.destroy()

root = tk.Tk()
root.title("McSkill Test Launcher")
root.geometry("400x100")
root.configure(bg="#1c1c1c")

status_label = tk.Label(root, text="", font=("Arial", 14), fg="#fff", bg="#1c1c1c")
status_label.pack(pady=10)

style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", thickness=10, background="#1c1c1c", troughcolor="#2a2a2a", bordercolor="#2a2a2a", lightcolor="#2a2a2a", darkcolor="#2a2a2a")
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
progress.pack(pady=10)

start_launcher()

root.mainloop()