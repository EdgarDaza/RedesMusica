from django.db import models
from django.contrib.auth.models import User

# 🎵 Tabla de géneros
class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# 🎧 Tabla de canciones
class Cancion(models.Model):
    id_cancion = models.AutoField(primary_key=True)  # ID único automático
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=150)
    archivo = models.FileField(upload_to='musica/')  # Ruta donde se guardará el archivo
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='canciones')
    usuario_subidor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.artista}"
