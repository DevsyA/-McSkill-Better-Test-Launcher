import os
import urllib.request
import zipfile
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

# Получаем путь к исполняемому файлу
if getattr(sys, 'frozen', False):
    current_path = os.path.dirname(sys.executable)
else:
    current_path = os.path.dirname(os.path.abspath(__file__))

jdkUrl = "https://cfdownload.adobe.com/pub/adobe/coldfusion/java/java8/java8u361/jdk/jdk-8u361-windows-x64.zip"
jarUrl = "https://github.com/DevsyA/McSkill-Better-Test-Launcher/blob/master/alt/McSkillTest.jar?raw=true"
tempFolder = os.environ["TEMP"] + "\\McSkillTest"
jdkFileName = os.path.join(tempFolder, "jdk.zip")
jdkFolder = os.path.join(tempFolder, "jdk")
jarFileName = os.path.join(tempFolder, "McSkillTest.jar")


def download_progress_hook(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    progress['value'] = percent
    progress.update()
    if percent == 100:
        status_label.config(text="Downloaded 100%")


def start_launcher():
    if not os.path.exists(tempFolder):
        os.mkdir(tempFolder)

    if not os.path.exists(jdkFolder):
        status_label.config(text="Downloading JDK...")
        urllib.request.urlretrieve(jdkUrl, jdkFileName, reporthook=download_progress_hook)
        status_label.config(text="Extracting JDK...")
        with zipfile.ZipFile(jdkFileName, 'r') as zip_ref:
            zip_ref.extractall(jdkFolder)
        status_label.config(text="Cleaning up...")
        os.remove(jdkFileName)

    if not os.path.exists(jarFileName):
        status_label.config(text="Downloading Launcher...")
        urllib.request.urlretrieve(jarUrl, jarFileName, reporthook=download_progress_hook)
        status_label.config(text="Download completed.")

    javaExe = os.path.join(jdkFolder, "jdk1.8.0_361", "bin", "java.exe")
    jarArgs = "-jar \"" + jarFileName + "\""
    status_label.config(text="Starting Launcher...")
    subprocess.Popen('\"' + javaExe + '\" ' + jarArgs, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    root.destroy()


root = tk.Tk()
root.title("McSkill Test Launcher")
root.geometry("400x150")

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

start_launcher()
root.mainloop()