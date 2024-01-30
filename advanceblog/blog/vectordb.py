from .apps import BlogConfig
chroma_collection=BlogConfig.chroma_collection

def recommend_from_vector_db(id):
    blog_embeddings=chroma_collection.get(
    ids=[str(id)],
    include=['embeddings'],
    
        )['embeddings']
    

    ids=chroma_collection.query(
        query_embeddings=blog_embeddings
    )['ids'][0]


    ids=list(map(int,ids))
    print(ids)
    return ids
    

    