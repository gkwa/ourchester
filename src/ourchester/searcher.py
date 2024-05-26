import whoosh.qparser


def perform_proximity_search(ix, query_str):
    with ix.searcher() as searcher:
        query = whoosh.qparser.QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        print(f"Found {len(results)} documents:")
        for hit in results:
            print(f"Path: {hit['path']}")
