from django.shortcuts import render
from .models import link
# Create your views here.
from .forms import ImageForm
from django.http import HttpResponse



def index(request):
    link_list = link.objects.all()
    context = {'link_list' : link_list}
    return render(request, 'links/index.html', context)
    

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})