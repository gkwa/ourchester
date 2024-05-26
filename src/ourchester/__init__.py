import pathlib

from . import cli, indexer, logging, searcher

__project_name__ = "ourchester"


def main() -> int:
    logging.configure_logging()
    args = cli.parse_args()

    if args.command == "index":
        directories = [pathlib.Path(dir) for dir in args.directories]
        index_dir = pathlib.Path(args.index)
        indexer.index_markdown_files(directories, index_dir)
    elif args.command == "search":
        index_dir = pathlib.Path(args.index)
        index = indexer.load_index(index_dir)
        searcher.perform_proximity_search(index, args.query)

    return 0
