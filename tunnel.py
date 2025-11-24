import subprocess

print("🌍 Iniciando túnel seguro con ngrok...")
subprocess.Popen(["ngrok", "http", "8000"])

print("🚀 Iniciando servidor Django...")
subprocess.call(["python", "manage.py", "runserver"])
