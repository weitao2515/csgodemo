from django.shortcuts import render

def index(request):
    request.META["CSRF_COOKIE_USED"] = True
    return render(request,'index.html')