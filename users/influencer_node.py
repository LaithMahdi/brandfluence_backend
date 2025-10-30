import graphene
from graphene_django import DjangoObjectType
from .influencer_models import (
    Influencer, ReseauSocial, Collaboration, 
    PortfolioMedia, OffreCollaboration, StatistiquesGlobales
)
from category.category_node import CategoryNode


class DisponibiliteEnum(graphene.Enum):
    """Enum for collaboration availability"""
    DISPONIBLE = 'disponible'
    OCCUPE = 'occupe'
    PARTIELLEMENT_DISPONIBLE = 'partiellement_disponible'


class PlateformeEnum(graphene.Enum):
    """Enum for social media platforms"""
    INSTAGRAM = 'Instagram'
    TIKTOK = 'TikTok'
    YOUTUBE = 'YouTube'
    FACEBOOK = 'Facebook'
    TWITTER = 'Twitter'
    LINKEDIN = 'LinkedIn'
    SNAPCHAT = 'Snapchat'


class FrequencePublicationEnum(graphene.Enum):
    """Enum for publication frequency"""
    QUOTIDIENNE = 'quotidienne'
    HEBDOMADAIRE = 'hebdomadaire'
    BI_HEBDOMADAIRE = 'bi_hebdomadaire'
    MENSUELLE = 'mensuelle'


class TypeCollaborationEnum(graphene.Enum):
    """Enum for collaboration type"""
    PLACEMENT_PRODUIT = 'placement_produit'
    STORY = 'story'
    POST = 'post'
    VIDEO = 'video'
    REEL = 'reel'
    LIVE = 'live'
    AMBASSADEUR = 'ambassadeur'


class ReseauSocialNode(DjangoObjectType):
    """GraphQL Node for ReseauSocial model"""
    plateforme = graphene.Field(PlateformeEnum)
    frequence_publication = graphene.Field(FrequencePublicationEnum)
    
    class Meta:
        model = ReseauSocial
        fields = (
            'id', 'plateforme', 'url_profil', 'nombre_abonnes', 
            'taux_engagement', 'moyenne_vues', 'moyenne_likes',
            'moyenne_commentaires', 'frequence_publication',
            'created_at', 'updated_at'
        )
        interfaces = (graphene.relay.Node,)


class CollaborationNode(DjangoObjectType):
    """GraphQL Node for Collaboration model"""
    
    class Meta:
        model = Collaboration
        fields = (
            'id', 'nom_marque', 'campagne', 'periode', 
            'resultats', 'lien_publication',
            'created_at', 'updated_at'
        )
        interfaces = (graphene.relay.Node,)


class PortfolioMediaNode(DjangoObjectType):
    """GraphQL Node for PortfolioMedia model"""
    
    class Meta:
        model = PortfolioMedia
        fields = (
            'id', 'image_url', 'titre', 'description', 
            'date_creation', 'created_at', 'updated_at'
        )
        interfaces = (graphene.relay.Node,)


class OffreCollaborationNode(DjangoObjectType):
    """GraphQL Node for OffreCollaboration model"""
    type_collaboration = graphene.Field(TypeCollaborationEnum)
    
    class Meta:
        model = OffreCollaboration
        fields = (
            'id', 'type_collaboration', 'tarif_minimum', 
            'tarif_maximum', 'conditions',
            'created_at', 'updated_at'
        )
        interfaces = (graphene.relay.Node,)


class StatistiquesGlobalesNode(DjangoObjectType):
    """GraphQL Node for StatistiquesGlobales model"""
    
    class Meta:
        model = StatistiquesGlobales
        fields = (
            'id', 'followers_totaux', 'engagement_moyen_global',
            'croissance_mensuelle', 'mois', 'created_at'
        )
        interfaces = (graphene.relay.Node,)


class StatistiquesGlobalesType(graphene.ObjectType):
    """Type for current global statistics"""
    followers_totaux = graphene.Int()
    engagement_moyen_global = graphene.Float()
    croissance_mensuelle = graphene.Float()


class InfluencerNode(DjangoObjectType):
    """GraphQL Node for Influencer model"""
    disponibilite_collaboration = graphene.Field(DisponibiliteEnum)
    selected_categories = graphene.List(CategoryNode)
    langues = graphene.List(graphene.String)
    centres_interet = graphene.List(graphene.String)
    type_contenu = graphene.List(graphene.String)
    reseaux_sociaux = graphene.List(ReseauSocialNode)
    collaborations = graphene.List(CollaborationNode)
    portfolio_media = graphene.List(PortfolioMediaNode)
    offres_collaboration = graphene.List(OffreCollaborationNode)
    statistiques_globales = graphene.Field(StatistiquesGlobalesType)
    
    class Meta:
        model = Influencer
        fields = (
            'id', 'user', 'instagram_username', 'pseudo', 'biography',
            'site_web', 'localisation', 'selected_categories',
            'langues', 'centres_interet', 'type_contenu',
            'disponibilite_collaboration', 'created_at', 'updated_at'
        )
        interfaces = (graphene.relay.Node,)
    
    def resolve_selected_categories(self, info):
        return self.selected_categories.all()
    
    def resolve_reseaux_sociaux(self, info):
        return self.reseaux_sociaux.all()
    
    def resolve_collaborations(self, info):
        return self.collaborations.all()
    
    def resolve_portfolio_media(self, info):
        return self.portfolio_media.all()
    
    def resolve_offres_collaboration(self, info):
        return self.offres_collaboration.all()
    
    def resolve_statistiques_globales(self, info):
        """Return current global statistics"""
        return {
            'followers_totaux': self.followers_totaux,
            'engagement_moyen_global': self.engagement_moyen_global,
            'croissance_mensuelle': self.calculate_croissance_mensuelle()
        }
