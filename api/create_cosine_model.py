
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import os

print(" Création du modèle Cosine Similarity...")


df = pd.read_csv('data/influenceurs_recommendation_ready.csv')
X = np.load('data/feature_matrix.npy')

print(f" Données chargées: {len(df)} influenceurs, {X.shape[1]} features")

# 2. Définir une classe simple
class CosineSimilarityRecommender:
    """Recommandateur basé sur la similarité cosinus"""
    
    def __init__(self, X, df):
        self.X = X
        self.df = df
        self.name = "Cosine Similarity"
        self.similarity_matrix = cosine_similarity(X)
        print(f" Matrice de similarité créée: {self.similarity_matrix.shape}")
    
    def recommend(self, query_idx, n=5):
        """Recommande des influenceurs similaires"""

        similar_indices = np.argsort(self.similarity_matrix[query_idx])[::-1][1:n+1]
        similarity_scores = self.similarity_matrix[query_idx][similar_indices]
        
        return similar_indices, similarity_scores
    
    def get_info(self):
        """Informations sur le modèle"""
        return {
            'name': self.name,
            'type': 'Similarité cosinus',
            'num_influencers': len(self.df),
            'num_features': self.X.shape[1],
            'similarity_matrix_shape': self.similarity_matrix.shape
        }


model = CosineSimilarityRecommender(X, df)


os.makedirs('models', exist_ok=True)
with open('models/best_model_cosine_similarity.pkl', 'wb') as f:
    pickle.dump(model, f)

print(" Modèle sauvegardé: models/best_model_cosine_similarity.pkl")


print("\n Test du modèle...")
test_idx = 0
similar_indices, scores = model.recommend(test_idx, 3)

print(f"Recommandations pour: {df.iloc[test_idx]['influencer_name']}")
for i, (idx, score) in enumerate(zip(similar_indices, scores), 1):
    inf = df.iloc[idx]
    print(f"{i}. {inf['influencer_name']}")
    print(f"   Catégorie: {inf['category']}, Pays: {inf['country']}")
    print(f"   Similarité: {score:.3f}")

print("\n Modèle prêt à être utilisé dans architecture_finale.py !")