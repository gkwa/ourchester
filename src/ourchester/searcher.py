import whoosh.qparser


def perform_proximity_search(ix, query_str):
    with ix.searcher() as searcher:
        query = whoosh.qparser.QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        return [dict(hit) for hit in results]
