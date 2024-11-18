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

    if source_path.is_dir():
        replica_path = Path(args['replica'])
        if not replica_path.is_dir():
            replica_path.mkdir()
            print(f'Replica folder created: {replica_path}')

        log_path = Path(args['log'])
        if not log_path.is_file():
            log_path.touch()
            print(f'Log file created: {log_path}')
        return source_path, replica_path, args['interval'], log_path
    else:
        print("Error: source directory doesn't exist")
        sys.exit(1)

def synchronizeFolders(source, replica, log_path):
    #Check and copy files from source to replica
    for file in source.glob("*"):
        replica_path = replica / file.name
        if replica_path.exists():
            if not cmp(source / file.name, replica / file.name):
                shutil.copy(source / file.name, replica / file.name)        
                log = f'Copied file {file.name} to replica'
                writeLogFile(log_path, log)
        else:
            shutil.copy(source / file.name, replica / file.name)
            log = f'Created file {file.name} in replica'
            writeLogFile(log_path, log)

    #Check files from replica to source and delete those that dont exist
    for file in replica.glob('*'):
        source_path = source / file.name
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
    source, replica, interval, log = argumentParser()

    try:
        print('Folder synchronization started')
        synchronizeFolders(source, replica, log)
        print('Folder synchronization ended\n')

    except KeyboardInterrupt:
        print('Folder synchronization interrupted')


if __name__ == "__main__":
    main()