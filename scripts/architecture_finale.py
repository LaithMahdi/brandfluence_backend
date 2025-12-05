# architecture_finale.py
class RecommandationSystem:
    """Système final de recommandation pour votre application"""
    
    def __init__(self):
        # 1. Charger le meilleur modèle non-supervisé
        with open('models/best_model_hybrid_recommendation.pkl', 'rb') as f:
            self.model = pickle.load(f)
        
        # 2. Charger les données
        self.df = pd.read_csv('data/influenceurs_recommendation_ready.csv')
    
    def recommend_for_brand(self, category, country, n=5):
        """Recommandation pour une marque"""
        
        # Étape 1: Trouver un influenceur de référence dans cette catégorie/pays
        reference = self.find_reference_influencer(category, country)
        
        # Étape 2: Utiliser le modèle pour trouver des similaires
        recommendations = self.model.recommend(reference['index'], n)
        
        # Étape 3: Formater les résultats
        return self.format_recommendations(recommendations)
    
    def find_reference_influencer(self, category, country):
        """Trouve un influenceur de référence pour la catégorie/pays"""
        # Logique pour trouver le "meilleur" influenceur comme référence
        mask = (self.df['category'] == category) & (self.df['country'] == country)
        
        if mask.any():
            # Prendre celui avec le plus haut score
            idx = self.df[mask]['global_score'].idxmax()
        else:
            # Sinon, prendre le meilleur global de la catégorie
            idx = self.df[self.df['category'] == category]['global_score'].idxmax()
        
        return {'index': idx, 'name': self.df.loc[idx, 'influencer_name']}