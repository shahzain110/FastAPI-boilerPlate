import chromadb
# chroma_client = chromadb.PersistentClient(path="app/vector_db/chroma")
chroma_client = chromadb.HttpClient(host='93.127.132.103', port=8000)


# collection = chroma_client.get_collection("69204b6f4c5fce72cb47d863")
# data = collection.get()
# print(data)
# metadata = collection.metadata
# print("ChromaDB Collection Metadata: ", metadata)


# print("ChromaDB client initialized successfully. > ", chroma_client.list_collections())