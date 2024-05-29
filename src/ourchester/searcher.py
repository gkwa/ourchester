import logging

import whoosh.qparser

logger = logging.getLogger(__name__)


def perform_proximity_search(ix, query_str):
    with ix.searcher() as searcher:
        parser = whoosh.qparser.MultifieldParser(["title", "content"], ix.schema)
        query = parser.parse(query_str)
        logger.debug(f"Parsed query: {query}")
        results = searcher.search(query, limit=None)
        return [dict(hit) for hit in results]
