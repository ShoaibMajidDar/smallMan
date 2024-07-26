from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import chromadb, os
from dotenv import load_dotenv
load_dotenv()



def get_or_create_chroma_collection():

    client = chromadb.PersistentClient(path="./vectordb")

    collection = client.get_or_create_collection(
        name="myCollection",
        embedding_function=OpenAIEmbeddingFunction(api_key=os.environ.get("api_key")),
    )

    return collection



def save_embedding(contents):
    try:
        contents = contents.decode("utf-8")
        chunks = contents.split("<<<\n\n\n")
        collection = get_or_create_chroma_collection()
        print("2")
        no_of_chunks_stored_in_chromadb = collection.count()
        print("3")
        generate_ids = lambda: [
            f"{i+no_of_chunks_stored_in_chromadb}" for i in range(len(chunks))
        ]
        ids = generate_ids()
        print("4")
        collection.upsert(documents=chunks, ids=ids)
        print("5")
        return True
    except: 
        return False
    
def get_similar_chunks(query):
    collection = get_or_create_chroma_collection()
    chunks = collection.query( 
                        query_texts=[query],
                        n_results=5,
                        )
    return chunks

    

