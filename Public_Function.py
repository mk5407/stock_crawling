import os
import time
import platform

# check platform 
# Linux: Linux
# Mac: Darwin
# Windows: Windows

g_os = platform.system()
g_encoding=''
if g_os=='Windows': g_encoding='ANSI'
else : g_encoding='utf-8'


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


def ChangeDirectory() :
    now = time
    directory = 'C:\Python\Test\\'+ now.strftime('%Y-%m-%d')
    createDirectory(directory)
    os.chdir(directory)