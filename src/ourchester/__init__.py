import pathlib

import fishhoof.find_files
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
        fps = fishhoof.find_files.build_path_list(
            directories,
            excludes=[".git"],
            extensions=["md", "txt", "org"],
            newer=args.newer,
        )

        file_paths = [str(p.file) for p in fps]
        indexer.index_files(file_paths, index_dir)
    elif args.command == "search":
        try:
            index = indexer.load_index(index_dir)
            results = searcher.perform_proximity_search(index, args.query)
            _print_search_results(results)
        except whoosh.index.EmptyIndexError:
            print(f"Index does not exist in {index_dir}")
            print("Please run the 'index' command first to create the index.")
            return 1
    elif args.command == "config":
        print(f"Index directory: {index_dir}")

    return 0


def _get_cache_dir():
    user_cache_dir = platformdirs.user_cache_dir()
    ourchester_cache_dir = pathlib.Path(user_cache_dir) / "ourchester"
    ourchester_cache_dir.mkdir(exist_ok=True, parents=True)
    return ourchester_cache_dir


def _print_search_results(results):
    print(f"Found {len(results):,} documents:")
    for hit in results:
        print(f"{hit['path']}")
