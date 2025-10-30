import graphene
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from django.db import transaction
from datetime import datetime

from ..influencer_models import (
    Influencer, ReseauSocial, Collaboration,
    PortfolioMedia, OffreCollaboration
)
from ..influencer_node import (
    InfluencerNode, DisponibiliteEnum, PlateformeEnum,
    FrequencePublicationEnum, TypeCollaborationEnum
)
from category.models import Category

User = get_user_model()


# Input types for nested objects
class ReseauSocialInput(graphene.InputObjectType):
    plateforme = graphene.Argument(PlateformeEnum, required=True)
    url_profil = graphene.String(required=True)
    nombre_abonnes = graphene.Int(required=True)
    taux_engagement = graphene.Float(required=True)
    moyenne_vues = graphene.Int()
    moyenne_likes = graphene.Int()
    moyenne_commentaires = graphene.Int()
    frequence_publication = graphene.Argument(FrequencePublicationEnum)


class CollaborationInput(graphene.InputObjectType):
    nom_marque = graphene.String(required=True)
    campagne = graphene.String(required=True)
    periode = graphene.String(required=True)
    resultats = graphene.String()
    lien_publication = graphene.String()


class PortfolioMediaInput(graphene.InputObjectType):
    image_url = graphene.String(required=True)
    titre = graphene.String(required=True)
    description = graphene.String()
    date_creation = graphene.String(required=True)  # Format: "YYYY-MM-DD"


class OffreCollaborationInput(graphene.InputObjectType):
    type_collaboration = graphene.Argument(TypeCollaborationEnum, required=True)
    tarif_minimum = graphene.Float(required=True)
    tarif_maximum = graphene.Float(required=True)
    conditions = graphene.String()


