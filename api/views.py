# api/views.py - VERSION CORRIGÉE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

class HealthCheckView(APIView):
    """Vérification de la santé de l'API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'Brandfluence Recommendation API',
            'version': '1.0.0'
        })

class BrandfluenceRecommender:
    """Système de recommandation Brandfluence - VERSION CORRIGÉE"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrandfluenceRecommender, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.initialized = True
            self._initialize()
    
    def _initialize(self):
        """Initialise le système de recommandation"""
        try:
            # Chemin vers le fichier data
            data_path = 'data/influenceurs_recommendation_ready.csv'
            
            if not os.path.exists(data_path):
                # Essayer un autre chemin
                data_path = '../data/influenceurs_recommendation_ready.csv'
            
            self.df = pd.read_csv(data_path)
            print(f"✓ Données chargées: {len(self.df)} influenceurs")
            
            # Créer la matrice de features
            self.X = self._create_feature_matrix()
            
            # Calculer la matrice de similarité
            self.similarity_matrix = cosine_similarity(self.X)
            print(f"✓ Matrice de similarité: {self.similarity_matrix.shape}")
            
            # Stocker les valeurs uniques
            self.categories = sorted(self.df['category'].dropna().unique().tolist())
            self.countries = sorted(self.df['country'].dropna().unique().tolist())
            
        except Exception as e:
            print(f"✗ Erreur d'initialisation: {e}")
            raise
    
    def _create_feature_matrix(self):
        """Crée la matrice de features"""
        scaler = StandardScaler()
        features_list = []
        
        # Normaliser les features numériques
        for col in ['followers', 'engagement_rate', 'global_score']:
            if col in self.df.columns:
                normalized = scaler.fit_transform(self.df[[col]].fillna(0))
                features_list.append(normalized)
        
        # Encoder la catégorie
        if 'category' in self.df.columns:
            le = LabelEncoder()
            category_encoded = le.fit_transform(self.df['category'].fillna('Unknown')).reshape(-1, 1)
            features_list.append(category_encoded)
        
        # Encoder le pays
        if 'country' in self.df.columns:
            le = LabelEncoder()
            country_encoded = le.fit_transform(self.df['country'].fillna('Unknown')).reshape(-1, 1)
            features_list.append(country_encoded)
        
        return np.hstack(features_list) if features_list else np.random.randn(len(self.df), 5)
    
    def recommend(self, category, country, n=5):
        """Recommande des influenceurs AVEC FILTRES PAR CATÉGORIE/PAYS"""
        category = str(category).strip().title()
        country = str(country).strip().title()
        n = max(1, min(n, 20))
        
        # 1. Filtrer par catégorie et pays
        mask = (self.df['category'].str.title() == category) & \
               (self.df['country'].str.title() == country)
        
        if not mask.any():
            mask = self.df['category'].str.title() == category
            if not mask.any():
                return {'error': f'Aucun influenceur trouvé pour {category}/{country}'}
        
        # 2. Get reference influencer
        if 'global_score' in self.df.columns and mask.any():
            idx = self.df[mask]['global_score'].idxmax()
        else:
            idx = self.df[mask].index[0]
        
        reference = self.df.iloc[idx]
        
        # 3. Get ALL similar influencers
        similar_indices = np.argsort(self.similarity_matrix[idx])[::-1][1:]  # Tous sauf lui-même
        similarity_scores = self.similarity_matrix[idx][similar_indices]
        
        # 4. FILTRER pour ne garder que ceux de la même catégorie/pays
        filtered_indices = []
        filtered_scores = []
        
        for inf_idx, score in zip(similar_indices, similarity_scores):
            inf = self.df.iloc[inf_idx]
            # Vérifier si l'influenceur a la même catégorie et pays
            if (str(inf['category']).title() == category and 
                str(inf['country']).title() == country):
                filtered_indices.append(inf_idx)
                filtered_scores.append(score)
                
                # Arrêter quand on a assez de résultats
                if len(filtered_indices) >= n:
                    break
        
        # Si pas assez de résultats avec le filtrage strict, assouplir
        if len(filtered_indices) < n:
            # Accepter juste la même catégorie
            for inf_idx, score in zip(similar_indices, similarity_scores):
                if inf_idx in filtered_indices:
                    continue
                    
                inf = self.df.iloc[inf_idx]
                if str(inf['category']).title() == category:
                    filtered_indices.append(inf_idx)
                    filtered_scores.append(score)
                    
                    if len(filtered_indices) >= n:
                        break
        
        # Si toujours pas assez, prendre les plus similaires tout court
        if len(filtered_indices) < n:
            for inf_idx, score in zip(similar_indices, similarity_scores):
                if inf_idx in filtered_indices:
                    continue
                    
                filtered_indices.append(inf_idx)
                filtered_scores.append(score)
                
                if len(filtered_indices) >= n:
                    break
        
        # 5. Build recommendations
        recommendations = []
        for i, (inf_idx, score) in enumerate(zip(filtered_indices[:n], filtered_scores[:n]), 1):
            inf = self.df.iloc[inf_idx]
            recommendations.append({
                'rank': i,
                'id': int(inf_idx),
                'name': str(inf['influencer_name']),
                'category': str(inf['category']),
                'country': str(inf['country']),
                'followers': int(inf['followers']),
                'followers_formatted': self._format_number(inf['followers']),
                'engagement_rate': float(inf['engagement_rate']),
                'similarity_score': float(score)
            })
        
        return {
            'success': True,
            'query': {'category': category, 'country': country, 'n': n},
            'reference': {
                'id': int(idx),
                'name': str(reference['influencer_name']),
                'category': str(reference['category']),
                'country': str(reference['country'])
            },
            'recommendations': recommendations,
            'total': len(recommendations),
            'note': 'Recommandations filtrées par catégorie/pays' if len(filtered_indices) >= n else 'Filtrage partiel appliqué'
        }
    
    def search(self, category=None, country=None, min_followers=0, limit=10):
        """Recherche d'influenceurs"""
        mask = pd.Series([True] * len(self.df))
        
        if category:
            mask &= self.df['category'].str.title() == category.title()
        
        if country:
            mask &= self.df['country'].str.title() == country.title()
        
        if min_followers > 0:
            mask &= self.df['followers'] >= min_followers
        
        results_df = self.df[mask].sort_values('global_score', ascending=False).head(limit)
        
        results = []
        for _, row in results_df.iterrows():
            results.append({
                'id': int(row.name),
                'name': str(row['influencer_name']),
                'category': str(row['category']),
                'country': str(row['country']),
                'followers': int(row['followers']),
                'followers_formatted': self._format_number(row['followers']),
                'engagement_rate': float(row['engagement_rate'])
            })
        
        return {
            'success': True,
            'results': results,
            'count': len(results)
        }
    
    def stats(self):
        """Statistiques du système"""
        return {
            'total_influencers': len(self.df),
            'categories': self.categories,
            'countries': self.countries,
            'avg_followers': int(self.df['followers'].mean()),
            'avg_engagement': float(self.df['engagement_rate'].mean())
        }
    
    def _format_number(self, num):
        """Formate un nombre"""
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return str(num)

