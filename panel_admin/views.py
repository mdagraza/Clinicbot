from django.shortcuts import render

# Create your views here.
def general(request):

    return render(request, 'panel.html')