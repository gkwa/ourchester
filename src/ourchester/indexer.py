import logging
import pathlib
import time

import whoosh.fields
import whoosh.index

logger = logging.getLogger(__name__)


def _create_or_open_index(index_home_path, schema):
    if whoosh.index.exists_in(index_home_path):
        return whoosh.index.open_dir(index_home_path)
    else:
        return whoosh.index.create_in(index_home_path, schema)


def _index_files(file_paths, writer):
    indexed_paths = set()
    for file_path in file_paths:
        logging.debug(f"deleting from whoosh index {file_path}")
        writer.delete_by_term("path", file_path)
        with open(file_path, "r") as file:
            content = file.read()
            logging.debug(f"indexing {file_path}")
            writer.add_document(path=file_path, content=content)
            indexed_paths.add(file_path)
    return indexed_paths


def _remove_deleted_files(ix, indexed_paths, writer):
    for doc in ix.searcher().documents():
        if pathlib.Path(doc["path"]).exists():
            continue
        if doc["path"] not in indexed_paths:
            logging.debug(f"deleting from whoosh index {doc['path']}")
            writer.delete_by_term("path", doc["path"])


def index_files(file_paths, index_home_path):
    schema = whoosh.fields.Schema(
        path=whoosh.fields.ID(unique=True, stored=True),
        content=whoosh.fields.TEXT(stored=True),
    )
    start_time = time.time()
    ix = _create_or_open_index(index_home_path, schema)
    writer = ix.writer()
    indexed_paths = _index_files(file_paths, writer)
    _remove_deleted_files(ix, indexed_paths, writer)
    writer.commit()
    end_time = time.time()
    indexing_time = end_time - start_time
    logger.info(f"Indexing completed in {indexing_time:.2f} seconds")


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
                    logging.debug(f"deleting from whoosh index {file_path_str}")
                    writer.delete_by_term("path", file_path_str)
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


def load_index(index_dir):
    return whoosh.index.open_dir(str(index_dir))
