import logging

import whoosh.fields
import whoosh.index

logger = logging.getLogger(__name__)


def index_files(directories, index_dir, extensions):
    schema = whoosh.fields.Schema(
        path=whoosh.fields.ID(unique=True, stored=True),
        content=whoosh.fields.TEXT(stored=True),
    )
    ix = _create_or_open_index(index_dir, schema)
    writer = ix.writer()
    indexed_paths = _index_directories(directories, extensions, writer)
    _remove_deleted_files(ix, indexed_paths, writer)
    writer.commit()


def _create_or_open_index(index_dir, schema):
    if not index_dir.exists():
        index_dir.mkdir(parents=True)
        return whoosh.index.create_in(str(index_dir), schema)
    else:
        return whoosh.index.open_dir(str(index_dir))


def _index_directories(directories, extensions, writer):
    indexed_paths = set()
    for directory in directories:
        logger.info(f"Indexing directory: {directory}")
        for ext in extensions:
            file_pattern = f"**/*.{ext}"
            text_files = directory.glob(file_pattern)
            for file_path in text_files:
                logging.debug(f"indexing {file_path}")
                file_path_str = _resolve_file_path(file_path)
                if file_path_str:
                    indexed_paths.add(file_path_str)
                    _index_file(file_path, file_path_str, writer)
    return indexed_paths


def _resolve_file_path(file_path):
    if file_path.is_symlink():
        try:
            file_path = file_path.resolve(strict=True)
            return str(file_path)
        except FileNotFoundError:
            logger.warning(f"Broken symlink: {file_path}")
            return None
    else:
        return str(file_path)


def _index_file(file_path, file_path_str, writer):
    with file_path.open(encoding="utf-8") as file:
        content = file.read()
    writer.update_document(path=file_path_str, content=content)


def _remove_deleted_files(ix, indexed_paths, writer):
    to_delete = [
        doc["path"]
        for doc in ix.searcher().documents()
        if doc["path"] not in indexed_paths
    ]
    for path in to_delete:
        writer.delete_by_term("path", path)


def load_index(index_dir):
    return whoosh.index.open_dir(str(index_dir))
