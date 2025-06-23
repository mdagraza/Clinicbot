from django.shortcuts import render
from panel.decorators import *

# Create your views here.
@login_required
def general(request):

    return render(request, 'panel copy.html') #datos