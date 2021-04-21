#from .forms import ImageForm
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.template import loader
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
def home(request):
    #return render(request, 'home.html')
    template = loader.get_template('home.html')
    link_list = link.objects.filter(user__username=request.user.username)
    context = {
            'link_list' : link_list
        }
    return HttpResponse(template.render(context, request))
    
def userPage(request,username):
    
    if User.objects.filter(username=username).exists():
        r_link = link.objects.filter(default=True, user__username=username)
        if r_link.exists():
            return redirect(r_link[0].hyperlink) 
        else:
            link_list = link.objects.filter(user__username=username)
            template = loader.get_template('user_page.html')
            context = {
                'link_list' : link_list,'username' : username
            }
            return HttpResponse(template.render(context, request))
    else:
        raise Http404("No Such User Exists.")

def base(request):
    return render(request, "base.html")