class CompleteInfluencerProfile(graphene.Mutation):
    """Complete influencer profile with all information"""
    
    influencer = graphene.Field(InfluencerNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        # Basic Information
        instagram_username = graphene.String()
        pseudo = graphene.String()
        biography = graphene.String()
        site_web = graphene.String()
        localisation = graphene.String()
        
        # Categories and Interests
        selected_categories = graphene.List(graphene.ID)
        langues = graphene.List(graphene.String)
        centres_interet = graphene.List(graphene.String)
        type_contenu = graphene.List(graphene.String)
        
        # Collaboration
        disponibilite_collaboration = graphene.Argument(DisponibiliteEnum)
        
        # Related objects
        reseaux_sociaux = graphene.List(ReseauSocialInput)
        collaborations = graphene.List(CollaborationInput)
        portfolio_media = graphene.List(PortfolioMediaInput)
        offres_collaboration = graphene.List(OffreCollaborationInput)
    
    @transaction.atomic
    def mutate(self, info, **kwargs):
        user = info.context.user
        
        # Check authentication
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        # Check if user is an influencer
        if user.role != 'INFLUENCER':
            raise GraphQLError('This action is only available for influencer accounts')
        
        # Get or create influencer profile
        influencer, created = Influencer.objects.get_or_create(user=user)
        
        # Update basic information
        if 'instagram_username' in kwargs:
            influencer.instagram_username = kwargs['instagram_username']
        if 'pseudo' in kwargs:
            influencer.pseudo = kwargs['pseudo']
        if 'biography' in kwargs:
            influencer.biography = kwargs['biography']
        if 'site_web' in kwargs:
            influencer.site_web = kwargs['site_web']
        if 'localisation' in kwargs:
            influencer.localisation = kwargs['localisation']
        
        # Update lists
        if 'langues' in kwargs:
            influencer.langues = kwargs['langues']
        if 'centres_interet' in kwargs:
            influencer.centres_interet = kwargs['centres_interet']
        if 'type_contenu' in kwargs:
            influencer.type_contenu = kwargs['type_contenu']
        
        # Update collaboration availability
        if 'disponibilite_collaboration' in kwargs:
            influencer.disponibilite_collaboration = kwargs['disponibilite_collaboration']
        
        influencer.save()
        
        # Update selected categories
        if 'selected_categories' in kwargs:
            category_ids = kwargs['selected_categories']
            categories = Category.objects.filter(id__in=category_ids)
            influencer.selected_categories.set(categories)
        
        # Handle reseaux sociaux
        if 'reseaux_sociaux' in kwargs:
            # Clear existing and create new
            influencer.reseaux_sociaux.all().delete()
            for rs_data in kwargs['reseaux_sociaux']:
                ReseauSocial.objects.create(
                    influencer=influencer,
                    plateforme=rs_data['plateforme'],
                    url_profil=rs_data['url_profil'],
                    nombre_abonnes=rs_data['nombre_abonnes'],
                    taux_engagement=rs_data['taux_engagement'],
                    moyenne_vues=rs_data.get('moyenne_vues', 0),
                    moyenne_likes=rs_data.get('moyenne_likes', 0),
                    moyenne_commentaires=rs_data.get('moyenne_commentaires', 0),
                    frequence_publication=rs_data.get('frequence_publication', 'hebdomadaire')
                )
        
        # Handle collaborations
        if 'collaborations' in kwargs:
            influencer.collaborations.all().delete()
            for collab_data in kwargs['collaborations']:
                Collaboration.objects.create(
                    influencer=influencer,
                    nom_marque=collab_data['nom_marque'],
                    campagne=collab_data['campagne'],
                    periode=collab_data['periode'],
                    resultats=collab_data.get('resultats', ''),
                    lien_publication=collab_data.get('lien_publication', '')
                )
        
        # Handle portfolio media
        if 'portfolio_media' in kwargs:
            influencer.portfolio_media.all().delete()
            for media_data in kwargs['portfolio_media']:
                try:
                    date_creation = datetime.strptime(
                        media_data['date_creation'], 
                        '%Y-%m-%d'
                    ).date()
                except ValueError:
                    raise GraphQLError(
                        f"Invalid date format for portfolio media. Use YYYY-MM-DD format."
                    )
                
                PortfolioMedia.objects.create(
                    influencer=influencer,
                    image_url=media_data['image_url'],
                    titre=media_data['titre'],
                    description=media_data.get('description', ''),
                    date_creation=date_creation
                )
        
        # Handle offres collaboration
        if 'offres_collaboration' in kwargs:
            influencer.offres_collaboration.all().delete()
            for offre_data in kwargs['offres_collaboration']:
                OffreCollaboration.objects.create(
                    influencer=influencer,
                    type_collaboration=offre_data['type_collaboration'],
                    tarif_minimum=offre_data['tarif_minimum'],
                    tarif_maximum=offre_data['tarif_maximum'],
                    conditions=offre_data.get('conditions', '')
                )
        
        # Mark user profile as completed
        user.is_completed_profile = True
        user.save(update_fields=['is_completed_profile'])
        
        return CompleteInfluencerProfile(
            influencer=influencer,
            success=True,
            message='Influencer profile completed successfully'
        )


class UpdateInfluencerProfile(graphene.Mutation):
    """Update influencer profile information"""
    
    influencer = graphene.Field(InfluencerNode)
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        # Basic Information
        instagram_username = graphene.String()
        pseudo = graphene.String()
        biography = graphene.String()
        site_web = graphene.String()
        localisation = graphene.String()
        
        # Categories and Interests
        selected_categories = graphene.List(graphene.ID)
        langues = graphene.List(graphene.String)
        centres_interet = graphene.List(graphene.String)
        type_contenu = graphene.List(graphene.String)
        
        # Collaboration
        disponibilite_collaboration = graphene.Argument(DisponibiliteEnum)
    
    def mutate(self, info, **kwargs):
        user = info.context.user
        
        # Check authentication
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        # Check if user is an influencer
        if user.role != 'INFLUENCER':
            raise GraphQLError('This action is only available for influencer accounts')
        
        try:
            influencer = Influencer.objects.get(user=user)
        except Influencer.DoesNotExist:
            raise GraphQLError('Influencer profile not found. Please complete your profile first.')
        
        # Update basic information
        if 'instagram_username' in kwargs:
            influencer.instagram_username = kwargs['instagram_username']
        if 'pseudo' in kwargs:
            influencer.pseudo = kwargs['pseudo']
        if 'biography' in kwargs:
            influencer.biography = kwargs['biography']
        if 'site_web' in kwargs:
            influencer.site_web = kwargs['site_web']
        if 'localisation' in kwargs:
            influencer.localisation = kwargs['localisation']
        
        # Update lists
        if 'langues' in kwargs:
            influencer.langues = kwargs['langues']
        if 'centres_interet' in kwargs:
            influencer.centres_interet = kwargs['centres_interet']
        if 'type_contenu' in kwargs:
            influencer.type_contenu = kwargs['type_contenu']
        
        # Update collaboration availability
        if 'disponibilite_collaboration' in kwargs:
            influencer.disponibilite_collaboration = kwargs['disponibilite_collaboration']
        
        influencer.save()
        
        # Update selected categories
        if 'selected_categories' in kwargs:
            category_ids = kwargs['selected_categories']
            categories = Category.objects.filter(id__in=category_ids)
            influencer.selected_categories.set(categories)
        
        return UpdateInfluencerProfile(
            influencer=influencer,
            success=True,
            message='Influencer profile updated successfully'
        )


class AddReseauSocial(graphene.Mutation):
    """Add a social network to influencer profile"""
    
    reseau_social = graphene.Field('users.influencer_node.ReseauSocialNode')
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        plateforme = graphene.Argument(PlateformeEnum, required=True)
        url_profil = graphene.String(required=True)
        nombre_abonnes = graphene.Int(required=True)
        taux_engagement = graphene.Float(required=True)
        moyenne_vues = graphene.Int()
        moyenne_likes = graphene.Int()
        moyenne_commentaires = graphene.Int()
        frequence_publication = graphene.Argument(FrequencePublicationEnum)
    
    def mutate(self, info, plateforme, url_profil, nombre_abonnes, taux_engagement, **kwargs):
        user = info.context.user
        
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        if user.role != 'INFLUENCER':
            raise GraphQLError('This action is only available for influencer accounts')
        
        try:
            influencer = Influencer.objects.get(user=user)
        except Influencer.DoesNotExist:
            raise GraphQLError('Influencer profile not found. Please complete your profile first.')
        
        # Check if platform already exists
        if ReseauSocial.objects.filter(influencer=influencer, plateforme=plateforme).exists():
            raise GraphQLError(f'Social network {plateforme} already exists. Use update mutation instead.')
        
        reseau_social = ReseauSocial.objects.create(
            influencer=influencer,
            plateforme=plateforme,
            url_profil=url_profil,
            nombre_abonnes=nombre_abonnes,
            taux_engagement=taux_engagement,
            moyenne_vues=kwargs.get('moyenne_vues', 0),
            moyenne_likes=kwargs.get('moyenne_likes', 0),
            moyenne_commentaires=kwargs.get('moyenne_commentaires', 0),
            frequence_publication=kwargs.get('frequence_publication', 'hebdomadaire')
        )
        
        return AddReseauSocial(
            reseau_social=reseau_social,
            success=True,
            message='Social network added successfully'
        )


class UpdateReseauSocial(graphene.Mutation):
    """Update a social network"""
    
    reseau_social = graphene.Field('users.influencer_node.ReseauSocialNode')
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        reseau_id = graphene.ID(required=True)
        url_profil = graphene.String()
        nombre_abonnes = graphene.Int()
        taux_engagement = graphene.Float()
        moyenne_vues = graphene.Int()
        moyenne_likes = graphene.Int()
        moyenne_commentaires = graphene.Int()
        frequence_publication = graphene.Argument(FrequencePublicationEnum)
    
    def mutate(self, info, reseau_id, **kwargs):
        user = info.context.user
        
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        try:
            reseau_social = ReseauSocial.objects.get(pk=reseau_id)
        except ReseauSocial.DoesNotExist:
            raise GraphQLError('Social network not found')
        
        # Check ownership
        if reseau_social.influencer.user != user:
            raise GraphQLError('Permission denied')
        
        # Update fields
        if 'url_profil' in kwargs:
            reseau_social.url_profil = kwargs['url_profil']
        if 'nombre_abonnes' in kwargs:
            reseau_social.nombre_abonnes = kwargs['nombre_abonnes']
        if 'taux_engagement' in kwargs:
            reseau_social.taux_engagement = kwargs['taux_engagement']
        if 'moyenne_vues' in kwargs:
            reseau_social.moyenne_vues = kwargs['moyenne_vues']
        if 'moyenne_likes' in kwargs:
            reseau_social.moyenne_likes = kwargs['moyenne_likes']
        if 'moyenne_commentaires' in kwargs:
            reseau_social.moyenne_commentaires = kwargs['moyenne_commentaires']
        if 'frequence_publication' in kwargs:
            reseau_social.frequence_publication = kwargs['frequence_publication']
        
        reseau_social.save()
        
        return UpdateReseauSocial(
            reseau_social=reseau_social,
            success=True,
            message='Social network updated successfully'
        )


class DeleteReseauSocial(graphene.Mutation):
    """Delete a social network"""
    
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        reseau_id = graphene.ID(required=True)
    
    def mutate(self, info, reseau_id):
        user = info.context.user
        
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        try:
            reseau_social = ReseauSocial.objects.get(pk=reseau_id)
        except ReseauSocial.DoesNotExist:
            raise GraphQLError('Social network not found')
        
        # Check ownership
        if reseau_social.influencer.user != user:
            raise GraphQLError('Permission denied')
        
        reseau_social.delete()
        
        return DeleteReseauSocial(
            success=True,
            message='Social network deleted successfully'
        )


class AddCollaboration(graphene.Mutation):
    """Add a past collaboration"""
    
    collaboration = graphene.Field('users.influencer_node.CollaborationNode')
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        nom_marque = graphene.String(required=True)
        campagne = graphene.String(required=True)
        periode = graphene.String(required=True)
        resultats = graphene.String()
        lien_publication = graphene.String()
    
    def mutate(self, info, nom_marque, campagne, periode, **kwargs):
        user = info.context.user
        
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        if user.role != 'INFLUENCER':
            raise GraphQLError('This action is only available for influencer accounts')
        
        try:
            influencer = Influencer.objects.get(user=user)
        except Influencer.DoesNotExist:
            raise GraphQLError('Influencer profile not found. Please complete your profile first.')
        
        collaboration = Collaboration.objects.create(
            influencer=influencer,
            nom_marque=nom_marque,
            campagne=campagne,
            periode=periode,
            resultats=kwargs.get('resultats', ''),
            lien_publication=kwargs.get('lien_publication', '')
        )
        
        return AddCollaboration(
            collaboration=collaboration,
            success=True,
            message='Collaboration added successfully'
        )


class AddPortfolioMedia(graphene.Mutation):
    """Add a portfolio media item"""
    
    portfolio_media = graphene.Field('users.influencer_node.PortfolioMediaNode')
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        image_url = graphene.String(required=True)
        titre = graphene.String(required=True)
        description = graphene.String()
        date_creation = graphene.String(required=True)  # Format: "YYYY-MM-DD"
    
    def mutate(self, info, image_url, titre, date_creation, **kwargs):
        user = info.context.user
        
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        if user.role != 'INFLUENCER':
            raise GraphQLError('This action is only available for influencer accounts')
        
        try:
            influencer = Influencer.objects.get(user=user)
        except Influencer.DoesNotExist:
            raise GraphQLError('Influencer profile not found. Please complete your profile first.')
        
        try:
            date_obj = datetime.strptime(date_creation, '%Y-%m-%d').date()
        except ValueError:
            raise GraphQLError('Invalid date format. Use YYYY-MM-DD format.')
        
        portfolio_media = PortfolioMedia.objects.create(
            influencer=influencer,
            image_url=image_url,
            titre=titre,
            description=kwargs.get('description', ''),
            date_creation=date_obj
        )
        
        return AddPortfolioMedia(
            portfolio_media=portfolio_media,
            success=True,
            message='Portfolio media added successfully'
        )


class AddOffreCollaboration(graphene.Mutation):
    """Add a collaboration offer"""
    
    offre = graphene.Field('users.influencer_node.OffreCollaborationNode')
    success = graphene.Boolean()
    message = graphene.String()
    
    class Arguments:
        type_collaboration = graphene.Argument(TypeCollaborationEnum, required=True)
        tarif_minimum = graphene.Float(required=True)
        tarif_maximum = graphene.Float(required=True)
        conditions = graphene.String()
    
    def mutate(self, info, type_collaboration, tarif_minimum, tarif_maximum, **kwargs):
        user = info.context.user
        
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        if user.role != 'INFLUENCER':
            raise GraphQLError('This action is only available for influencer accounts')
        
        try:
            influencer = Influencer.objects.get(user=user)
        except Influencer.DoesNotExist:
            raise GraphQLError('Influencer profile not found. Please complete your profile first.')
        
        offre = OffreCollaboration.objects.create(
            influencer=influencer,
            type_collaboration=type_collaboration,
            tarif_minimum=tarif_minimum,
            tarif_maximum=tarif_maximum,
            conditions=kwargs.get('conditions', '')
        )
        
        return AddOffreCollaboration(
            offre=offre,
            success=True,
            message='Collaboration offer added successfully'
        )


class InfluencerMutations(graphene.ObjectType):
    """All influencer mutations"""
    complete_influencer_profile = CompleteInfluencerProfile.Field()
    update_influencer_profile = UpdateInfluencerProfile.Field()
    add_reseau_social = AddReseauSocial.Field()
    update_reseau_social = UpdateReseauSocial.Field()
    delete_reseau_social = DeleteReseauSocial.Field()
    add_collaboration = AddCollaboration.Field()
    add_portfolio_media = AddPortfolioMedia.Field()
    add_offre_collaboration = AddOffreCollaboration.Field()
