import pathlib

from . import cli, indexer, logging, searcher

__project_name__ = "ourchester"


def main() -> int:
    logging.configure_logging()
    args = cli.parse_args()

    if args.command == "index":
        directories = [pathlib.Path(dir) for dir in args.directories]
        index_dir = pathlib.Path(args.index)
        indexer.index_files(directories, index_dir, args.extensions)
    elif args.command == "search":
        index_dir = pathlib.Path(args.index)
        index = indexer.load_index(index_dir)
        results = searcher.perform_proximity_search(index, args.query)
        _print_search_results(results)

    return 0


def _print_search_results(results):
    print(f"Found {len(results)} documents:")
    for hit in results:
        print(f"Path: {hit['path']}")
