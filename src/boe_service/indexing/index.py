from boe_service.indexing.qdrant_db import connect_to_local


def main():
    # Create a local Qdrant database
    client = connect_to_local()
    if not client:
        return

    doc_collection = client.get_collection("documents")
    print(doc_collection.config.params)


if __name__ == "__main__":
    main()
