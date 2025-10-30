from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Song
from django.views.decorators.http import require_http_methods




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(1209600)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'music/login.html')

def artist_view(request):
    return render(request, 'music/artist.html')@login_required(login_url='login')

@login_required(login_url='login')
def home(request):
    section = request.GET.get('section', 'recent')  # valor por defecto
    songs = Song.objects.all().order_by('-id')

    # Ejemplo básico de filtrado o título
    if section == 'artist':
        title = "Artists"
    elif section == 'albums':
        title = "Albums"
    elif section == 'songs':
        title = "Songs"
    elif section == 'made':
        title = "Made for You"
    else:
        title = "Recently Added"

    return render(request, 'music/home.html', {
        'user': request.user,
        'songs': songs,
        'section': section,
        'title': title,
    })


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
        messages.success(request, 'Cuenta creada exitosamente. Inicia sesión.')
        return redirect('login')

    return render(request, 'music/register.html')

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def upload_song(request):
    if request.method == "POST":
        title = request.POST.get("title") or ""
        artist = request.POST.get("artist") or "Desconocido"
        file = request.FILES.get("file")
        cover = request.FILES.get("cover")

        if not file:
            from django.contrib import messages
            messages.error(request, "Debes seleccionar un archivo de audio.")
            return redirect('upload_song')

        song = Song(title=title or file.name.rsplit('.', 1)[0], artist=artist, file=file)
        if cover:
            song.cover = cover
        song.save()
        return redirect('home')

    return render(request, 'music/upload.html')
