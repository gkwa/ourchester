import argparse
import datetime
import os


def find_recent_files(directory, minutes=60):
    cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
    recent_files = []

    def scan_dir(path):
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    if ".git" not in entry.path:
                        scan_dir(entry.path)
                elif entry.is_file(follow_symlinks=False):
                    if (
                        datetime.datetime.fromtimestamp(entry.stat().st_mtime)
                        > cutoff_time
                    ):
                        recent_files.append(entry.path)

    scan_dir(directory)
    return recent_files


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Find files modified within the last specified minutes."
    )
    parser.add_argument("directory", type=str, help="The directory to search in.")
    parser.add_argument(
        "-m", "--minutes", type=int, default=60, help="The time interval in minutes."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    files = find_recent_files(args.directory, args.minutes)
    for file in files:
        print(file)


if __name__ == "__main__":
    main()
