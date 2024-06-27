import pandas as pd
import os

def lastest_file():
    input_path = os.path.join(".", "data", "input")

    dir = sorted(os.listdir(input_path))
    if len(dir) == 0:
        print('ERROR: NO files exist in input dir')
        return False
    
    lastest_timestr = sorted([file.split('_')[-1].split('.')[0] for file in dir])[-1]
    for file_name in dir:
        if lastest_timestr in file_name:
            return file_name

if __name__ == "__main__":
    print(lastest_file())