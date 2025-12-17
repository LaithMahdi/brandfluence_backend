
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
import sys
import os


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def clean_followers(value):
    """Convertit '1.2m' en 1200000, '540k' en 540000"""
    try:
        if pd.isna(value):
            return None
        
        value_str = str(value).strip().lower()
        
       
        value_str = value_str.replace(',', '').replace(' ', '')
        
       
        if 'k' in value_str:
            return int(float(value_str.replace('k', '')) * 1000)
        elif 'm' in value_str:
            return int(float(value_str.replace('m', '')) * 1000000)
        elif 'b' in value_str:
            return int(float(value_str.replace('b', '')) * 1000000000)
        else:
            return int(float(value_str))
    except:
        return None

def clean_engagement(value):
    """Convertit '8.5%' en 8.5"""
    try:
        if pd.isna(value):
            return None
        
        value_str = str(value).strip()
        value_str = value_str.replace('%', '')
        result = float(value_str)
        
       
        if 0 <= result <= 100:
            return round(result, 2)
        return None
    except:
        return None

def clean_category(cat):
    """Uniformise les catégories"""
    if pd.isna(cat):
        return 'Unknown'
    
    cat = str(cat).strip().title()
    
   
    mapping = {
        'Fashion': 'Fashion',
        'Tech': 'Tech',
        'Technology': 'Tech',
        'Lifestyle': 'Lifestyle',
        'Food': 'Food',
        'Travel': 'Travel',
        'Beauty': 'Beauty',
        'Fitness': 'Fitness',
        'Music': 'Music',
        'Gaming': 'Gaming',
        'Sports': 'Sports',
        'Entertainment': 'Entertainment',
        'Education': 'Education',
        'Business': 'Business'
    }
    
    return mapping.get(cat, cat)

def extract_name_from_channel(channel_info):
    """Essaye d'extraire un nom depuis Channel Info"""
    if pd.isna(channel_info):
        return None
    
    channel_str = str(channel_info)
    
  
    suffixes = [
        '_vlog', '_tv', '_world', '_zone', '_lab', '_official', 
        '_vlogs', '_channel', '_show', '_network', '_media', '_hd'
    ]
    
   
    channel_lower = channel_str.lower()
    
   
    for suffix in suffixes:
        if channel_lower.endswith(suffix):
          
            channel_str = channel_str[:len(channel_str)-len(suffix)]
            break
    
   
    channel_str = channel_str.replace('_', ' ')
    channel_str = channel_str.replace('-', ' ')
    
 
    while channel_str and channel_str[-1].isdigit():
        channel_str = channel_str[:-1]
    

    channel_str = channel_str.strip().title()
    
  
    if len(channel_str) < 2 or channel_str.lower() in ['', 'style', 'music', 'city', 'shop', 'eco', 'daily']:
        return None
    
    return channel_str

def clean_numeric_k(value):
    """Convertit '3.4k' en 3400, '21.4k' en 21400, etc."""
    try:
        if pd.isna(value):
            return None
        
        value_str = str(value).strip().lower()
        
      
        value_str = value_str.replace(',', '').replace(' ', '')
        
     
        if 'k' in value_str:
            return int(float(value_str.replace('k', '')) * 1000)
        elif 'm' in value_str:
            return int(float(value_str.replace('m', '')) * 1000000)
        elif 'b' in value_str:
            return int(float(value_str.replace('b', '')) * 1000000000)
        else:
          
            return int(float(value_str))
    except:
        return None

