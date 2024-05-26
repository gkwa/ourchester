import os
import pathlib

import platformdirs
import whoosh.index

from . import cli, indexer, log, searcher

__project_name__ = "ourchester"


def main() -> int:
    args = cli.parse_args()
    log.configure_logging(args.verbose)

    cache_dir = _get_cache_dir()
    index_dir = cache_dir / args.index

    if args.command == "index":
        directories = [pathlib.Path(dir) for dir in args.directories]
        indexer.index_files(directories, index_dir, args.extensions)
    elif args.command == "search":
        try:
            index = indexer.load_index(index_dir)
            results = searcher.perform_proximity_search(index, args.query)
            _print_search_results(results)
        except whoosh.index.EmptyIndexError:
            print(f"Index does not exist in {index_dir}")
            print("Please run the 'index' command first to create the index.")
            return 1

    return 0


def _get_cache_dir():
    user_cache_dir = platformdirs.user_cache_dir()
    ourchester_cache_dir = os.path.join(user_cache_dir, "ourchester")
    os.makedirs(ourchester_cache_dir, exist_ok=True)
    return pathlib.Path(ourchester_cache_dir)


def _print_search_results(results):
    print(f"Found {len(results)} documents:")
    for hit in results:
        print(f"Path: {hit['path']}")
