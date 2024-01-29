from django.apps import AppConfig
from sentence_transformers import SentenceTransformer
import chromadb
# from transformers import pipeline

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    chroma_client=chromadb.PersistentClient(path="./my_vector_db")
    chroma_collection=chroma_client.get_collection(name="blogs")
    

