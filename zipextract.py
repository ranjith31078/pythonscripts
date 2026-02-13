import datetime
import zipfile
import sys
import os
import shutil
from datetime import datetime as dt

ZIP_FILE = 'c:\\ranjith\\Kindle Backup.zip'
EXTRACT_DIR = 'c:\\ranjith\\Kindle Considered2'

def extract_files(archive_name, modified_after):
    with zipfile.ZipFile(archive_name) as zf:
        for info in zf.infolist():
            if not info.filename.endswith('/'):
                modified = datetime.datetime(*info.date_time)
                if modified > modified_after:
                    zf.extract(info.filename, EXTRACT_DIR)

def compress_files(folder):
    os.chdir(folder)
    os.system("7z a -mhe+ -r -sdel -p ..\Kindle2.7z *")
    return ""

def clear_extract_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Usage: script <[date - dd-mmm-yyyy eg. 1-oct-2017]>")
    else:
        clear_extract_folder(EXTRACT_DIR)
        extract_files(ZIP_FILE, dt.strptime(sys.argv[1], '%d-%b-%Y'))
        compress_files(EXTRACT_DIR)