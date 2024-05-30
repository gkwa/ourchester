import logging
import pathlib
import time
import typing

import humanize
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
        writer.delete_by_term("path", str(file_path))
        with open(file_path, "r") as file:
            content = file.read()
            logging.debug(f"indexing {file_path}")
            writer.add_document(
                path=str(file_path),
                title=file_path.with_suffix("").name,
                content=content,
            )
            indexed_paths.add(file_path)
    return indexed_paths


def _remove_deleted_files(ix, indexed_paths, writer):
    for doc in ix.searcher().documents():
        if pathlib.Path(doc["path"]).exists():
            continue
        if doc["path"] not in indexed_paths:
            logging.debug(f"deleting from whoosh index {doc['path']}")
            writer.delete_by_term("path", doc["path"])


def get_index_files(index_home_path):
    ix = whoosh.index.open_dir(index_home_path)

    with ix.reader() as reader:
        for stored_fields in reader.all_stored_fields():
            doc_title = stored_fields["title"]
            doc_path = stored_fields["path"]

            print(f"Title: {doc_title}")
            print(f"Path: {doc_path}")
            print("---")


def index_files(file_paths: typing.List[pathlib.Path], index_home_path):
    schema = whoosh.fields.Schema(
        title=whoosh.fields.TEXT(stored=True),
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
    t = humanize.naturaldelta(indexing_time)
    logger.info(f"Indexing completed in {t}")


def _create_or_open_index(index_dir, schema):
    if not index_dir.exists():
        index_dir.mkdir(parents=True)
        return whoosh.index.create_in(str(index_dir), schema)
    else:
        return whoosh.index.open_dir(str(index_dir))


def load_index(index_dir):
    return whoosh.index.open_dir(str(index_dir))
