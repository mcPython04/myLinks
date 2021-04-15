#from .models import link
# Create your views here.
#from .forms import ImageForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import User
from django.template import loader

def home(request, username):
    return render(request, 'home.html')
    
def user_page(request,username):
    link_list = link.objects.all()
    template = loader.get_template('user_page.html')
    context = {
        'link_list' : link_list,'username' : username
    }
    return HttpResponse(template.render(context, request))   

def add_view(request): 
    """Process images uploaded by users"""
    link_list = link.objects.all()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'links/add.html', {'form': form, 'img_obj': img_obj,'link_list' : link_list})
    else:
        form = ImageForm()
    return render(request, 'links/add.html', {'form': form,'link_list' : link_list})


def dashboard(request):
    return render(request, "links/dashboard.html")

def base(request):
    return render(request, "base.html")