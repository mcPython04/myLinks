#from .forms import ImageForm
import requests
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.template import loader
from django.views.generic.edit import FormView, DeleteView, CreateView, UpdateView, BaseDetailView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError


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


def collectionPage(request, username, collection_name):
    if User.objects.filter(username=username).exists():
        if collection.objects.filter(user__username=username, name=collection_name).exists():
            collection1 = collection.objects.get(user__username=username, name=collection_name)
            template = loader.get_template('collection_page.html')
            context = {
                'collection': collection1, 'username': username, 'collection_name': collection_name
            }
            return HttpResponse(template.render(context, request))
        else:
            raise Http404("No Such Collection Exists.")
    else:
        raise Http404("No Such User Exists.")


def base(request):
    return render(request, "base.html")


# comment
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
    fields = ['hyperlink', 'website_name', 'image']
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


# View to create collections
class CollectionCreateView(CreateView):
    model = collection
    form_class = CreateCollectionForm
    success_url = '../../home'
    template_name = 'links/create_collection.html'

    # Passes the request object to the form class; necessary to display links that only belongs to the user
    def get_form_kwargs(self):
        kwargs = super(CollectionCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    # Catches error is user doesn't enter unique collection name
    def post(self, request, *args, **kwargs):
        try:
            return super(CollectionCreateView, self).post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                 'You already have registered a Collection with this name! ' + \
                                 'All of your Collection names must be unique!')
            return render(request, template_name=self.template_name, context=self.get_context_data())

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CollectionCreateView, self).form_valid(form)


# Collection detail view
class CollectionDetailView(DetailView):
    model = collection
    template_name = 'links/collection_detail.html'


# Collection delete view
class CollectionDeleteView(DeleteView):
    model = collection
    success_url = '../../../home'
    template_name = 'links/delete_collection.html'


# Collection update view
class CollectionUpdateView(UpdateView):
    model = collection
    form_class = UpdateCollectionForm
    template_name = 'links/update_collection.html'

    # Defines new success url in order to send user back to the same collection after updating
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('detailCollection', args=[str(pk)])

    # Passes the request object to the form class; necessary to display links that only belongs to the user
    def get_form_kwargs(self):
        kwargs = super(CollectionUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


# Remove links from specified collection
def collection_link_delete_view(request, pk):
    link1 = get_object_or_404(link, id=request.POST.get('link_id'))
    link1.collection_set.remove(pk)
    return HttpResponseRedirect(reverse('detailCollection', args=[str(pk)]))





