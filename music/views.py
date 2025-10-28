from django.shortcuts import render

def home(request):
    return render(request, 'music/home.html')

def login_view(request):
    return render(request, 'music/login.html')

