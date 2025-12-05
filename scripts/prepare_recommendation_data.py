# prepare_recommendation_data.py - VERSION CORRIGÉE
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pickle
import json
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')
import os

# Connexion à PostgreSQL
engine = create_engine('postgresql://postgres:0000@localhost:5432/brandfluence')

def load_and_prepare_data():
    """Charge et prépare les données pour la recommandation"""
    print(" Chargement des données depuis PostgreSQL...")
    
    try:
        # Essayer d'abord influenceurs_enhanced
        df = pd.read_sql("SELECT * FROM influenceurs_enhanced", engine)
        print(" Table 'influenceurs_enhanced' trouvée")
    except:
        # Sinon utiliser influenceurs_simple et créer les features
        print(" Table 'influenceurs_enhanced' non trouvée, utilisation de 'influenceurs_simple'")
        df = pd.read_sql("SELECT * FROM influenceurs_simple", engine)
        
        # Créer les features manquantes
        print(" Création des features manquantes...")
        
        # Normaliser les noms de colonnes
        df.columns = [col.lower().replace(' ', '_').replace('.', '_') for col in df.columns]
        
        # Créer popularity_score s'il n'existe pas
        if 'popularity_score' not in df.columns:
            # Normaliser les valeurs pour calculer le score
            if 'followers' in df.columns:
                df['followers_normalized'] = (df['followers'] - df['followers'].min()) / (df['followers'].max() - df['followers'].min())
            else:
                df['followers_normalized'] = 0.5
            
            if 'engagement_rate' in df.columns:
                df['engagement_normalized'] = (df['engagement_rate'] - df['engagement_rate'].min()) / (df['engagement_rate'].max() - df['engagement_rate'].min())
            else:
                df['engagement_normalized'] = 0.5
            
            df['popularity_score'] = (
                df['followers_normalized'] * 0.4 +
                df['engagement_normalized'] * 0.3 +
                np.random.rand(len(df)) * 0.3  # Un peu d'aléatoire
            )
        
        # Créer influence_score s'il n'existe pas
        if 'influence_score' not in df.columns:
            df['influence_score'] = 100.0
        
        # S'assurer que les colonnes nécessaires existent
        required_columns = ['category', 'country', 'channel_info']
        for col in required_columns:
            if col not in df.columns:
                df[col] = 'Unknown'
    
    print(f" {len(df)} influenceurs chargés")
    
    # Nettoyage final
    df['category'] = df['category'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['channel_info'] = df['channel_info'].fillna('')
    
    # S'assurer que les colonnes numériques existent
    numeric_features = ['followers', 'engagement_rate', 'posts', 'avg_likes', 'avg_comments']
    for feature in numeric_features:
        if feature not in df.columns:
            print(f" Colonne {feature} manquante, création avec valeurs par défaut")
            if feature == 'engagement_rate':
                df[feature] = 7.5  # Valeur moyenne
            else:
                df[feature] = df.get(feature + '_normalized', 0.5) * 1000
    
    # Créer des features pour la recommandation
    print(" Création des features pour la recommandation...")
    
    # 1. Normalisation des features numériques
    scaler = StandardScaler()
    for feature in numeric_features:
        if feature in df.columns:
            col_name = f'{feature}_normalized'
            df[col_name] = scaler.fit_transform(df[[feature]].fillna(0))
    
    # 2. Encodage des catégories
    le_category = LabelEncoder()
    df['category_encoded'] = le_category.fit_transform(df['category'])
    
    # 3. Encodage des pays
    le_country = LabelEncoder()
    df['country_encoded'] = le_country.fit_transform(df['country'])
    
    # 4. Feature textuelle (channel_info)
    tfidf = TfidfVectorizer(max_features=30, stop_words='english')  # Réduit à 30 features
    tfidf_matrix = tfidf.fit_transform(df['channel_info'].fillna(''))
    
    # Convertir en DataFrame
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), 
                           columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])],
                           index=df.index)
    
    # Combiner avec le DataFrame original
    df = pd.concat([df, tfidf_df], axis=1)
    
    # 5. Calculer un score global si pas déjà fait
    if 'global_score' not in df.columns:
        df['global_score'] = (
            df.get('popularity_score', 0.5) * 0.4 +
            df.get('engagement_rate_normalized', 0.5) * 0.3 +
            df.get('followers_normalized', 0.5) * 0.2 +
            np.random.rand(len(df)) * 0.1
        )
    
    print(f" Données préparées: {df.shape[1]} colonnes")
    
    # Sauvegarder les encodeurs
    print("💾 Sauvegarde des encodeurs...")
    os.makedirs('models', exist_ok=True)
    
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    with open('models/le_category.pkl', 'wb') as f:
        pickle.dump(le_category, f)
    
    with open('models/le_country.pkl', 'wb') as f:
        pickle.dump(le_country, f)
    
    with open('models/tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    
    return df

def create_feature_matrix(df):
    """Crée la matrice de features pour les modèles"""
    print(" Création de la matrice de features...")
    
    # Sélectionner les features pour la similarité
    feature_columns = []
    
    # Features numériques normalisées
    numeric_features = ['followers_normalized', 'engagement_rate_normalized']
    if 'posts_normalized' in df.columns:
        numeric_features.append('posts_normalized')
    if 'avg_likes_normalized' in df.columns:
        numeric_features.append('avg_likes_normalized')
    if 'avg_comments_normalized' in df.columns:
        numeric_features.append('avg_comments_normalized')
    if 'influence_score_normalized' in df.columns:
        numeric_features.append('influence_score_normalized')
    
    for feature in numeric_features:
        if feature in df.columns:
            feature_columns.append(feature)
    
    # Features encodées
    if 'category_encoded' in df.columns:
        feature_columns.append('category_encoded')
    if 'country_encoded' in df.columns:
        feature_columns.append('country_encoded')
    
    # Features TF-IDF (prendre un sous-ensemble)
    tfidf_columns = [col for col in df.columns if col.startswith('tfidf_')]
    feature_columns.extend(tfidf_columns[:10])  # Prendre seulement 10 features TF-IDF
    
    print(f" Features sélectionnées: {len(feature_columns)}")
    print(f"   • Numériques: {len([f for f in feature_columns if 'normalized' in f])}")
    print(f"   • Encodées: {len([f for f in feature_columns if 'encoded' in f])}")
    print(f"   • TF-IDF: {len([f for f in feature_columns if 'tfidf' in f])}")
    
    # Créer la matrice
    X = df[feature_columns].fillna(0).values
    
    print(f" Matrice créée: {X.shape[0]} samples, {X.shape[1]} features")
    
    # Sauvegarder la liste des features
    with open('models/feature_columns.pkl', 'wb') as f:
        pickle.dump(feature_columns, f)
    
    return X, feature_columns

def save_prepared_data(df, X):
    """Sauvegarde les données préparées"""
    print(" Sauvegarde des données préparées...")
    
    os.makedirs('data', exist_ok=True)
    
    # Sauvegarder le DataFrame enrichi
    df.to_csv('data/influenceurs_recommendation_ready.csv', index=False)
    
    # Sauvegarder la matrice de features
    np.save('data/feature_matrix.npy', X)
    
    # Sauvegarder les métadonnées
    metadata = {
        'num_influencers': len(df),
        'num_features': X.shape[1],
        'categories': df['category'].unique().tolist(),
        'countries': df['country'].unique().tolist(),
        'date_prepared': pd.Timestamp.now().isoformat(),
        'columns': df.columns.tolist()[:20]  # Premières 20 colonnes seulement
    }
    
    with open('data/metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(" Données sauvegardées dans 'data/'")

def main():
    """Fonction principale"""
    print(" PRÉPARATION DES DONNÉES POUR RECOMMANDATION")
    print("="*60)
    
    # Créer les dossiers nécessaires
    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # 1. Charger et préparer les données
    df = load_and_prepare_data()
    
    # 2. Créer la matrice de features
    X, feature_columns = create_feature_matrix(df)
    
    # 3. Sauvegarder
    save_prepared_data(df, X)
    
    # 4. Statistiques
    print("\n STATISTIQUES FINALES:")
    print(f"   • Influenceurs: {len(df)}")
    print(f"   • Features: {len(feature_columns)}")
    print(f"   • Catégories: {df['category'].nunique()}")
    print(f"   • Pays: {df['country'].nunique()}")
    print(f"   • Score global moyen: {df['global_score'].mean():.3f}")
    
    # Aperçu des données
    print("\n APERÇU DES DONNÉES:")
    print(df[['influencer_name', 'category', 'country', 'followers', 'engagement_rate', 'global_score']].head(3))
    
    print("\n PRÉPARATION TERMINÉE !")
    print("="*60)
    print("\n📁 FICHIERS CRÉÉS:")
    print("  data/influenceurs_recommendation_ready.csv")
    print("  data/feature_matrix.npy")
    print("  data/metadata.json")
    print("  models/scaler.pkl")
    print("  models/le_category.pkl")
    print("  models/le_country.pkl")
    print("  models/tfidf.pkl")
    print("  models/feature_columns.pkl")

if __name__ == "__main__":
    main()