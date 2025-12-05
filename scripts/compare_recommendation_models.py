# compare_recommendation_models.py
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import pairwise_distances
import warnings
warnings.filterwarnings('ignore')

# Configuration des graphiques
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_prepared_data():
    """Charge les données préparées"""
    print(" Chargement des données préparées...")
    
    df = pd.read_csv('data/influenceurs_recommendation_ready.csv')
    X = np.load('data/feature_matrix.npy')
    
    with open('models/feature_columns.pkl', 'rb') as f:
        feature_columns = pickle.load(f)

    print(f" Données chargées: {len(df)} influenceurs, {X.shape[1]} features")
    return df, X, feature_columns

class Model1_CosineSimilarity:
    """Modèle 1: Similarité Cosinus"""
    
    def __init__(self, X):
        self.X = X
        self.name = "Cosine Similarity"
        self.similarity_matrix = None
        
    def fit(self):
        """Calcule la matrice de similarité"""
        print("🔧 Entraînement du modèle Cosine Similarity...")
        self.similarity_matrix = cosine_similarity(self.X)
        return self
    
    def recommend(self, query_idx, n=5):
        """Recommande des influenceurs similaires"""
        if self.similarity_matrix is None:
            self.fit()
        
        # Obtenir les indices des plus similaires (exclure lui-même)
        similar_indices = np.argsort(self.similarity_matrix[query_idx])[::-1][1:n+1]
        similarity_scores = self.similarity_matrix[query_idx][similar_indices]
        
        return similar_indices, similarity_scores
    
    def get_model_info(self):
        """Retourne les informations du modèle"""
        return {
            'name': self.name,
            'type': 'Similarité basée sur le contenu',
            'complexity': 'Faible',
            'speed': 'Rapide (pré-calculé)',
            'memory': f"Matrice {self.similarity_matrix.shape}",
            'params': 'Aucun hyperparamètre'
        }

class Model2_KNN:
    """Modèle 2: K-Nearest Neighbors"""
    
    def __init__(self, X, n_neighbors=5):
        self.X = X
        self.n_neighbors = n_neighbors
        self.name = "K-Nearest Neighbors"
        self.model = NearestNeighbors(n_neighbors=n_neighbors+1, 
                                      metric='euclidean', 
                                      algorithm='auto')
        
    def fit(self):
        """Entraîne le modèle KNN"""
        print(" Entraînement du modèle KNN...")
        self.model.fit(self.X)
        return self
    
    def recommend(self, query_idx, n=5):
        """Recommande des influenceurs similaires"""
        if n > self.n_neighbors:
            n = self.n_neighbors
        
        # Reshape pour scikit-learn
        query = self.X[query_idx].reshape(1, -1)
        
        # Trouver les plus proches voisins
        distances, indices = self.model.kneighbors(query, n_neighbors=n+1)
        
        # Exclure le premier (lui-même)
        similar_indices = indices[0][1:n+1]
        similarity_scores = 1 / (1 + distances[0][1:n+1])  # Convertir distance en similarité
        
        return similar_indices, similarity_scores
    
    def get_model_info(self):
        """Retourne les informations du modèle"""
        return {
            'name': self.name,
            'type': 'Méthode des k-plus proches voisins',
            'complexity': 'Moyenne',
            'speed': 'Moyenne (recherche à la volée)',
            'memory': f"Stockage des {len(self.X)} points",
            'params': f'n_neighbors={self.n_neighbors}'
        }

