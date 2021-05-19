from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.template import loader
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from pythonjsonlogger import jsonlogger

logger = logging.getLogger('django')
logger1 = logging.getLogger()
logHandler = logging.FileHandler(filename='./logs/myLink.json')
formatter = jsonlogger.JsonFormatter(timestamp='server_time')
logHandler.setFormatter(formatter)
logger1.addHandler(logHandler)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')

    logger.info('{user} logged in via ip: {ip}'.format(
        user=user,
        ip=ip,
    ))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')

    logger.info('{user} logged out via ip: {ip}'.format(
        user=user,
        ip=ip,
    ))


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger.info('login failed for: {credentials} via ip: {ip}'.format(
        credentials=credentials,
        ip=ip,
    ))


def home(request):
    template = loader.get_template('home.html')
    collection_list = collection.objects.filter(user__username=request.user.username)
    link_list = link.objects.filter(user__username=request.user.username)
    context = {
            'link_list': link_list, 'collection_list': collection_list
        }
    logger.info(request.user.username + ' visited the home page')
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
            logger.info(request.user.username + ' visited ' + username + '\'s page')
            return HttpResponse(template.render(context, request))
    else:
        logger.info(request.user.username + ' tried to visit a user\'s page that did not exist')
        raise Http404("No Such User Exists.")


def collectionPage(request, username, collection_name):
    if User.objects.filter(username=username).exists():
        if collection.objects.filter(user__username=username, name=collection_name).exists():
            collection1 = collection.objects.get(user__username=username, name=collection_name)
            template = loader.get_template('collection_page.html')
            context = {
                'collection': collection1, 'username': username, 'collection_name': collection_name
            }
            logger.info(request.user.username + ' visited ' + username + '\'s ' + collection_name + ' collection')
            return HttpResponse(template.render(context, request))
        else:
            logger.info(request.user.username + ' tried to visit ' + username + '\'s collection that did not exist')
            raise Http404("No Such Collection Exists.")
    else:
        logger.info(request.user.username + ' tried to visit a user\'s collection page but the user did not exist')
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
        logger.info(self.request.user.username + ' created a link')
        return super(LinkCreateView, self).form_valid(form)


class LinkDeleteView(DeleteView):
    model = link
    success_url = '../../home'
    template_name = 'links/delete.html'

    def delete(self, request, *args, **kwargs):
        logger.info(self.request.user.username + ' deleted a link')
        return super().delete(request, *args, **kwargs)


class LinkUploadView(UpdateView):
    model = link
    fields = ['image']
    template_name = 'links/image.html'
    success_url = '../../home'

    def form_valid(self, form):
        logger.info(self.request.user.username + ' updated a link\'s image')
        return super().form_valid(form)


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
        logger.info(self.request.user.username + ' created a collection')
        return super(CollectionCreateView, self).form_valid(form)


# Collection detail view
class CollectionDetailView(DetailView):
    model = collection
    template_name = 'links/collection_detail.html'

    def get(self, request, *args, **kwargs):
        logger.info(self.request.user.username + ' looked at a collection')
        return super().get(request, *args, **kwargs)


# Collection delete view
class CollectionDeleteView(DeleteView):
    model = collection
    success_url = '../../../home'
    template_name = 'links/delete_collection.html'

    def delete(self, request, *args, **kwargs):
        logger.info(self.request.user.username + ' deleted a collection')
        return super().delete(request, *args, **kwargs)


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

    def form_valid(self, form):
        logger.info(self.request.user.username + ' updated a collection')
        return super().form_valid(form)


# Remove links from specified collection
def collection_link_delete_view(request, pk):
    link1 = get_object_or_404(link, id=request.POST.get('link_id'))
    link1.collection_set.remove(pk)
    logger.info(request.user.username + ' removed a link from his/her collection')
    return HttpResponseRedirect(reverse('detailCollection', args=[str(pk)]))

