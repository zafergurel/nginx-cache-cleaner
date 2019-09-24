#!/usr/bin/env python3
'''
Creates index files for each nginx cache folder
'''
import os
import subprocess
import datetime
import sys

# Script parameters
cache_folder = "/cache"
index_folder = "/cache/_cacheindex"
default_cache_duration = 30
current_dir = os.getcwd()
index_creator_script = current_dir + "/bin/create_index.sh"
dir_empty_check_script = current_dir + "/bin/is_empty_dir.sh"

def create_indexes(op_mode="append"):
    '''Creates index files for each nginx cache folder.
    op_mode can be append or create
    In "append" mode, index file creation dates are checked and only 
    recently added cache files are added to index file.
    In "create" mode index files are re-created.
    Default mode is append.
    '''
    if op_mode != "append" and op_mode != "create":
        op_mode = "append"
    
    if not os.path.exists(index_folder):
        subprocess.Popen(["mkdir", "-p", index_folder]).wait()

    folders = get_folders(cache_folder)
    
    for f in folders:
        index_file = index_folder + "/" + f.replace("/", "_") + ".ind"
        delta = -1 * default_cache_duration

        if os.path.exists(index_file) and op_mode == "append":
            # get creation time
            ctime = datetime.datetime.fromtimestamp(os.stat(index_file).st_mtime)
            delta = -1 * round((datetime.datetime.now() - ctime).seconds / 3600 / 24, 2)
        
        if delta < 0:
            print("Cache operation: "+ op_mode + " -> " + f + " (" + str(delta) + " days)")
            subprocess.Popen([index_creator_script, op_mode, f, index_file, str(delta)]).wait()

def is_empty_dir(dir_path):
    '''Checks whether a directory is empty or not
    '''
    result = "0"
    with subprocess.Popen([dir_empty_check_script, dir_path],stdout=subprocess.PIPE) as proc:
        result = proc.stdout.read().decode().strip
    return result == "1"

def get_folders(base_folder):
    '''Returns all the folders (except index_folder) under 
    cache folder.
    '''
    folders = []
    for root, dirs, _ in os.walk(base_folder):
        for dir in dirs:
            full_path = root + "/" + dir
            if full_path != index_folder and not is_empty_dir(full_path):
                folders.append(full_path)
    return folders


if __name__ == "__main__":
    op_mode = sys.argv[1] if len(sys.argv) > 1 else "append"
    create_indexes(op_mode)
