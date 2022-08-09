import pickle
import numpy as np
import torch
from sentence_transformers import SentenceTransformer


class SentenceSimilarityBert:
    def __init__(self):
        super().__init__()
        self.model = SentenceTransformer("colorfulscoop/sbert-base-ja")
        self.model.eval()
        self.embeddings = None

    def load_embeddings(self, path):
        self.embeddings = pickle.load(open(path, 'rb'))

    def get_embedding(self, text: str):
        with torch.no_grad():
            output = self.model.encode(text)
        return output
    
    def get_product_idc(self, query: str):
        query_embedding = self.get_embedding(query)
        similarities = {}
        for idx, embedding in self.embeddings.items():
            similarities[idx] = self.compute_cosine_similarity(embedding, query_embedding)
            
        similarities_sorted = dict(sorted(similarities.items(), key=lambda item: item[1]))
        top_20_idc = sorted(list(similarities_sorted.keys())[-20:], reverse=True)
        top_20_percentages = sorted(list(similarities_sorted.values())[-20:], reverse=True)
        return {str(top_20_idc[i]): top_20_percentages[i] for i in range(20)}
    
    def compute_cosine_similarity(self, emb1, emb2):
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-9)
        return similarity