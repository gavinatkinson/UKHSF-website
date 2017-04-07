from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from .models import Space
import sys
import requests
import markdown
import urlparse

def index(request):
    json_data = open('main/static/data.json')
    data = json.load(json_data)
    context = {
        'spaces':data
    }
    return render(request, 'main/index.html', context)

def spaces(request):
    json_data = open('main/static/data.json')
    data = json.load(json_data)
    return JsonResponse({'spaces':data})


@login_required
def space_detail(request):
    context = {
        'spaces': Space.objects.all()
    }
    return render(request, 'main/space_detail.html', context)

def valueOrBlank(obj, attr, d):
    if attr in obj:
        return obj[attr]
    else:
        return d

@login_required
def import_spaces(request):
    json_data = open('main/static/data.json')
    data = json.load(json_data)

    for s in data:

        # see if record already exists
        q = Space.objects.filter(name=s['name'])
        if len(q) == 0:
            srecord = Space(
                name = valueOrBlank(s,'name',''),
                longname = valueOrBlank(s,'longname',''),
                town = valueOrBlank(s,'town',''),
                country = valueOrBlank(s,'country',''),
                region = valueOrBlank(s,'region',''),
                have_premises = valueOrBlank(s,'havePremises','No')== 'Yes',
                town_not_in_name = valueOrBlank(s,'townNotInName','No')== 'Yes',
                address_first_line = valueOrBlank(s,'addressFirstLine',''),
                postcode = valueOrBlank(s,'postcode',''),
                lat = valueOrBlank(s,'lat',0.0),
                lng = valueOrBlank(s,'lng',0.0),
                main_website_url = valueOrBlank(s,'mainWebsiteUrl',''),
                logo_image_url = valueOrBlank(s,'logoImageUrl',''),
                status = valueOrBlank(s,'status',''),
                classification = valueOrBlank(s,'classification','')
            )
            srecord.save()

        #else
            # existing record, do nothing for now


    return redirect('/space_detail')


def starting(request):
    return render(request, 'main/starting.html')


def join(request):
    return render(request, 'main/join.html')


def join_supporter(request):
    return render(request, 'main/supporter.html')

class Login(View):
    def get(self, request):
        return render(request, 'main/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def resources(request, path):

    origpath = path

    # need to make sure path ends in an .md file, assume README.md
    if not path.endswith('.md'):
        if path != '' and not path.endswith('/'):
            path += '/'
        path += 'README.md'
        return redirect('/resources/' + path)

    rawurl = urlparse.urljoin('https://raw.githubusercontent.com/UKHackspaceFoundation/resources/master/', path);

    url = urlparse.urljoin('https://github.com/UKHackspaceFoundation/resources/blob/master/', path)

    r = requests.get(rawurl)

    # build breadcrumbs
    slugs = path.split('/')
    breadcrumbs = []
    slugurl = ''
    for slug in slugs:
        if slug != '':
            slugurl = '%s/%s' % (slugurl, slug)
            breadcrumb = {'slug':slug, 'url':slugurl}
            breadcrumbs.append(breadcrumb)

    # TODO: deal with not found
    context = {
        'origpath': origpath,
        'breadcrumbs':breadcrumbs,
        'path':path.split('/'),
        'rawurl':rawurl,
        'url':url,
        'imageBase': rawurl.rsplit('/', 1)[0] + '/',
        'md': markdown.markdown(r.text, safe_mode='escape')
    }
    return render(request, 'main/resources.html', context)
