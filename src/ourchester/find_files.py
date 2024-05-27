import argparse
import collections
import pathlib


class FileWithTimestamp:
    def __init__(self, file, timestamp):
        self.file = file
        self.timestamp = timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp


def find_files(directory):
    files = []

    def scan_dir(path):
        for entry in pathlib.Path(path).rglob("*"):
            if entry.is_file():
                files.append(entry)

    scan_dir(directory)
    return files


def filter_files(files, exclude_substrings):
    return [
        file
        for file in files
        if not any(substring in str(file) for substring in exclude_substrings)
    ]


def filter_by_extensions(files, extensions):
    extensions = [f".{ext}" for ext in extensions if not ext.startswith(".")]
    extensions = [ext.lower() for ext in extensions]
    if extensions:
        return [file for file in files if any(file.suffix == ext for ext in extensions)]
    return files


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Find files in the specified directory."
    )
    parser.add_argument("directory", type=str, help="The directory to search in.")
    parser.add_argument(
        "--exclude",
        type=str,
        action="append",
        default=[],
        help="Substrings to exclude from paths.",
    )
    parser.add_argument(
        "--ext",
        type=str,
        action="append",
        default=[],
        help="File extensions to include.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    files = find_files(args.directory)
    files = filter_files(files, args.exclude)
    files = filter_by_extensions(files, args.ext)

    file_timestamps = collections.deque()
    for file in files:
        file_timestamps.append(FileWithTimestamp(file, file.stat().st_mtime))

    # Sort the files by timestamp
    file_timestamps = sorted(file_timestamps, key=lambda x: x.timestamp)

    for file_with_timestamp in file_timestamps:
        print(
            f"{file_with_timestamp.file}, Timestamp: {file_with_timestamp.timestamp}"
        )


if __name__ == "__main__":
    main()