def main():
 
    logger.info("Recherche du fichier CSV...")
    
   
    possible_paths = [
        'Top_Influencers_Full_1500.csv',
        '../Top_Influencers_Full_1500.csv',
        './Top_Influencers_Full_1500.csv'
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            logger.info(f"Fichier trouvé à: {path}")
            break
    
    if csv_path is None:
        logger.error("Fichier CSV non trouvé.")
        sys.exit(1)
    
   
    try:
        df = pd.read_csv(csv_path)
        logger.info(f"Fichier chargé: {len(df)} lignes, {len(df.columns)} colonnes")
        print(f"Colonnes trouvées: {list(df.columns)}")
        print(f"\nAperçu des données:")
        print(df.head())
    except Exception as e:
        logger.error(f"Erreur de chargement: {e}")
        sys.exit(1)
    
  
    print("\n" + "="*60)
    print("ANALYSE DES COLONNES")
    print("="*60)
    

    print("\nTypes de données:")
    print(df.dtypes)
    

    important_cols = ['Followers', 'Engagement Rate (%)', '60-Day Eng Rate', 'Category', 'Influencer Name', 'Username']
    for col in important_cols:
        if col in df.columns:
            print(f"\nColonne '{col}':")
            print(f"  Valeurs uniques (premières 10): {df[col].dropna().unique()[:10]}")
            print(f"  Type: {df[col].dtype}")
            print(f"  Non-null: {df[col].notna().sum()}/{len(df)}")
    
   
    col_mapping = {
        'Influencer Name': 'influencer_name',
        'Followers': 'followers',
        'Engagement Rate (%)': 'engagement_rate',
        '60-Day Eng Rate': 'engagement_rate_60day',
        'Category': 'category',
        'Posts': 'posts',
        'Country Or Region': 'country',
        'Country': 'country_alt',
        'Avg. Likes': 'avg_likes',
        'Avg Comments': 'avg_comments',
        'Influence Score': 'influence_score',
        'Rank': 'rank',
        'Username': 'username'
    }
    
  
    df_renamed = df.copy()
    for old_col, new_col in col_mapping.items():
        if old_col in df_renamed.columns:
            df_renamed.rename(columns={old_col: new_col}, inplace=True)
            logger.info(f"Colonne renommée: '{old_col}' -> '{new_col}'")
    

    if 'country' in df_renamed.columns and 'country_alt' in df_renamed.columns:
       
        df_renamed['country_final'] = df_renamed['country'].combine_first(df_renamed['country_alt'])
        logger.info("Colonnes 'country' et 'country_alt' fusionnées en 'country_final'")
    

    logger.info("\nNettoyage des données...")
    
   
    if 'followers' in df_renamed.columns:
        logger.info(f"Avant nettoyage - Exemple de followers: {df_renamed['followers'].head(3).tolist()}")
        df_renamed['followers_clean'] = df_renamed['followers'].apply(clean_followers)
        logger.info(f"Followers nettoyés: {df_renamed['followers_clean'].notna().sum()}/{len(df_renamed)}")
        logger.info(f"Après nettoyage - Exemple: {df_renamed['followers_clean'].head(3).tolist()}")
    
   
    for col in ['posts', 'avg_likes', 'avg_comments']:
        if col in df_renamed.columns:
            logger.info(f"\n{col} - Avant nettoyage: {df_renamed[col].head(3).tolist()}")
            df_renamed[f'{col}_clean'] = df_renamed[col].apply(clean_numeric_k)
            logger.info(f"{col} nettoyés: {df_renamed[f'{col}_clean'].notna().sum()}/{len(df_renamed)}")
            logger.info(f"Après nettoyage - Exemple: {df_renamed[f'{col}_clean'].head(3).tolist()}")
    
  
    engagement_col = None
    if 'engagement_rate' in df_renamed.columns:
        logger.info(f"\nEngagement Rate - Non-null values: {df_renamed['engagement_rate'].notna().sum()}")
        engagement_col = 'engagement_rate'
    
  
    if not engagement_col or df_renamed['engagement_rate'].notna().sum() < 500:
        if 'engagement_rate_60day' in df_renamed.columns:
            logger.info(f"\nUtilisation de 60-Day Eng Rate - Non-null: {df_renamed['engagement_rate_60day'].notna().sum()}")
            engagement_col = 'engagement_rate_60day'
    
    if engagement_col:
        df_renamed['engagement_rate_clean'] = df_renamed[engagement_col].apply(clean_engagement)
        logger.info(f"Engagement Rate nettoyé: {df_renamed['engagement_rate_clean'].notna().sum()}/{len(df_renamed)}")
    
  
    if 'category' in df_renamed.columns:
        logger.info(f"\nCatégories - Avant nettoyage: {df_renamed['category'].dropna().unique()[:10]}")
        logger.info(f"Valeurs nulles dans category: {df_renamed['category'].isna().sum()}")
        df_renamed['category_clean'] = df_renamed['category'].apply(clean_category)
        logger.info(f"Catégories nettoyées - Exemples: {df_renamed['category_clean'].dropna().unique()[:10]}")
    
  
    logger.info("\nCréation du DataFrame final...")
    
  
    columns_to_keep = []
    
  
    if 'influencer_name' in df_renamed.columns:
        columns_to_keep.append('influencer_name')
    
    if 'category_clean' in df_renamed.columns:
        columns_to_keep.append('category_clean')
    elif 'category' in df_renamed.columns:
        columns_to_keep.append('category')
    
    if 'followers_clean' in df_renamed.columns:
        columns_to_keep.append('followers_clean')
    elif 'followers' in df_renamed.columns:
        columns_to_keep.append('followers')
    
  
    for col in ['posts', 'avg_likes', 'avg_comments']:
        if f'{col}_clean' in df_renamed.columns:
            columns_to_keep.append(f'{col}_clean')
        elif col in df_renamed.columns:
            columns_to_keep.append(col)
    
    if 'engagement_rate_clean' in df_renamed.columns:
        columns_to_keep.append('engagement_rate_clean')
    elif 'engagement_rate' in df_renamed.columns:
        columns_to_keep.append('engagement_rate')
    elif 'engagement_rate_60day' in df_renamed.columns:
        columns_to_keep.append('engagement_rate_60day')
    
 
    optional_cols_order = [
        'country_final', 
        'influence_score', 
        'rank', 
        'username',
        'Channel Info'
    ]
    
    for col in optional_cols_order:
        if col in df_renamed.columns and col not in columns_to_keep:
            columns_to_keep.append(col)
    
   
    clean_df = df_renamed[columns_to_keep].copy()
    
   
    rename_dict = {
        'category_clean': 'category',
        'followers_clean': 'followers',
        'engagement_rate_clean': 'engagement_rate',
        'country_final': 'country',
        'posts_clean': 'posts',
        'avg_likes_clean': 'avg_likes',
        'avg_comments_clean': 'avg_comments'
    }
    
    for old_name, new_name in rename_dict.items():
        if old_name in clean_df.columns:
            clean_df.rename(columns={old_name: new_name}, inplace=True)
    
    logger.info("\nTraitement des valeurs manquantes...")
    
    before = len(clean_df)
    print(f"\nAVANT traitement des valeurs manquantes: {before} lignes")
    
    print("\nValeurs manquantes par colonne:")
    missing_data = clean_df.isnull().sum()
    for col, count in missing_data.items():
        if count > 0:
            percentage = (count / len(clean_df)) * 100
            print(f"  {col}: {count} manquants ({percentage:.1f}%)")
    
 
    
  
    if 'influencer_name' in clean_df.columns:
        missing_names = clean_df['influencer_name'].isna().sum()
        if missing_names > 0:
         
            if 'username' in clean_df.columns:
                mask = clean_df['influencer_name'].isna() & clean_df['username'].notna()
                clean_df.loc[mask, 'influencer_name'] = clean_df.loc[mask, 'username']
                logger.info(f"Noms remplacés par username: {mask.sum()}")
            
           
            if 'Channel Info' in clean_df.columns:
                for idx, row in clean_df[clean_df['influencer_name'].isna()].iterrows():
                    channel_info = row['Channel Info']
                    extracted_name = extract_name_from_channel(channel_info)
                    if extracted_name:
                        clean_df.at[idx, 'influencer_name'] = extracted_name
                
                extracted_count = clean_df['influencer_name'].notna().sum() - (len(clean_df) - missing_names)
                logger.info(f"Noms extraits depuis Channel Info: {extracted_count}")
            
           
            remaining = clean_df['influencer_name'].isna().sum()
            if remaining > 0:
                clean_df.loc[clean_df['influencer_name'].isna(), 'influencer_name'] = 'Influenceur'
                logger.info(f"Noms inconnus marqués comme 'Influenceur': {remaining}")
    
 
    if 'followers' in clean_df.columns and 'category' in clean_df.columns:
        missing_followers = clean_df['followers'].isna().sum()
        if missing_followers > 0:
          
            median_by_category = clean_df.groupby('category')['followers'].median()
            
            for idx, row in clean_df[clean_df['followers'].isna()].iterrows():
                category = row['category']
                if category in median_by_category and not pd.isna(median_by_category[category]):
                    clean_df.at[idx, 'followers'] = median_by_category[category]
                else:
                    
                    global_median = clean_df['followers'].median()
                    if not pd.isna(global_median):
                        clean_df.at[idx, 'followers'] = global_median
            
            logger.info(f"Followers manquants remplis: {missing_followers}")
    
    
    if 'engagement_rate' in clean_df.columns and 'category' in clean_df.columns:
        missing_engagement = clean_df['engagement_rate'].isna().sum()
        if missing_engagement > 0:
          
            mean_by_category = clean_df.groupby('category')['engagement_rate'].mean()
            
            for idx, row in clean_df[clean_df['engagement_rate'].isna()].iterrows():
                category = row['category']
                if category in mean_by_category and not pd.isna(mean_by_category[category]):
                    clean_df.at[idx, 'engagement_rate'] = mean_by_category[category]
                else:
                  
                    global_mean = clean_df['engagement_rate'].mean()
                    if not pd.isna(global_mean):
                        clean_df.at[idx, 'engagement_rate'] = global_mean
            
            logger.info(f"Engagement rates manquants remplis: {missing_engagement}")
    
   
    if 'category' in clean_df.columns:
        missing_category = clean_df['category'].isna().sum()
        if missing_category > 0:
          
            clean_df.loc[clean_df['category'].isna(), 'category'] = 'General'
            logger.info(f"Catégories manquantes marquées comme 'General': {missing_category}")
    
   
    if 'country' in clean_df.columns:
        missing_country = clean_df['country'].isna().sum()
        if missing_country > 0:
            clean_df.loc[clean_df['country'].isna(), 'country'] = 'Unknown'
            logger.info(f"Pays inconnus marqués: {missing_country}")
    
   
    numeric_cols_to_fill = ['posts', 'avg_likes', 'avg_comments', 'influence_score', 'rank']
    for col in numeric_cols_to_fill:
        if col in clean_df.columns and clean_df[col].isna().sum() > 0:
            median_val = clean_df[col].median()
            if not pd.isna(median_val):
                clean_df.loc[clean_df[col].isna(), col] = median_val
                logger.info(f"{col}: valeurs manquantes remplacées par médiane {median_val}")
    
    
    text_cols = clean_df.select_dtypes(include=['object']).columns
    for col in text_cols:
        if col in clean_df.columns and col not in ['influencer_name', 'category', 'country'] and clean_df[col].isna().sum() > 0:
            clean_df.loc[clean_df[col].isna(), col] = 'Unknown'
    
    after = len(clean_df)
    print(f"\nAPRÈS traitement des valeurs manquantes: {after} lignes")
    print(f"Toutes les {before} lignes sont conservées!")
    
    
    remaining_missing = clean_df.isnull().sum().sum()
    if remaining_missing == 0:
        logger.info("✓ Plus aucune valeur manquante dans le dataset!")
    else:
        logger.warning(f"Encore {remaining_missing} valeurs manquantes")
        print("\nValeurs manquantes restantes:")
        print(clean_df.isnull().sum())
    
   
    print("\n" + "="*60)
    print("APERÇU FINAL DES DONNÉES NETTOYÉES")
    print("="*60)
    print(clean_df.head(10))
    print(f"\nShape: {clean_df.shape}")
    
  
    print(f"\nColonnes finales: {list(clean_df.columns)}")
    print(f"Nombre de colonnes: {len(clean_df.columns)}")
    
   
    if len(clean_df.columns) != len(set(clean_df.columns)):
        print("ATTENTION: Il y a des colonnes en double!")
        clean_df = clean_df.loc[:, ~clean_df.columns.duplicated()]
        print("Doublons supprimés.")
        print(f"Nouvelles colonnes: {list(clean_df.columns)}")
    
   
    print("\n" + "="*60)
    print("STATISTIQUES DESCRIPTIVES")
    print("="*60)
    
    if 'followers' in clean_df.columns:
        print(f"\nFollowers:")
        print(f"  Min: {clean_df['followers'].min():,}")
        print(f"  Max: {clean_df['followers'].max():,}")
        print(f"  Moyenne: {clean_df['followers'].mean():,.0f}")
        print(f"  Médiane: {clean_df['followers'].median():,.0f}")
    
    if 'engagement_rate' in clean_df.columns:
        print(f"\nEngagement Rate (%):")
        print(f"  Min: {clean_df['engagement_rate'].min():.2f}")
        print(f"  Max: {clean_df['engagement_rate'].max():.2f}")
        print(f"  Moyenne: {clean_df['engagement_rate'].mean():.2f}")
        print(f"  Médiane: {clean_df['engagement_rate'].median():.2f}")
        print(f"  Non-null: {clean_df['engagement_rate'].notna().sum()}")
    
    if 'category' in clean_df.columns:
        print(f"\nDistribution des catégories:")
        cat_counts = clean_df['category'].value_counts()
        print(cat_counts)
        print(f"\nTotal catégories: {len(cat_counts)}")
    
    
    for col in ['posts', 'avg_likes', 'avg_comments']:
        if col in clean_df.columns and clean_df[col].dtype in [np.int64, np.float64]:
            print(f"\n{col}:")
            print(f"  Min: {clean_df[col].min():,}")
            print(f"  Max: {clean_df[col].max():,}")
            print(f"  Moyenne: {clean_df[col].mean():,.0f}")
            print(f"  Médiane: {clean_df[col].median():,.0f}")
    
   
    clean_csv_path = 'influenceurs_clean.csv'
    clean_df.to_csv(clean_csv_path, index=False, encoding='utf-8')
    logger.info(f"\nDonnées nettoyées sauvegardées dans: {clean_csv_path}")
    
  
    try:
        json_path = 'influenceurs_clean_sample.json'
        clean_df.head(50).to_json(json_path, orient='records', indent=2, force_ascii=False)
        logger.info(f"Échantillon sauvegardé dans: {json_path}")
    except Exception as e:
        logger.warning(f"Impossible de créer le fichier JSON: {e}")
    
    print("\n" + "="*60)
    print("RÉSUMÉ DU NETTOYAGE")
    print("="*60)
    print(f"Lignes originales: {len(df)}")
    print(f"Lignes finales: {len(clean_df)}")
    print(f"Colonnes nettoyées: {len(clean_df.columns)}")
    
   
    if len(df) > 0:
        conservation_rate = len(clean_df) / len(df) * 100
        print(f"\nTaux de conservation: {conservation_rate:.1f}%")
        print(f"✓ TOUTES les lignes ont été conservées grâce au remplissage des valeurs manquantes!")
    

    print(f"\nColonnes disponibles ({len(clean_df.columns)}):")
    for i, col in enumerate(clean_df.columns, 1):
        non_null = clean_df[col].notna().sum()
        dtype = str(clean_df[col].dtype)
        unique = clean_df[col].nunique()
      
        print(f"  {i:2d}. {col:20} (Type: {dtype}): {non_null:4d} non-null, {unique:4d} valeurs uniques")
    
  
    print("\n" + "="*60)
    print("EXEMPLE DES NOMS D'INFLUENCEURS")
    print("="*60)
    if 'influencer_name' in clean_df.columns:
        sample_names = clean_df['influencer_name'].head(20).tolist()
        for i, name in enumerate(sample_names, 1):
            print(f"{i:2d}. {name}")
    
   
    print("\n" + "="*60)
    print("QUALITÉ DES DONNÉES FINALES")
    print("="*60)
    
   
    if 'influencer_name' in clean_df.columns:
        real_names = clean_df[clean_df['influencer_name'] != 'Influenceur']['influencer_name'].count()
        percentage_real_names = (real_names / len(clean_df)) * 100
        print(f"✓ Noms réels: {real_names}/{len(clean_df)} ({percentage_real_names:.1f}%)")
    
   
    if 'category' in clean_df.columns:
        known_categories = clean_df[clean_df['category'] != 'General']['category'].count()
        percentage_known_cat = (known_categories / len(clean_df)) * 100
        print(f"✓ Catégories connues: {known_categories}/{len(clean_df)} ({percentage_known_cat:.1f}%)")
    
  
    if 'country' in clean_df.columns:
        known_countries = clean_df[clean_df['country'] != 'Unknown']['country'].count()
        percentage_known_countries = (known_countries / len(clean_df)) * 100
        print(f"✓ Pays connus: {known_countries}/{len(clean_df)} ({percentage_known_countries:.1f}%)")
    
    print(f"\n Fichier CSV nettoyé créé: {clean_csv_path}")
    print(f" Échantillon JSON créé: {json_path if 'json_path' in locals() else 'influenceurs_clean_sample.json'}")
    print(" Nettoyage terminé avec succès!")
    
    return clean_df

if __name__ == "__main__":
    clean_data = main()