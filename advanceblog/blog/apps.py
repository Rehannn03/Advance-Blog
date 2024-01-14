from django.apps import AppConfig
from sentence_transformers import SentenceTransformer
# from transformers import pipeline

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # summarizer = pipeline('summarization')

