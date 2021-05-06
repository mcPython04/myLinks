#from .forms import ImageForm
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.template import loader
from django.views.generic.edit import FormView, DeleteView, CreateView, UpdateView, BaseDetailView
from django.views.generic import DetailView
from django.urls import reverse_lazy


def home(request):
    #return render(request, 'home.html')
    template = loader.get_template('home.html')
    collection_list = collection.objects.filter(user__username=request.user.username)
    link_list = link.objects.filter(user__username=request.user.username)
    context = {
            'link_list' : link_list, 'collection_list' : collection_list
        }
    return HttpResponse(template.render(context, request))


def userPage(request, username):
    
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


def linkUpdateView(request):
    if request.method == "POST":
        link_list = link.objects.filter(user__username=request.user.username)
        d_id = request.POST['d_id']
        d_set = request.POST['set']
        d_id=int(d_id)
        d_link = link.objects.filter(id=d_id)
        if request.POST['type'] == "Default":
            d_link = link_list.filter(default=True)
            if d_link.exists():
                d_link.update(default=False) 
            d_link = link.objects.filter(id=d_id)
            if d_set == "Set":
                d_link.update(default=True)
            else:
                d_link.update(default=False)
        elif request.POST['type'] == "Enable":
            link_list = link.objects.filter(user__username=request.user.username, enabled=True)
            if d_set == "Set":
                d_link.update(enabled=True)
            else:
                d_link.update(enabled=False)
        return redirect('home')
    else:
        raise Http404("Something went wrong.")


class LinkCreateView(CreateView):
    model = link
    fields = ['hyperlink','website_name','image']
    success_url = '../../home'
    template_name = 'links/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(LinkCreateView, self).form_valid(form)


class LinkDeleteView(DeleteView):
    model = link
    success_url = '../../home'
    template_name = 'links/delete.html'


class LinkUploadView(UpdateView):
    model = link
    fields = ['image']
    template_name = 'links/image.html'
    success_url = '../../home'


class CollectionCreateView(CreateView):
    model = collection
    #TODO
    #ADD LINKS
    form_class = CreateCollectionForm
    success_url = '../../home'
    template_name = 'links/create_collection.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CollectionCreateView, self).form_valid(form)


# Collection detail view
class CollectionDetailView(DetailView):
    model = collection
    template_name = 'links/collection_detail.html'
