import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Perform proximity search on text files."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    listindex_parser = subparsers.add_parser(
        "listindex", help="List files in index for debug"
    )
    listindex_parser.add_argument(
        "-i", "--index", type=str, default="index", help="Directory to store the index"
    )
    listindex_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    index_parser = subparsers.add_parser("index", help="Index text files")
    index_parser.add_argument(
        "directories", type=str, nargs="+", help="Directories containing text files"
    )
    index_parser.add_argument(
        "-i", "--index", type=str, default="index", help="Directory to store the index"
    )
    index_parser.add_argument(
        "-e",
        "--extensions",
        type=str,
        nargs="+",
        default=["txt", "md", "org"],
        help="File extensions to index (default: txt, md, org)",
    )
    index_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    index_parser.add_argument(
        "--newer",
        type=str,
        default="",
        help="Ignore files older than specified time (1h, 3.4d, 1.7y, 10s)",
    )
    index_parser.add_argument(
        "--exclude",
        type=str,
        action="append",
        default=[],
        help="Substrings to exclude from paths.",
    )
    index_parser.add_argument(
        "--ext",
        type=str,
        action="append",
        default=[],
        help="File extensions to include.",
    )

    search_parser = subparsers.add_parser("search", help="Search indexed text files")
    search_parser.add_argument("query", type=str, help="Proximity search query")
    search_parser.add_argument(
        "-i",
        "--index",
        type=str,
        default="index",
        help="Directory containing the index",
    )
    search_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    config_parser = subparsers.add_parser("config", help="Show configuration")
    config_parser.add_argument(
        "-i",
        "--index",
        type=str,
        default="index",
        help="Directory containing the index",
    )
    config_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    return parser.parse_args()
