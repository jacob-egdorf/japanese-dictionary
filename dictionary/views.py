import re

from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

CACHE_DURATION_SECONDS = 300
RESULTS_PER_PAGE = 10

def rank_entry_search_results(results, query):
    """
    Returns a list of `JmdictEntry` search results sorted by relevance to the given query.
    
    For queries in English, the ranking algorithm prioritizes entries with the shortest glosses (definitions) 
    that contain the query; the idea is that less additional information in the gloss represents a gloss that is
    a closer match to the query.
    """ 
    ranked_results = []
    for result in results:
        ranked_result = {"result": result, "rank": 999}
        for sense in result["senses"]:
            for gloss in sense["glosses"]:
                gloss_matches_query = re.search(query, gloss)
                if gloss_matches_query:
                    ranked_result["rank"] = min(ranked_result["rank"], len(gloss))
        for i in range(0, len(ranked_results)):
            if ranked_result["rank"] < ranked_results[i]["rank"]:
                ranked_results.insert(i, ranked_result)
                break
        else:
            ranked_results.append(ranked_result)
    return [r["result"] for r in ranked_results]

def home(request):
    return render(request, 'dictionary/home.html')

def search(request):
    query = request.GET.get('q')
    page_number = request.GET.get('p')
    if not page_number:
        page_number = 1
    else:
        page_number = int(page_number)

    cached_data = cache.get(query)
    if cached_data:
        search_results = cached_data
    else:
        matched_entries = JmdictEntry.objects.search_text(query).order_by('$text_score')[:100]
        search_results = rank_entry_search_results(matched_entries, query)
        cache.set(query, search_results, CACHE_DURATION_SECONDS)

    paginator = Paginator(search_results, RESULTS_PER_PAGE)
    page = paginator.get_page(page_number)

    context = {
        "query": query,
        "page_obj": page
    }

    template = loader.get_template("dictionary/search.html")
    return HttpResponse(template.render(context, request))

def word(request, entry_id):
    context = {
        "response": JmdictEntry.objects.get(entry_id=entry_id)
    }

    template = loader.get_template("dictionary/word.html")
    return HttpResponse(template.render(context, request))