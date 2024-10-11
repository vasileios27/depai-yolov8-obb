import errno
import logging
import os
import shutil


def clean_temp_directory(folder_name: str):
    try:
        shutil.rmtree(folder_name)
    except OSError as e:
        logging.error("Error: %s - %s.", e.filename, e.strerror)


def create_directory(folder_name: str):
    if not os.path.exists(folder_name):
        try:
            os.mkdir(folder_name)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
