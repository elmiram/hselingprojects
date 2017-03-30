# -*- coding: utf-8 -*-
"""
Function views which correspond to index page, /help, /about and /project pages on website.

index() - does all the filtering on main page.
project() - collects project from database by id and renders it to project.html
about() and help() - render about.html and help.html
"""

from django import http
from django.shortcuts import render
from django.urls import translate_url
from projects.models import *
from django.utils.translation import ugettext_lazy as _
from django.utils.http import is_safe_url, urlunquote
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language, get_language, to_locale,
)


LANGUAGE_QUERY_PARAMETER = 'lang'


def index(request):
    projects = Project.objects.all()
    fields = Field.objects.all()
    project_types = Project.formChoices
    q = request.GET
    if q:
        author = q['author']
        title = q['title']
        prof = q['prof']
        keywords = q['keywords']
        annot = q['abstract']
        year1, year2 = q['year1'], q['year2']
        selected_fields = q.getlist('field')
        selected_types = q.getlist('project_type')
        if author:
            projects = projects.filter(author__a_second_name__contains=author.capitalize())
        if title:
            projects = projects.filter(title__icontains=title)
        if prof:
            projects = projects.filter(prof__t_second_name__contains=prof.capitalize())
        if keywords:
            words = [i.strip() for i in keywords.lower().split(',')]
            for w in words:
                projects = projects.filter(keywords__contains=w)
        if annot:
            words = [i.strip() for i in annot.lower().split(',')]
            for w in words:
                projects = projects.filter(abstract__contains=w)
        if year1:
            projects = projects.filter(year__gte=year1)
        if year2:
            projects = projects.filter(year__lte=year2)
        if selected_fields:
            projects = projects.filter(field__in=selected_fields)
        if selected_types:
            projects = projects.filter(form__in=selected_types)
        selected_fields = [int(i) for i in selected_fields]
        projects = projects.distinct()
    return render(request, 'index.html', locals())


def about(request):
    return render(request, 'about.html')


def project(request, id):
    p = Project.objects.get(pk=id)
    return render(request, 'project.html', locals())


def help(request):
    return render(request, 'help.html')


def set_lang(request):
    """
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.GET.get('next')
    if (next or not request.is_ajax()) and not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if next:
            next = urlunquote(next)  # HTTP_REFERER may be encoded.
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next) if next else http.HttpResponse(status=204)
    lang_code = request.GET.get(LANGUAGE_QUERY_PARAMETER)
    if lang_code and check_for_language(lang_code):
        if next:
            next_trans = translate_url(next, lang_code)
            if next_trans != next:
                response = http.HttpResponseRedirect(next_trans)
        if hasattr(request, 'session'):
            request.session[LANGUAGE_SESSION_KEY] = lang_code
        else:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
            )
    return response