class Model3_ContentBasedFiltering:
    """Modèle 3: Filtrage basé sur le contenu avec pondération"""
    
    def __init__(self, df, feature_columns):
        self.df = df.copy()
        self.feature_columns = feature_columns
        self.name = "Content-Based Filtering"
        
        # Poids pour différentes features
        self.weights = {
            'engagement': 0.3,
            'followers': 0.25,
            'category': 0.2,
            'popularity': 0.15,
            'diversity': 0.1
        }
    
    def calculate_similarity(self, query_idx, candidate_idx):
        """Calcule un score de similarité personnalisé"""
        query = self.df.iloc[query_idx]
        candidate = self.df.iloc[candidate_idx]
        
        score = 0
        
        # 1. Similarité d'engagement
        engagement_sim = 1 - abs(query['engagement_rate_normalized'] - 
                                candidate['engagement_rate_normalized']) / 2
        score += engagement_sim * self.weights['engagement']
        
        # 2. Similarité de followers
        followers_sim = 1 - abs(query['followers_normalized'] - 
                               candidate['followers_normalized']) / 2
        score += followers_sim * self.weights['followers']
        
        # 3. Similarité de catégorie
        category_sim = 1 if query['category'] == candidate['category'] else 0.3
        score += category_sim * self.weights['category']
        
        # 4. Popularité
        popularity_sim = candidate['global_score']
        score += popularity_sim * self.weights['popularity']
        
        # 5. Diversité (pénalité si même pays)
        diversity_penalty = 0.1 if query['country'] == candidate['country'] else 0
        score -= diversity_penalty * self.weights['diversity']
        
        return min(max(score, 0), 1)  # Normaliser entre 0 et 1
    
    def fit(self):
        """Prépare le modèle"""
        print(" Préparation du modèle Content-Based...")
        # Pas d'entraînement nécessaire pour ce modèle simple
        return self
    
    def recommend(self, query_idx, n=5):
        """Recommande des influenceurs"""
        scores = []
        
        for i in range(len(self.df)):
            if i != query_idx:
                score = self.calculate_similarity(query_idx, i)
                scores.append((i, score))
        
        # Trier par score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Prendre le top n
        similar_indices = [idx for idx, _ in scores[:n]]
        similarity_scores = [score for _, score in scores[:n]]
        
        return similar_indices, similarity_scores
    
    def get_model_info(self):
        """Retourne les informations du modèle"""
        return {
            'name': self.name,
            'type': 'Filtrage basé sur contenu avec pondération',
            'complexity': 'Personnalisable',
            'speed': 'Lent (calcul à la volée)',
            'memory': 'Faible',
            'params': f'weights={self.weights}'
        }

def evaluate_models(models, df, X, n_tests=10):
    """Évalue les modèles sur différents critères"""
    print("\n" + "="*60)
    print(" ÉVALUATION DES MODÈLES")
    print("="*60)
    
    results = {}
    
    for model_name, model in models.items():
        print(f"\n🔍 Évaluation de: {model_name}")
        
        metrics = {
            'diversity_scores': [],
            'relevance_scores': [],
            'coverage': set(),
            'execution_times': []
        }
        
        import time
        
        # Tester sur plusieurs influenceurs
        test_indices = np.random.choice(len(df), min(n_tests, len(df)), replace=False)
        
        for query_idx in test_indices:
            start_time = time.time()
            
            # Obtenir des recommandations
            recommended_indices, scores = model.recommend(query_idx, n=5)
            
            execution_time = time.time() - start_time
            metrics['execution_times'].append(execution_time)
            
            # 1. Diversité (éviter les recommandations trop similaires entre elles)
            if len(recommended_indices) > 1:
                # Calculer la distance moyenne entre les recommandations
                recommended_features = X[recommended_indices]
                diversity = np.mean(pairwise_distances(recommended_features))
                metrics['diversity_scores'].append(diversity)
            
            # 2. Couverture (combien d'items différents sont recommandés)
            metrics['coverage'].update(recommended_indices)
            
            # 3. Pertinence (simulate avec similarité cosinus comme référence)
            reference_scores = cosine_similarity(X[query_idx].reshape(1, -1), 
                                                X[recommended_indices]).flatten()
            relevance = np.mean(reference_scores)
            metrics['relevance_scores'].append(relevance)
        
        # Calculer les moyennes
        results[model_name] = {
            'avg_diversity': np.mean(metrics['diversity_scores']) if metrics['diversity_scores'] else 0,
            'avg_relevance': np.mean(metrics['relevance_scores']),
            'coverage_percentage': len(metrics['coverage']) / len(df) * 100,
            'avg_execution_time': np.mean(metrics['execution_times']),
            'model_info': model.get_model_info()
        }
        
        print(f"  • Pertinence moyenne: {results[model_name]['avg_relevance']:.3f}")
        print(f"  • Diversité moyenne: {results[model_name]['avg_diversity']:.3f}")
        print(f"  • Couverture: {results[model_name]['coverage_percentage']:.1f}%")
        print(f"  • Temps d'exécution: {results[model_name]['avg_execution_time']:.3f}s")
    
    return results

