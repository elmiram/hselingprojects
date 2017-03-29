# -*- coding: utf-8 -*-
"""
Function views which correspond to index page, /help, /about and /project pages on website.

index() - does all the filtering on main page.
project() - collects project from database by id and renders it to project.html
about() and help() - render about.html and help.html
"""

from django.shortcuts import render
from projects.models import *


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
