from pathlib import Path
import os, sys
import argparse
import filecmp

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
            log_path.mkfile()
            print(f'Log file created: {log_path}')
        return source_path, replica_path, args['interval'], log_path
    else:
        print("Error: source directory doesn't exist")
        sys.exit(1)

def synchronizeFolders(source, replica, log):

    #Check and copy files from source to replica
    for file in source.glob("*"):
        replica_file = replica / file.name
        if replica_file.exists():
            #comparar ficheiros usando filecmp / hash
            #se foram iguais não há operacao . se forem diferentes copia ficheiro para replica
            pass
        else:
            #cria ficheiro na replica
            pass

    #Check files from replica to source and delete those that dont exist


def writeLogFile(log_path, log):
    pass

def main():
    source, replica, interval, log = argumentParser()

    try:
        print('Folder synchronization started')
        synchronizeFolders(source, replica, log)
        print('Folder synchronization ended')

    except KeyboardInterrupt:
        print('Folder synchronization interrupted')


if __name__ == "__main__":
    main()