from datetime import date

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from djangomako.shortcuts import render_to_response

from newsissue.paginator import Paginator
from newsissue.news.models import *

def get_template_name(name):
    return '%s/%s' % ('cleanblue', name)

def server_error(request):
    return direct_to_template(request, get_template_name('500.html'))

def page_not_found(request):
    return direct_to_template(request, get_template_name('404.html'))

def list_view(request, category_id, page):
    entries = Entry.published.order_by('-pub_date')
    base_url = request.path
    
    if page:
        base_url = base_url[:-1 * len(page) - 1]

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        entries = entries.filter(category=category)
    
    dates = Entry.published.all().dates('pub_date', 'month')
    
    categorys = Category.objects.all()   
    
    #paginator = Paginator(entries, 5)
    #page = paginator.page(page or 1)
    return render_to_response( get_template_name('list.html'),{'user':request.user,
			                                       'entries':entries,
							       'categorys':categorys})
def entry_view(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    entry.views +=1
    entry.save()
    categorys = Category.objects.all() 
    return render_to_response( get_template_name('entry.html'),{'user':request.user,
			                                        'entry_':entry,
								'categorys':categorys})

def vote_view(request, type, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if type == "goodnews":
        entry.good += 1
    elif type == "badnews":
        entry.bad += 1
    entry.save()
    return render_to_response( get_template_name('blank.html'),{})