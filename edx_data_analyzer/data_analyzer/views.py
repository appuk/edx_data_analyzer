# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import maincode
from .forms import NameForm
from django.http import HttpResponseRedirect
# Create your views here.

# def index(request):
#     context = {
#         'message': data_extract()
#     }
#     return render(request, 'index.html', context)


def index(request):
    graph = maincode.options[int(request.GET['graph'])]()
    return render(request, 'index.html', {'list': [i for i in range(1,11)], 'graph': graph})


#
# def index(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             data_extract()
#             return render(request, 'index.html', {'message': form.cleaned_data['your_name']})
#             # redirect to a new URL:
#             #return HttpResponseRedirect('/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request, 'index.html', {'form': form})
