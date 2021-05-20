from django.shortcuts import render
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from .models import StaticLink
from bs4 import BeautifulSoup
from django.views.generic import DetailView


# Create your views here.
class StaticCreateView(CreateView):
    model = StaticLink
    fields = ['name', 'description', 'file']
    success_url = '../../home'
    template_name = 'create_static.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        soup = BeautifulSoup(form.instance.file, "html.parser")
        form.instance.context = soup.text
        if not form.instance.name:
            form.instance.name = soup.title.string
        return super(StaticCreateView, self).form_valid(form)
