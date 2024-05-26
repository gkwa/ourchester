import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Perform proximity search on text files."
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

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

    search_parser = subparsers.add_parser("search", help="Search indexed text files")
    search_parser.add_argument("query", type=str, help="Proximity search query")
    search_parser.add_argument(
        "-i",
        "--index",
        type=str,
        default="index",
        help="Directory containing the index",
    )

    return parser.parse_args()
