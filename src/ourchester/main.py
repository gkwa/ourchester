import logging
import whoosh.fields
import whoosh.index
import whoosh.qparser

logger = logging.getLogger(__name__)

def index_markdown_files(directory, index_dir):
    schema = whoosh.fields.Schema(
        path=whoosh.fields.ID(unique=True, stored=True),
        content=whoosh.fields.TEXT(stored=True),
    )
    if not index_dir.exists():
        index_dir.mkdir()
        ix = whoosh.index.create_in(str(index_dir), schema)
    else:
        ix = whoosh.index.open_dir(str(index_dir))
    writer = ix.writer()
    markdown_files = directory.glob("**/*.md")
    indexed_paths = set()
    for file_path in markdown_files:
        if file_path.is_symlink():
            try:
                file_path = file_path.resolve(strict=True)
            except FileNotFoundError:
                logger.warning(f"Broken symlink: {file_path}")
                continue
        file_path_str = str(file_path)
        indexed_paths.add(file_path_str)
        with file_path.open(encoding="utf-8") as file:
            content = file.read()
        writer.update_document(path=file_path_str, content=content)
    to_delete = []
    for doc in ix.searcher().documents():
        if doc["path"] not in indexed_paths:
            to_delete.append(doc["path"])
    for path in to_delete:
        writer.delete_by_term("path", path)
    writer.commit()

def load_index(index_dir):
    return whoosh.index.open_dir(str(index_dir))

def perform_proximity_search(ix, query_str):
    with ix.searcher() as searcher:
        query = whoosh.qparser.QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        print(f"Found {len(results)} documents:")
        for hit in results:
            print(f"Path: {hit['path']}")
