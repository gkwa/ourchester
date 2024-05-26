import pathlib
from . import cli, logging
from . import main as mainmod

__project_name__ = "ourchester"

def main() -> int:
    logging.configure_logging()
    args = cli.parse_args()

    if args.command == "index":
        directory = pathlib.Path(args.directory)
        index_dir = pathlib.Path(args.index)
        mainmod.index_markdown_files(directory, index_dir)
    elif args.command == "search":
        index_dir = pathlib.Path(args.index)
        index = mainmod.load_index(index_dir)
        mainmod.perform_proximity_search(index, args.query)

    return 0

