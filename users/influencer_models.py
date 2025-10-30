from django.db import models
from django.contrib.auth import get_user_model
from category.models import Category

User = get_user_model()


class Influencer(models.Model):
    """Influencer profile extending User model"""
    
    DISPONIBILITE_CHOICES = [
        ('disponible', 'Disponible'),
        ('occupe', 'Occupé'),
        ('partiellement_disponible', 'Partiellement disponible'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    
    # Basic Information
    instagram_username = models.CharField(max_length=255, blank=True, null=True)
    pseudo = models.CharField(max_length=255, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    site_web = models.URLField(blank=True, null=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    
    # Categories and Interests
    selected_categories = models.ManyToManyField(
        Category, 
        related_name='influencers_categories',
        blank=True
    )
    
    # Additional fields stored as JSON for flexibility
    langues = models.JSONField(default=list, blank=True)  # ["Français", "Anglais", "Arabe"]
    centres_interet = models.JSONField(default=list, blank=True)  # ["Mode", "Voyage", "Beauté"]
    type_contenu = models.JSONField(default=list, blank=True)  # ["Photo", "Vidéo", "Story"]
    
    # Collaboration
    disponibilite_collaboration = models.CharField(
        max_length=50,
        choices=DISPONIBILITE_CHOICES,
        default='disponible'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'influencers'
        verbose_name = 'Influencer'
        verbose_name_plural = 'Influencers'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.name} - {self.pseudo or 'No pseudo'}"
    
    @property
    def followers_totaux(self):
        """Calculate total followers across all platforms"""
        return sum(rs.nombre_abonnes for rs in self.reseaux_sociaux.all())
    
    @property
    def engagement_moyen_global(self):
        """Calculate average engagement across all platforms"""
        reseaux = self.reseaux_sociaux.all()
        if not reseaux:
            return 0.0
        return sum(rs.taux_engagement for rs in reseaux) / len(reseaux)
    
    def calculate_croissance_mensuelle(self):
        """Calculate monthly growth (placeholder for future implementation)"""
        # This would require historical data tracking
        return 0.0


class ReseauSocial(models.Model):
    """Social network profile for influencer"""
    
    PLATEFORME_CHOICES = [
        ('Instagram', 'Instagram'),
        ('TikTok', 'TikTok'),
        ('YouTube', 'YouTube'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('LinkedIn', 'LinkedIn'),
        ('Snapchat', 'Snapchat'),
    ]
    
    FREQUENCE_CHOICES = [
        ('quotidienne', 'Quotidienne'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('bi_hebdomadaire', 'Bi-hebdomadaire'),
        ('mensuelle', 'Mensuelle'),
    ]
    
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.CASCADE,
        related_name='reseaux_sociaux'
    )
    
    plateforme = models.CharField(max_length=50, choices=PLATEFORME_CHOICES)
    url_profil = models.URLField()
    nombre_abonnes = models.IntegerField(default=0)
    taux_engagement = models.FloatField(default=0.0)  # Percentage
    moyenne_vues = models.IntegerField(default=0)
    moyenne_likes = models.IntegerField(default=0)
    moyenne_commentaires = models.IntegerField(default=0)
    frequence_publication = models.CharField(
        max_length=50,
        choices=FREQUENCE_CHOICES,
        default='hebdomadaire'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reseaux_sociaux'
        verbose_name = 'Réseau Social'
        verbose_name_plural = 'Réseaux Sociaux'
        ordering = ['-nombre_abonnes']
        unique_together = ['influencer', 'plateforme']
    
    def __str__(self):
        return f"{self.influencer.user.name} - {self.plateforme}"


class Collaboration(models.Model):
    """Past collaboration for influencer"""
    
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.CASCADE,
        related_name='collaborations'
    )
    
    nom_marque = models.CharField(max_length=255)
    campagne = models.CharField(max_length=255)
    periode = models.CharField(max_length=100)  # e.g., "Juin 2025"
    resultats = models.TextField(blank=True, null=True)
    lien_publication = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaborations'
        verbose_name = 'Collaboration'
        verbose_name_plural = 'Collaborations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.influencer.user.name} - {self.nom_marque}"


class PortfolioMedia(models.Model):
    """Portfolio media items for influencer"""
    
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.CASCADE,
        related_name='portfolio_media'
    )
    
    image_url = models.URLField()
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'portfolio_media'
        verbose_name = 'Portfolio Media'
        verbose_name_plural = 'Portfolio Media'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.influencer.user.name} - {self.titre}"


class OffreCollaboration(models.Model):
    """Collaboration offer pricing and conditions"""
    
    TYPE_CHOICES = [
        ('placement_produit', 'Placement produit'),
        ('story', 'Story'),
        ('post', 'Post'),
        ('video', 'Vidéo'),
        ('reel', 'Reel'),
        ('live', 'Live'),
        ('ambassadeur', 'Ambassadeur'),
    ]
    
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.CASCADE,
        related_name='offres_collaboration'
    )
    
    type_collaboration = models.CharField(max_length=100, choices=TYPE_CHOICES)
    tarif_minimum = models.DecimalField(max_digits=10, decimal_places=2)
    tarif_maximum = models.DecimalField(max_digits=10, decimal_places=2)
    conditions = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'offres_collaboration'
        verbose_name = 'Offre de Collaboration'
        verbose_name_plural = 'Offres de Collaboration'
        ordering = ['type_collaboration']
    
    def __str__(self):
        return f"{self.influencer.user.name} - {self.type_collaboration}"


class StatistiquesGlobales(models.Model):
    """Global statistics for influencer (historical tracking)"""
    
    influencer = models.ForeignKey(
        Influencer,
        on_delete=models.CASCADE,
        related_name='statistiques_historique'
    )
    
    followers_totaux = models.IntegerField(default=0)
    engagement_moyen_global = models.FloatField(default=0.0)
    croissance_mensuelle = models.FloatField(default=0.0)  # Percentage
    
    # Month tracking
    mois = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'statistiques_globales'
        verbose_name = 'Statistiques Globales'
        verbose_name_plural = 'Statistiques Globales'
        ordering = ['-mois']
        unique_together = ['influencer', 'mois']
    
    def __str__(self):
        return f"{self.influencer.user.name} - {self.mois.strftime('%B %Y')}"
