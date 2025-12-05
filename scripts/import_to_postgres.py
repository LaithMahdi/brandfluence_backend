# import_to_postgres.py
import pandas as pd
from sqlalchemy import create_engine, text
import logging
import os
import sys

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_postgres_connection():
    """Récupère les paramètres de connexion PostgreSQL"""
    
    # Configuration par défaut - À MODIFIER SELON VOTRE ENVIRONNEMENT
    config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'brandfluence',
        'user': 'postgres',  # Changez selon votre utilisateur
        'password': '0000',  # Changez selon votre mot de passe
        'schema': 'public'  # Ou un autre schéma si nécessaire
    }
    
    # Demander à l'utilisateur si les paramètres par défaut ne conviennent pas
    print("\n" + "="*60)
    print("CONFIGURATION POSTGRESQL")
    print("="*60)
    print(f"Configuration actuelle:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    change_config = input("\nVoulez-vous modifier la configuration ? (o/n): ").lower().strip()
    
    if change_config == 'o':
        print("\nLaissez vide pour conserver la valeur actuelle.")
        config['host'] = input(f"Hôte [{config['host']}]: ") or config['host']
        config['port'] = input(f"Port [{config['port']}]: ") or config['port']
        config['database'] = input(f"Base de données [{config['database']}]: ") or config['database']
        config['user'] = input(f"Utilisateur [{config['user']}]: ") or config['user']
        config['password'] = input(f"Mot de passe [{config['password']}]: ") or config['password']
        config['schema'] = input(f"Schéma [{config['schema']}]: ") or config['schema']
    
    # Créer l'URL de connexion
    connection_string = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    
    return connection_string, config

def test_connection(engine):
    """Teste la connexion à PostgreSQL"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            logger.info(f" Connexion PostgreSQL établie: {version}")
            return True
    except Exception as e:
        logger.error(f" Erreur de connexion à PostgreSQL: {e}")
        logger.info("\n VÉRIFIEZ QUE:")
        logger.info("   1. PostgreSQL est installé et fonctionne")
        logger.info("   2. La base 'brandfluence' existe")
        logger.info("   3. Les identifiants sont corrects")
        return False

def create_tables(engine, schema='public'):
    """Crée les tables dans PostgreSQL"""
    
    logger.info("Création des tables dans PostgreSQL...")
    
    # SQL pour créer les tables
    sql_commands = [
        # Table des catégories
        f"""
        CREATE TABLE IF NOT EXISTS {schema}.categories (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Table des pays
        f"""
        CREATE TABLE IF NOT EXISTS {schema}.countries (
            country_id SERIAL PRIMARY KEY,
            country_name VARCHAR(100) UNIQUE NOT NULL,
            region VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Table principale des influenceurs
        f"""
        CREATE TABLE IF NOT EXISTS {schema}.influenceurs (
            influencer_id SERIAL PRIMARY KEY,
            influencer_name VARCHAR(255) NOT NULL,
            username VARCHAR(100),
            category_id INTEGER REFERENCES {schema}.categories(category_id),
            followers BIGINT NOT NULL,
            posts INTEGER,
            avg_likes INTEGER,
            avg_comments INTEGER,
            engagement_rate DECIMAL(5,2),
            country_id INTEGER REFERENCES {schema}.countries(country_id),
            influence_score DECIMAL(5,2),
            rank_position INTEGER,
            channel_info TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Table des statistiques (optionnelle)
        f"""
        CREATE TABLE IF NOT EXISTS {schema}.statistiques (
            stat_id SERIAL PRIMARY KEY,
            influencer_id INTEGER REFERENCES {schema}.influenceurs(influencer_id),
            date_stat DATE DEFAULT CURRENT_DATE,
            nouveaux_followers INTEGER,
            nouveaux_likes INTEGER,
            nouveaux_comments INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    # Création des indexes
    index_commands = [
        f"CREATE INDEX IF NOT EXISTS idx_influenceurs_followers ON {schema}.influenceurs(followers);",
        f"CREATE INDEX IF NOT EXISTS idx_influenceurs_category ON {schema}.influenceurs(category_id);",
        f"CREATE INDEX IF NOT EXISTS idx_influenceurs_country ON {schema}.influenceurs(country_id);",
        f"CREATE INDEX IF NOT EXISTS idx_influenceurs_engagement ON {schema}.influenceurs(engagement_rate);",
        f"CREATE INDEX IF NOT EXISTS idx_influenceurs_name ON {schema}.influenceurs(influencer_name);"
    ]
    
    try:
        with engine.connect() as conn:
            # Exécuter les commandes de création de tables
            for sql in sql_commands:
                conn.execute(text(sql))
            conn.commit()
            
            # Exécuter les commandes de création d'indexes
            for sql in index_commands:
                try:
                    conn.execute(text(sql))
                except Exception as e:
                    logger.warning(f"Index peut déjà exister: {e}")
            conn.commit()
            
            logger.info("✅ Tables créées avec succès")
            return True
            
    except Exception as e:
        logger.error(f" Erreur lors de la création des tables: {e}")
        return False

def import_data_to_postgres(clean_df, engine, schema='public'):
    """Importe les données dans PostgreSQL avec structure normalisée"""
    
    logger.info("Début de l'importation des données...")
    
    try:
        with engine.connect() as conn:
            # 1. Nettoyer et préparer les données de référence
            # Catégories uniques
            categories = clean_df['category'].dropna().unique()
            categories_df = pd.DataFrame({'category_name': categories})
            
            # Pays uniques
            countries = clean_df['country'].dropna().unique()
            countries_df = pd.DataFrame({'country_name': countries})
            
            # 2. Importer les catégories (en ignorant les doublons)
            logger.info("Importation des catégories...")
            categories_df.to_sql('categories', conn, schema=schema, if_exists='append', index=False)
            
            # Récupérer le mapping catégorie -> ID
            result = conn.execute(text(f"SELECT category_id, category_name FROM {schema}.categories"))
            category_map = {row[1]: row[0] for row in result.fetchall()}
            logger.info(f" {len(category_map)} catégories disponibles")
            
            # 3. Importer les pays
            logger.info("Importation des pays...")
            countries_df.to_sql('countries', conn, schema=schema, if_exists='append', index=False)
            
            # Récupérer le mapping pays -> ID
            result = conn.execute(text(f"SELECT country_id, country_name FROM {schema}.countries"))
            country_map = {row[1]: row[0] for row in result.fetchall()}
            logger.info(f" {len(country_map)} pays disponibles")
            
            # 4. Préparer les données des influenceurs
            logger.info("Préparation des données des influenceurs...")
            influenceurs_df = clean_df.copy()
            
            # Ajouter les IDs des références
            influenceurs_df['category_id'] = influenceurs_df['category'].map(category_map)
            influenceurs_df['country_id'] = influenceurs_df['country'].map(country_map)
            
            # Vérifier les valeurs manquantes
            missing_category = influenceurs_df['category_id'].isna().sum()
            missing_country = influenceurs_df['country_id'].isna().sum()
            
            if missing_category > 0:
                logger.warning(f" {missing_category} influenceurs sans catégorie correspondante")
                # Remplacer par NULL
                influenceurs_df['category_id'] = influenceurs_df['category_id'].where(influenceurs_df['category_id'].notna(), None)
            
            if missing_country > 0:
                logger.warning(f" {missing_country} influenceurs sans pays correspondant")
                # Remplacer par NULL
                influenceurs_df['country_id'] = influenceurs_df['country_id'].where(influenceurs_df['country_id'].notna(), None)
            
            # Sélectionner et renommer les colonnes
            columns_mapping = {
                'influencer_name': 'influencer_name',
                'username': 'username',
                'category_id': 'category_id',
                'followers': 'followers',
                'posts': 'posts',
                'avg_likes': 'avg_likes',
                'avg_comments': 'avg_comments',
                'engagement_rate': 'engagement_rate',
                'country_id': 'country_id',
                'influence_score': 'influence_score',
                'rank': 'rank_position',
                'Channel Info': 'channel_info'
            }
            
            influenceurs_final = influenceurs_df[list(columns_mapping.keys())].rename(columns=columns_mapping)
            
            # 5. Importer les influenceurs
            logger.info("Importation des influenceurs...")
            influenceurs_final.to_sql('influenceurs', conn, schema=schema, if_exists='append', index=False)
            
            # 6. Statistiques finales
            result = conn.execute(text(f"""
                SELECT 
                    COUNT(*) as total_influenceurs,
                    AVG(followers) as avg_followers,
                    AVG(engagement_rate) as avg_engagement,
                    COUNT(DISTINCT category_id) as categories_count,
                    COUNT(DISTINCT country_id) as countries_count
                FROM {schema}.influenceurs
            """))
            stats = result.fetchone()
            
            logger.info("\n STATISTIQUES DE L'IMPORTATION:")
            logger.info(f"  Total influenceurs: {stats[0]:,}")
            logger.info(f"  Followers moyens: {stats[1]:,.0f}")
            logger.info(f"  Engagement moyen: {stats[2]:.2f}%")
            logger.info(f"  Catégories différentes: {stats[3]}")
            logger.info(f"  Pays différents: {stats[4]}")
            
            # Afficher le top 5
            result = conn.execute(text(f"""
                SELECT i.influencer_name, i.followers, c.country_name, cat.category_name, i.engagement_rate
                FROM {schema}.influenceurs i
                LEFT JOIN {schema}.countries c ON i.country_id = c.country_id
                LEFT JOIN {schema}.categories cat ON i.category_id = cat.category_id
                ORDER BY i.followers DESC
                LIMIT 5
            """))
            top_influencers = result.fetchall()
            
            logger.info("\n🏆 TOP 5 INFLUENCEURS:")
            for inf in top_influencers:
                logger.info(f"   {inf[0]}")
                logger.info(f"     {inf[1]:,} followers")
                logger.info(f"     {inf[2]} | 🏷️ {inf[3]} | ⭐ {inf[4]:.1f}% engagement")
                logger.info("")
            
            return True
            
    except Exception as e:
        logger.error(f" Erreur lors de l'importation: {e}")
        return False

def import_simple_table(clean_df, engine, schema='public'):
    """Importe les données dans une table simple (alternative)"""
    
    logger.info("Importation dans une table simple...")
    
    try:
        with engine.connect() as conn:
            # Renommer les colonnes pour PostgreSQL
            df_for_import = clean_df.copy()
            
            # S'assurer que les noms de colonnes sont valides pour PostgreSQL
            df_for_import.columns = [col.lower().replace(' ', '_').replace('.', '_') for col in df_for_import.columns]
            
            # Importer
            df_for_import.to_sql('influenceurs_simple', conn, schema=schema, if_exists='replace', index=False)
            
            # Vérifier
            result = conn.execute(text(f"SELECT COUNT(*) FROM {schema}.influenceurs_simple"))
            count = result.fetchone()[0]
            
            logger.info(f" {count} influenceurs importés dans la table 'influenceurs_simple'")
            return True
            
    except Exception as e:
        logger.error(f" Erreur lors de l'importation simple: {e}")
        return False

def main():
    """Fonction principale"""
    
    # 1. Vérifier que le fichier nettoyé existe
    csv_file = 'influenceurs_clean.csv'
    
    if not os.path.exists(csv_file):
        logger.error(f" Fichier {csv_file} non trouvé")
        logger.info(" Exécutez d'abord: python clean_and_import.py")
        return
    
    # 2. Charger les données
    logger.info(f" Chargement du fichier {csv_file}...")
    try:
        clean_df = pd.read_csv(csv_file)
        logger.info(f" Fichier chargé: {len(clean_df)} lignes, {len(clean_df.columns)} colonnes")
    except Exception as e:
        logger.error(f" Erreur de chargement: {e}")
        return
    
    # 3. Configuration PostgreSQL
    connection_string, config = get_postgres_connection()
    
    # 4. Créer le moteur SQLAlchemy
    try:
        engine = create_engine(connection_string)
        logger.info(f"🔗 Connexion à PostgreSQL: {config['database']}@{config['host']}:{config['port']}")
    except Exception as e:
        logger.error(f" Erreur de création du moteur: {e}")
        return
    
    # 5. Tester la connexion
    if not test_connection(engine):
        return
    
    # 6. Menu d'importation
    print("\n" + "="*60)
    print("OPTIONS D'IMPORTATION")
    print("="*60)
    print("1. Structure normalisée (recommandé)")
    print("   - Tables séparées: categories, countries, influenceurs")
    print("   - Relations avec clés étrangères")
    print("   - Meilleure pour les requêtes complexes")
    print()
    print("2. Table simple")
    print("   - Une seule table 'influenceurs_simple'")
    print("   - Plus rapide, moins de relations")
    print("   - Parfait pour des requêtes simples")
    print()
    print("3. Les deux")
    print("="*60)
    
    while True:
        choice = input("\nChoisissez une option (1-3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print(" Choix invalide. Veuillez entrer 1, 2 ou 3.")
    
    # 7. Exécuter l'importation selon le choix
    success = False
    
    if choice == '1':
        # Créer les tables
        if create_tables(engine, config['schema']):
            # Importer les données
            success = import_data_to_postgres(clean_df, engine, config['schema'])
    
    elif choice == '2':
        success = import_simple_table(clean_df, engine, config['schema'])
    
    elif choice == '3':
        success1 = create_tables(engine, config['schema']) and import_data_to_postgres(clean_df, engine, config['schema'])
        success2 = import_simple_table(clean_df, engine, config['schema'])
        success = success1 and success2
    
    # 8. Afficher les instructions de connexion
    if success:
        print("\n" + "="*60)
        print(" IMPORTATION RÉUSSIE !")
        print("="*60)
        
        print(f"\n BASE DE DONNÉES: {config['database']}")
        print(f" HÔTE: {config['host']}:{config['port']}")
        print(f" UTILISATEUR: {config['user']}")
        
        if choice in ['1', '3']:
            print("\n TABLES CRÉÉES (structure normalisée):")
            print("   • categories")
            print("   • countries")
            print("   • influenceurs")
            print("   • statistiques (vide)")
        
        if choice in ['2', '3']:
            print("\n TABLE CRÉÉE (structure simple):")
            print("   • influenceurs_simple")
        
        print("\n POUR SE CONNECTER AVEC PSQL:")
        print(f"   psql -h {config['host']} -p {config['port']} -U {config['user']} -d {config['database']}")
        
        print("\n EXEMPLES DE REQUÊTES SQL:")
        print("   -- Compter les influenceurs")
        print("   SELECT COUNT(*) FROM influenceurs;")
        print()
        print("   -- Top 10 par followers")
        print("   SELECT influencer_name, followers, country_name, category_name")
        print("   FROM influenceurs i")
        print("   JOIN countries c ON i.country_id = c.country_id")
        print("   JOIN categories cat ON i.category_id = cat.category_id")
        print("   ORDER BY followers DESC LIMIT 10;")
        print()
        print("   -- Statistiques par catégorie")
        print("   SELECT category_name, COUNT(*), AVG(followers), AVG(engagement_rate)")
        print("   FROM influenceurs i")
        print("   JOIN categories c ON i.category_id = c.category_id")
        print("   GROUP BY category_name ORDER BY COUNT(*) DESC;")
        
        print("\n POUR UTILISER AVEC PYTHON:")
        print("   from sqlalchemy import create_engine")
        print("   import pandas as pd")
        print(f"   engine = create_engine('postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}')")
        print("   df = pd.read_sql('SELECT * FROM influenceurs', engine)")
        
        print("\n Vos données sont maintenant dans PostgreSQL et prêtes à être utilisées !")

if __name__ == "__main__":
    main()