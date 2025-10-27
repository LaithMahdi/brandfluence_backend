from django.db import models
from time_stamped_model.models import TimeStampedModel


class Category(TimeStampedModel):
    """Category model for organizing content"""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name