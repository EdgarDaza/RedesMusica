from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Song


# ============================================================
#                    AUTENTICACIÓN
# ============================================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.set_expiry(1209600)  # 14 días
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'music/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']
        email = request.POST['email']

        if password != confirm:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese usuario ya existe')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Cuenta creada exitosamente.')
        return redirect('login')

    return render(request, 'music/register.html')


# ============================================================
#                     HOME PRINCIPAL
# ============================================================

@login_required(login_url='login')
def home(request):
    # Título dinámico por secciones (aunque ya no usamos API)
    section = request.GET.get('section', 'recent')
    songs = Song.objects.all().order_by('-id')

    if section == "artist":
        title = "Artists"
    elif section == "albums":
        title = "Albums"
    elif section == "songs":
        title = "Songs"
    elif section == "made":
        title = "Made for You"
    else:
        title = "Recently Added"

    return render(request, 'music/home.html', {
        "user": request.user,
        "songs": songs,
        "section": section,
        "title": title,
    })


@login_required(login_url='login')
def artist_view(request):
    return render(request, 'music/artist.html')


# ============================================================
#                SUBIDA MANUAL DE AUDIO
# ============================================================

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def upload_song(request):
    if request.method == "POST":
        title = request.POST.get("title") or ""
        artist = request.POST.get("artist") or "Desconocido"

        audio_file = request.FILES.get("file")
        cover_file = request.FILES.get("cover")

        if not audio_file:
            messages.error(request, "Debes seleccionar un archivo de audio.")
            return redirect('upload_song')

        # Si no se especifica título, usar el nombre del archivo
        if not title:
            title = audio_file.name.rsplit('.', 1)[0]

        song = Song(title=title, artist=artist, file=audio_file)
        if cover_file:
            song.cover = cover_file

        song.save()
        messages.success(request, "Canción subida correctamente.")
        return redirect('home')

    return render(request, 'music/upload.html')


# ============================================================
#                       SECCIONES UI
# ============================================================

@login_required(login_url='login')
def favorites(request):
    return render(request, 'music/favorites.html')


@login_required(login_url='login')
def playlists_view(request):
    return render(request, 'music/playlists.html')


@login_required(login_url='login')
def profile_view(request):
    return render(request, 'music/profile.html')


# ============================================================
#            API INTERNA PARA ACTUALIZAR PERFIL
# ============================================================

@csrf_exempt
@login_required(login_url='login')
def update_profile(request):
    if request.method == "POST":
        new_username = request.POST.get("username")
        new_email = request.POST.get("email")

        user = request.user

        # Verificar si el username ya existe y no es el mismo usuario
        if User.objects.filter(username=new_username).exclude(id=user.id).exists():
            return JsonResponse({
                "status": "error",
                "message": "Este nombre de usuario ya está en uso."
            })

        user.username = new_username
        user.email = new_email
        user.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error", "message": "Método no permitido"})
