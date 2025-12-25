from django.db import models
from django.conf import settings



class ApplicationStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    APPROVED = 'Approved', 'Approved'
    REJECTED = 'Rejected', 'Rejected'
    WITHDRAW = 'Withdraw', 'Withdraw'



class Offer(models.Model):
    title = models.CharField(max_length=200)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    influencer_number = models.PositiveIntegerField()
    requirement = models.TextField()
    objectif = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_offers'
    )

    def __str__(self):
        return self.title



class OfferApplication(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    proposal = models.TextField()
    asking_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional professional fields
    cover_letter = models.TextField(blank=True, null=True, help_text="Optional cover letter from influencer")
    estimated_reach = models.PositiveIntegerField(null=True, blank=True, help_text="Estimated audience reach")
    delivery_days = models.PositiveIntegerField(null=True, blank=True, help_text="Estimated days to complete")
    portfolio_links = models.JSONField(default=list, blank=True, help_text="Links to previous work")
    rejection_reason = models.TextField(blank=True, null=True, help_text="Reason for rejection (if applicable)")
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes for admin")
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        help_text="Admin who reviewed the application"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, help_text="When the application was reviewed")

    class Meta:
        unique_together = ('offer', 'user')
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['status', '-submitted_at']),
            models.Index(fields=['offer', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.offer.title} ({self.status})"
    
    @property
    def is_pending(self):
        return self.status == ApplicationStatus.PENDING
    
    @property
    def is_approved(self):
        return self.status == ApplicationStatus.APPROVED
    
    @property
    def is_rejected(self):
        return self.status == ApplicationStatus.REJECTED
