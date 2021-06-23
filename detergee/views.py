from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def services(request):
    return render(request, "services.html")
    
def about(request):
    return render(request, "about.html")
