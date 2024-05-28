import logging

import whoosh.qparser

logger = logging.getLogger(__name__)


def perform_proximity_search(ix, query_str):
    with ix.searcher() as searcher:
        query = whoosh.qparser.QueryParser("content", ix.schema).parse(query_str)
        logger.debug(f"Parsed query: {query}")
        results = searcher.search(query, limit=None)
        return [dict(hit) for hit in results]
