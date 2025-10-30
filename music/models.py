from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100, blank=True, default="Desconocido")
    file = models.FileField(upload_to='music/')  # MP3, WAV, etc.
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)  # opcional

    def __str__(self):
        return f"{self.title} - {self.artist}"
