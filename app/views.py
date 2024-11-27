from django.shortcuts import render, HttpResponse

# Create your views here.
def first_home_page(request):
    return render(request, 'home/first_home.html')