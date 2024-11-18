from datetime import datetime
from pathlib import Path
from filecmp import cmp
import argparse
import shutil
import sys
import time

def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument('replica', type=str)
    parser.add_argument('interval', type=int)
    parser.add_argument('log', type=str)

    args = vars(parser.parse_args())

    source_path = Path(args['source'])

    #Error if source folder doesnt exist
    if source_path.is_dir():
        replica_path = Path(args['replica'])
        #Creates replica folder if it doesnt exist
        if not replica_path.is_dir():
            replica_path.mkdir()
            print(f'Replica folder created: {replica_path}')

        #Creates log file if it doesnt exist
        log_path = Path(args['log'])
        if not log_path.is_file():
            log_path.touch()
            print(f'Log file created: {log_path}')
        return source_path, replica_path, args['interval'], log_path
    else:
        print("Error: source directory doesn't exist")
        sys.exit(1)

def synchronizeFolders(source, replica, log_path):
    #Create/copy operations from source folder to replica
    for file in source.glob("*"):
        replica_path = replica / file.name
        #If file in replica folder exists, it compares both files to see if the content match. Else creates the file in replica folder
        if replica_path.exists():
            #If they are not the same copies file to replica folder
            if not cmp(source / file.name, replica / file.name):
                shutil.copy(source / file.name, replica / file.name)        
                log = f'Copied file {file.name} to replica'
                writeLogFile(log_path, log)
        else:
            shutil.copy(source / file.name, replica / file.name)
            log = f'Created file {file.name} in replica'
            writeLogFile(log_path, log)

    #Remove operation from replica folder
    for file in replica.glob('*'):
        source_path = source / file.name
        #If file doesnt exist in source folder, deletes the file in replica folder
        if not source_path.exists():
            replica_path = replica / file.name
            replica_path.unlink()
            log = f'Removed file {file.name} in replica'
            writeLogFile(log_path, log)

def writeLogFile(log_path, log):
    print(log)

    f = open(log_path, 'a')
    f.write(f'({datetime.now().strftime("%H:%M:%S")}) - {log}\n')
    f.close
    

def main():
    #Receives arguments
    source, replica, interval, log = argumentParser()

    try:
        while True:
            print('Folder synchronization started')
            synchronizeFolders(source, replica, log)
            print('Folder synchronization ended\n')

            time.sleep(interval)

    except KeyboardInterrupt:
        print('Folder synchronization interrupted')


if __name__ == "__main__":
    main()