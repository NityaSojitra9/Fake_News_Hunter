from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def display_name(self):
        return self.full_name if self.full_name else self.user.username

# Signal to create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='activity')
    total_analyses = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)
    reputation_score = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Activity"

    class Meta:
        verbose_name_plural = "User Activities"

class ArticleAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analyses', null=True, blank=True)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=512)
    content = models.TextField()
    publication_date = models.DateTimeField(null=True, blank=True)
    author = models.CharField(max_length=256, null=True, blank=True)
    source_domain = models.CharField(max_length=128)
    prediction = models.CharField(max_length=32)
    confidence = models.FloatField()
    sentiment = models.CharField(max_length=32)
    sentiment_score = models.FloatField()
    entities = models.TextField()
    trust_score = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.prediction})"

    class Meta:
        verbose_name_plural = "Article Analyses"
        ordering = ['-created_at']
