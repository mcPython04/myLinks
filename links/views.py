from django.shortcuts import render
from .models import link
# Create your views here.
from .forms import ImageForm
from django.http import HttpResponse



def index_view(request):
    #link_list = link.objects.all()
    #context = {'link_list' : link_list}
    return render(request, 'index.html')
    

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