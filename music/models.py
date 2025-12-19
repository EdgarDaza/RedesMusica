from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100, blank=True, default="Desconocido")
    file = models.FileField(upload_to='music/')  # MP3, WAV, etc.
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)  # opcional

    def __str__(self):
        return f"{self.title} - {self.artist}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_photos/", default="default.jpg")

    def __str__(self):
        return self.user.username
        
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)

    instance.profile.save()