# Initialize recommender singleton
recommender = BrandfluenceRecommender()

class StatsView(APIView):
    """Statistiques du système"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        stats = recommender.stats()
        return Response(stats)

class CategoriesView(APIView):
    """Liste des catégories"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'categories': recommender.categories,
            'count': len(recommender.categories)
        })

class CountriesView(APIView):
    """Liste des pays"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'countries': recommender.countries,
            'count': len(recommender.countries)
        })

class RecommendView(APIView):
    """Recommandation d'influenceurs"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # GET parameters
        category = request.GET.get('category', '')
        country = request.GET.get('country', '')
        n = request.GET.get('n', 5)
        
        try:
            n = int(n)
        except:
            n = 5
        
        if not category or not country:
            return Response({
                'error': 'Les paramètres "category" et "country" sont requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = recommender.recommend(category, country, n)
        
        if 'error' in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        return Response(result)
    
    def post(self, request):
        # POST body
        category = request.data.get('category', '')
        country = request.data.get('country', '')
        n = request.data.get('n', 5)
        
        if not category or not country:
            return Response({
                'error': 'Les champs "category" et "country" sont requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = recommender.recommend(category, country, n)
        
        if 'error' in result:
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        
        return Response(result)

class SearchView(APIView):
    """Recherche d'influenceurs"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        category = request.GET.get('category', '')
        country = request.GET.get('country', '')
        min_followers = request.GET.get('min_followers', 0)
        limit = request.GET.get('limit', 10)
        
        try:
            min_followers = int(min_followers)
            limit = int(limit)
        except:
            min_followers = 0
            limit = 10
        
        result = recommender.search(
            category=category if category else None,
            country=country if country else None,
            min_followers=min_followers,
            limit=limit
        )
        
        return Response(result)

class InfluencerDetailView(APIView):
    """Détails d'un influenceur"""
    permission_classes = [AllowAny]
    
    def get(self, request, influencer_id):
        try:
            influencer_id = int(influencer_id)
        except:
            return Response({'error': 'ID invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        if influencer_id < 0 or influencer_id >= len(recommender.df):
            return Response({
                'error': f'ID {influencer_id} invalide. Doit être entre 0 et {len(recommender.df)-1}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        inf = recommender.df.iloc[influencer_id]
        
        return Response({
            'id': int(influencer_id),
            'name': str(inf['influencer_name']),
            'category': str(inf['category']),
            'country': str(inf['country']),
            'followers': int(inf['followers']),
            'followers_formatted': recommender._format_number(inf['followers']),
            'engagement_rate': float(inf['engagement_rate']),
            'global_score': float(inf.get('global_score', 0))
        })