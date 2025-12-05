# verifier_qualite.py
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def verifier_qualite_donnees(csv_path='influenceurs_clean.csv'):
    """Vérifie la qualité des données nettoyées"""
    
    print("="*60)
    print("VÉRIFICATION DE LA QUALITÉ DES DONNÉES")
    print("="*60)
    
    # 1. Charger les données
    try:
        df = pd.read_csv(csv_path)
        print(f"✓ Fichier chargé: {len(df)} lignes, {len(df.columns)} colonnes")
    except Exception as e:
        print(f"✗ Erreur de chargement: {e}")
        return
    
    # 2. Vérification des colonnes
    print("\n" + "="*60)
    print("1. STRUCTURE DES DONNÉES")
    print("="*60)
    
    print("\nColonnes disponibles:")
    for i, col in enumerate(df.columns, 1):
        non_null = df[col].notna().sum()
        dtype = df[col].dtype
        pourcentage = (non_null / len(df)) * 100
        print(f"  {i:2d}. {col:20} ({dtype}): {non_null:4d} valeurs ({pourcentage:5.1f}%)")
    
    # 3. Vérification des données manquantes
    print("\n" + "="*60)
    print("2. DONNÉES MANQUANTES")
    print("="*60)
    
    cols_essentielles = ['influencer_name', 'category', 'followers', 'engagement_rate']
    print("\nColonnes essentielles (doivent être complètes):")
    for col in cols_essentielles:
        if col in df.columns:
            missing = df[col].isna().sum()
            if missing == 0:
                print(f"  ✓ {col:20}: COMPLET ({len(df)}/{len(df)} valeurs)")
            else:
                print(f"  ✗ {col:20}: {missing} valeurs manquantes")
        else:
            print(f"  ✗ {col:20}: COLONNE ABSENTE")
    
    # 4. Vérification des types de données
    print("\n" + "="*60)
    print("3. TYPES DE DONNÉES ET VALEURS")
    print("="*60)
    
    # Followers (doit être numérique)
    if 'followers' in df.columns:
        print(f"\nColonne 'followers':")
        print(f"  Type: {df['followers'].dtype}")
        print(f"  Min: {df['followers'].min():,}")
        print(f"  Max: {df['followers'].max():,}")
        print(f"  Valeurs négatives: {(df['followers'] < 0).sum()}")
        
        # Vérifier s'il reste des 'k', 'm'
        if df['followers'].dtype == 'object':
            has_k_m = df['followers'].astype(str).str.contains('[km]', case=False, na=False).any()
            if has_k_m:
                print("  ✗ ATTENTION: Contient encore 'k' ou 'm'")
            else:
                print("  ✓ Format numérique correct")
    
    # Engagement rate (doit être entre 0 et 100)
    if 'engagement_rate' in df.columns:
        print(f"\nColonne 'engagement_rate':")
        print(f"  Type: {df['engagement_rate'].dtype}")
        print(f"  Min: {df['engagement_rate'].min():.2f}%")
        print(f"  Max: {df['engagement_rate'].max():.2f}%")
        
        # Vérifier la plage
        hors_plage = ((df['engagement_rate'] < 0) | (df['engagement_rate'] > 100)).sum()
        if hors_plage > 0:
            print(f"  ✗ {hors_plage} valeurs hors plage [0-100]%")
        else:
            print("  ✓ Toutes les valeurs sont entre 0% et 100%")
    
    # 5. Vérification des catégories
    if 'category' in df.columns:
        print(f"\nColonne 'category':")
        print(f"  Nombre de catégories uniques: {df['category'].nunique()}")
        print(f"  Catégories: {', '.join(sorted(df['category'].dropna().unique().astype(str)))}")
        
        # Vérifier les catégories inconnues
        unknown_count = (df['category'] == 'Unknown').sum()
        if unknown_count > 0:
            print(f"  ⚠ {unknown_count} catégories marquées 'Unknown'")
    
    # 6. Vérification des doublons
    print("\n" + "="*60)
    print("4. DOUBLONS ET INCOHÉRENCES")
    print("="*60)
    
    # Doublons exacts
    duplicates = df.duplicated().sum()
    print(f"\nLignes dupliquées exactes: {duplicates}")
    if duplicates > 0:
        print("  ✗ Des doublons exacts ont été trouvés")
    else:
        print("  ✓ Pas de doublons exacts")
    
    # Doublons sur le nom
    if 'influencer_name' in df.columns:
        name_duplicates = df['influencer_name'].duplicated().sum()
        print(f"\nNoms d'influenceurs dupliqués: {name_duplicates}")
        if name_duplicates > 0:
            print("  ✗ Certains influenceurs apparaissent plusieurs fois")
            # Afficher les doublons
            dup_names = df[df['influencer_name'].duplicated(keep=False)]['influencer_name'].unique()
            print(f"  Exemples: {dup_names[:5]}")
    
    # 7. Statistiques descriptives
    print("\n" + "="*60)
    print("5. STATISTIQUES DESCRIPTIVES")
    print("="*60)
    
    if 'followers' in df.columns and 'engagement_rate' in df.columns:
        print("\nCorrélation followers / engagement:")
        correlation = df['followers'].corr(df['engagement_rate'])
        print(f"  Coefficient de corrélation: {correlation:.3f}")
        
        if correlation < -0.3:
            print("  ↑ Forte corrélation négative (plus de followers = moins d'engagement)")
        elif correlation > 0.3:
            print("  ↑ Forte corrélation positive")
        else:
            print("  → Faible corrélation")
    
    # 8. Score de qualité
    print("\n" + "="*60)
    print("SCORE DE QUALITÉ")
    print("="*60)
    
    score = 100
    problemes = []
    
    # Critères de qualité
    if 'followers' in df.columns and df['followers'].dtype != 'int64':
        score -= 20
        problemes.append("Followers pas en format numérique")
    
    if 'engagement_rate' in df.columns:
        hors_plage = ((df['engagement_rate'] < 0) | (df['engagement_rate'] > 100)).sum()
        if hors_plage > 0:
            score -= 15
            problemes.append(f"{hors_plage} taux d'engagement hors plage")
    
    cols_essentielles_completes = all(col in df.columns and df[col].notna().all() 
                                     for col in ['influencer_name', 'followers', 'engagement_rate'])
    if not cols_essentielles_completes:
        score -= 25
        problemes.append("Colonnes essentielles incomplètes")
    
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        score -= 10
        problemes.append(f"{duplicates} doublons exacts")
    
    # Afficher le score
    print(f"\n📊 SCORE DE QUALITÉ: {score}/100")
    
    if score >= 90:
        print("✅ EXCELLENT - Données prêtes pour l'analyse")
    elif score >= 70:
        print("⚠️  BON - Quelques améliorations possibles")
    elif score >= 50:
        print("⚠️  MOYEN - Améliorations nécessaires")
    else:
        print("❌ FAIBLE - Nettoyage supplémentaire requis")
    
    if problemes:
        print("\nProblèmes identifiés:")
        for prob in problemes:
            print(f"  • {prob}")
    
    # 9. Recommandations
    print("\n" + "="*60)
    print("RECOMMANDATIONS")
    print("="*60)
    
    recommendations = []
    
    if 'avg_comments' in df.columns and df['avg_comments'].dtype == 'object':
        recommendations.append("Nettoyer la colonne 'avg_comments' (contient 'k', 'm')")
    
    empty_cols = [col for col in df.columns if df[col].notna().sum() == 0]
    if empty_cols:
        recommendations.append(f"Supprimer les colonnes vides: {', '.join(empty_cols)}")
    
    if 'category' in df.columns and (df['category'] == 'Unknown').any():
        recommendations.append("Corriger les catégories 'Unknown'")
    
    if recommendations:
        print("\nActions recommandées:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("\n✅ Aucune action recommandée - données de bonne qualité")
    
    return df, score

if __name__ == "__main__":
    df, score = verifier_qualite_donnees()
    
    # Option : Générer un rapport détaillé
    if score < 80:
        print("\n" + "="*60)
        print("RAPPORT DÉTAILLÉ POUR AMÉLIORATION")
        print("="*60)
        
        # Exporter les lignes problématiques
        if 'followers' in df.columns and df['followers'].dtype == 'object':
            problem_rows = df[df['followers'].astype(str).str.contains('[km]', case=False, na=False)]
            if len(problem_rows) > 0:
                print("\nLignes avec followers mal formatés:")
                print(problem_rows[['influencer_name', 'followers']].head())
        
        if 'engagement_rate' in df.columns:
            problem_rows = df[(df['engagement_rate'] < 0) | (df['engagement_rate'] > 100)]
            if len(problem_rows) > 0:
                print("\nLignes avec engagement_rate hors plage:")
                print(problem_rows[['influencer_name', 'engagement_rate']].head())