def visualize_comparison(results, df, models):
    """Visualise la comparaison des modèles"""
    print("\n CRÉATION DES VISUALISATIONS...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # 1. Bar plot: Pertinence
    model_names = list(results.keys())
    relevance_scores = [results[m]['avg_relevance'] for m in model_names]
    
    axes[0, 0].bar(model_names, relevance_scores, color='skyblue')
    axes[0, 0].set_title('Pertinence Moyenne des Recommandations')
    axes[0, 0].set_ylabel('Score de Pertinence')
    axes[0, 0].set_ylim([0, 1])
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Ajouter les valeurs sur les barres
    for i, v in enumerate(relevance_scores):
        axes[0, 0].text(i, v + 0.01, f'{v:.3f}', ha='center')
    
    # 2. Bar plot: Diversité
    diversity_scores = [results[m]['avg_diversity'] for m in model_names]
    
    axes[0, 1].bar(model_names, diversity_scores, color='lightgreen')
    axes[0, 1].set_title('Diversité Moyenne des Recommandations')
    axes[0, 1].set_ylabel('Score de Diversité')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    for i, v in enumerate(diversity_scores):
        axes[0, 1].text(i, v + 0.01, f'{v:.3f}', ha='center')
    
    # 3. Bar plot: Couverture
    coverage_scores = [results[m]['coverage_percentage'] for m in model_names]
    
    axes[0, 2].bar(model_names, coverage_scores, color='salmon')
    axes[0, 2].set_title('Couverture des Recommandations')
    axes[0, 2].set_ylabel('Pourcentage de Couverture')
    axes[0, 2].tick_params(axis='x', rotation=45)
    
    for i, v in enumerate(coverage_scores):
        axes[0, 2].text(i, v + 0.5, f'{v:.1f}%', ha='center')
    
    # 4. Bar plot: Temps d'exécution
    execution_times = [results[m]['avg_execution_time'] for m in model_names]
    
    axes[1, 0].bar(model_names, execution_times, color='gold')
    axes[1, 0].set_title('Temps d\'Exécution Moyen')
    axes[1, 0].set_ylabel('Secondes')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    for i, v in enumerate(execution_times):
        axes[1, 0].text(i, v + 0.001, f'{v:.3f}s', ha='center')
    
    # 5. Radar chart: Comparaison complète
    ax_radar = axes[1, 1]
    
    # Normaliser les scores pour le radar chart
    categories = ['Pertinence', 'Diversité', 'Couverture', 'Vitesse']
    
    # Inverser le temps (plus rapide = mieux)
    max_time = max(execution_times)
    speed_scores = [(max_time - t) / max_time for t in execution_times]
    
    # Préparer les données
    radar_data = []
    for i, model in enumerate(model_names):
        model_scores = [
            relevance_scores[i],          # Pertinence
            diversity_scores[i] / max(diversity_scores),  # Diversité normalisée
            coverage_scores[i] / 100,     # Couverture normalisée
            speed_scores[i]               # Vitesse normalisée
        ]
        radar_data.append(model_scores)
    
    # Créer le radar chart
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Fermer le cercle
    
    for i, model in enumerate(model_names):
        values = radar_data[i] + radar_data[i][:1]  # Fermer le cercle
        ax_radar.plot(angles, values, 'o-', label=model)
        ax_radar.fill(angles, values, alpha=0.25)
    
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(categories)
    ax_radar.set_title('Comparaison Radar des Modèles')
    ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    ax_radar.grid(True)
    
    # 6. Matrice de corrélation entre modèles
    ax_corr = axes[1, 2]
    
    # Créer une matrice de similarité entre les recommandations des modèles
    n_influencers = 100  # Échantillon pour le calcul
    sample_indices = np.random.choice(len(df), min(n_influencers, len(df)), replace=False)
    
    corr_matrix = np.zeros((len(model_names), len(model_names)))
    
    for i, model1 in enumerate(model_names):
        for j, model2 in enumerate(model_names):
            if i <= j:
                # Comparer les recommandations sur l'échantillon
                agreements = []
                for idx in sample_indices:
                    rec1, _ = models[model1].recommend(idx, n=3)
                    rec2, _ = models[model2].recommend(idx, n=3)
                    
                    # Calculer le recouvrement
                    overlap = len(set(rec1) & set(rec2)) / 3
                    agreements.append(overlap)
                
                corr_matrix[i, j] = np.mean(agreements)
                corr_matrix[j, i] = corr_matrix[i, j]
    
    # Heatmap
    im = ax_corr.imshow(corr_matrix, cmap='YlOrRd', vmin=0, vmax=1)
    
    # Ajouter les annotations
    for i in range(len(model_names)):
        for j in range(len(model_names)):
            text = ax_corr.text(j, i, f'{corr_matrix[i, j]:.2f}',
                               ha="center", va="center", color="black")
    
    ax_corr.set_xticks(range(len(model_names)))
    ax_corr.set_yticks(range(len(model_names)))
    ax_corr.set_xticklabels([m[:15] for m in model_names], rotation=45)
    ax_corr.set_yticklabels([m[:15] for m in model_names])
    ax_corr.set_title('Corrélation entre Modèles')
    plt.colorbar(im, ax=ax_corr)
    
    plt.tight_layout()
    plt.savefig('visualizations/model_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 7. Graphique supplémentaire: Exemple de recommandations
    fig2, ax_example = plt.subplots(figsize=(10, 6))
    
    # Prendre un exemple spécifique
    example_idx = 42
    example_influencer = df.iloc[example_idx]['influencer_name']
    
    recommendations_data = []
    for model_name, model in models.items():
        rec_indices, scores = model.recommend(example_idx, n=3)
        
        for i, (rec_idx, score) in enumerate(zip(rec_indices, scores)):
            rec_name = df.iloc[rec_idx]['influencer_name']
            recommendations_data.append({
                'Model': model_name,
                'Rank': i+1,
                'Influencer': rec_name[:20],
                'Score': score
            })
    
    rec_df = pd.DataFrame(recommendations_data)
    
    # Pivot pour heatmap
    pivot_df = rec_df.pivot(index='Model', columns='Rank', values='Score')
    
    sns.heatmap(pivot_df, annot=True, fmt='.2f', cmap='YlGnBu', ax=ax_example)
    ax_example.set_title(f'Recommandations pour: {example_influencer[:30]}...')
    ax_example.set_xlabel('Rang de Recommandation')
    
    plt.tight_layout()
    plt.savefig('visualizations/example_recommendations.png', dpi=300, bbox_inches='tight')
    plt.show()

def save_best_model(results, models):
    """Sauvegarde le meilleur modèle"""
    print("\n" + "="*60)
    print("🏆 SÉLECTION DU MEILLEUR MODÈLE")
    print("="*60)
    
    # Calculer un score composite
    model_scores = {}
    for model_name, metrics in results.items():
        composite_score = (
            metrics['avg_relevance'] * 0.4 +
            metrics['avg_diversity'] * 0.3 +
            (metrics['coverage_percentage'] / 100) * 0.2 +
            (1 / (1 + metrics['avg_execution_time'])) * 0.1
        )
        model_scores[model_name] = composite_score
    
    # Trier par score
    sorted_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)
    
    print("\n SCORES COMPOSITES:")
    for model_name, score in sorted_models:
        print(f"  {model_name}: {score:.3f}")
    
    # Sélectionner le meilleur
    best_model_name, best_score = sorted_models[0]
    best_model = models[best_model_name]
    
    print(f"\n MEILLEUR MODÈLE: {best_model_name} (score: {best_score:.3f})")
    
    # Sauvegarder le meilleur modèle
    print(f"💾 Sauvegarde du modèle: {best_model_name}")
    
    with open(f'models/best_model_{best_model_name.replace(" ", "_").lower()}.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    # Sauvegarder les résultats de comparaison
    comparison_results = {
        'best_model': best_model_name,
        'best_score': best_score,
        'all_scores': model_scores,
        'detailed_results': results,
        'timestamp': pd.Timestamp.now().isoformat()
    }
    
    with open('models/model_comparison_results.pkl', 'wb') as f:
        pickle.dump(comparison_results, f)
    
    # Exporter en JSON pour lecture facile
    import json
    
    # Convertir en format JSON-friendly
    json_results = {}
    for model_name, metrics in results.items():
        json_results[model_name] = {
            'avg_relevance': float(metrics['avg_relevance']),
            'avg_diversity': float(metrics['avg_diversity']),
            'coverage_percentage': float(metrics['coverage_percentage']),
            'avg_execution_time': float(metrics['avg_execution_time']),
            'composite_score': float(model_scores[model_name])
        }
    
    with open('models/model_comparison_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'best_model': best_model_name,
            'best_score': float(best_score),
            'model_scores': json_results,
            'recommendation': f"Utiliser {best_model_name} pour votre système de recommandation"
        }, f, indent=2, ensure_ascii=False)
    
    print("\n FICHIERS CRÉÉS:")
    print(f"  models/best_model_{best_model_name.replace(' ', '_').lower()}.pkl")
    print("  models/model_comparison_results.pkl")
    print("  models/model_comparison_results.json")
    print("  visualizations/model_comparison.png")
    print("  visualizations/example_recommendations.png")
    
    return best_model_name, best_model

def main():
    """Fonction principale"""
    print(" COMPARAISON DE 3 MODÈLES DE RECOMMANDATION")
    print("="*60)
    
    # Créer le dossier visualizations
    import os
    os.makedirs('visualizations', exist_ok=True)
    
    # 1. Charger les données
    df, X, feature_columns = load_prepared_data()
    
    # 2. Initialiser les modèles
    print("\n INITIALISATION DES 3 MODÈLES:")
    
    models = {
        'Cosine Similarity': Model1_CosineSimilarity(X).fit(),
        'K-Nearest Neighbors': Model2_KNN(X, n_neighbors=10).fit(),
        'Content-Based Filtering': Model3_ContentBasedFiltering(df, feature_columns).fit()
    }
    
    print(" 3 modèles initialisés et entraînés")
    
    # 3. Évaluer les modèles
    results = evaluate_models(models, df, X, n_tests=20)
    
    # 4. Visualiser la comparaison
    visualize_comparison(results, df, models)  # CORRECTION ICI
    
    # 5. Sauvegarder le meilleur modèle
    best_model_name, best_model = save_best_model(results, models)
    
    print("\n" + "="*60)
    print(" COMPARAISON TERMINÉE !")
    print("="*60)
    print(f"\n MODÈLE RECOMMANDÉ: {best_model_name}")
    print("\n CARACTÉRISTIQUES:")
    model_info = results[best_model_name]['model_info']
    for key, value in model_info.items():
        print(f"  {key}: {value}")
    
    print("\n PROCHAINES ÉTAPES:")
    print("  1. Utiliser le modèle sauvegardé pour votre API")
    print("  2. Tester avec des requêtes réelles")
    print("  3. Collecter du feedback pour amélioration")
    print("  4. Mettre en production l'API de recommandation")

if __name__ == "__main__":
    main()