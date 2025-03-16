from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *


def home(request):
    return render(request, 'dictionary/home.html')

def word(request, entry_id):
    context = {
        "response": JmdictEntry.objects.get(entry_id=entry_id)
    }

    template = loader.get_template("dictionary/word.html")
    return HttpResponse(template.render(context, request))