import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Perform proximity search on Markdown files."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="Index Markdown files")
    index_parser.add_argument(
        "directory", type=str, help="Directory containing Markdown files"
    )
    index_parser.add_argument(
        "-i", "--index", type=str, default="index", help="Directory to store the index"
    )

    search_parser = subparsers.add_parser(
        "search", help="Search indexed Markdown files"
    )
    search_parser.add_argument("query", type=str, help="Proximity search query")
    search_parser.add_argument(
        "-i",
        "--index",
        type=str,
        default="index",
        help="Directory containing the index",
    )

    return parser.parse_args()
