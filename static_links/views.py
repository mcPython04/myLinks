from django.shortcuts import render
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from .models import StaticLink
from bs4 import BeautifulSoup
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views.generic import DetailView, ListView
from django.db.models import Q

# Create your views here.
class StaticCreateView(CreateView):
    model = StaticLink
    fields = ['name', 'description', 'file']
    success_url = '../../home'
    template_name = 'create_static.html'

    def post(self, request, *args, **kwargs):
        try:
            return super(StaticCreateView, self).post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                 'There is already a static link with this name. Please enter another name.')
            return render(request, template_name=self.template_name, context=self.get_context_data())

    def form_valid(self, form):
        form.instance.user = self.request.user
        soup = BeautifulSoup(form.instance.file, "html.parser")
        form.instance.context = soup.text
        if not form.instance.name:
            form.instance.name = soup.title.string
        return super(StaticCreateView, self).form_valid(form)


def static_link_page(request, name):
    if StaticLink.objects.filter(name=name).exists():
            link = StaticLink.objects.get(name=name)
            template = loader.get_template('static_page.html')
            context = {
                'link': link,
            }
            return HttpResponse(template.render(context, request))
    else:
        raise Http404("No Such Static Link Exists.")


class SearchResultsView(ListView):
    model = StaticLink
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = StaticLink.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(context__icontains=query))
        return object_list

