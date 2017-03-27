# coding=utf-8
import sys
import os
import json
import requests


sys.path.append(r'C:\Users\Admin\OneDrive\PycharmProjects\hselingprojects\hselingprojects')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hselingprojects.settings'

import django
django.setup()
from projects.models import *
from django.core.files import File


def save_file(url):
    work_file = requests.get(url)
    fname = work_file.headers['content-disposition'].split('=')[-1]
    with open(fname, 'wb') as pdf:
        pdf.write(work_file.content)

    with open(fname, 'rb') as f:
        dict_file = File(f)
        d = DictFile(user=User.objects.get(pk=2))
        d.file.save(fname, dict_file, True)
        d.save()
    os.remove(fname)
    return d


with open('hse_vkr.json', 'r', encoding='utf-8') as f:
    works = json.loads(f.read())

for w in works:
    author, created = Author.objects.get_or_create(**w['author'])
    prof, created2 = Teacher.objects.get_or_create(**w['prof'])
    p = Project(title=w['title'], title_en=w['title_en'],
                keywords=w['keywords'], keywords_en=w['keywords_en'],
                abstract=w['abstract'], abstract_en=w['abstract_en'],
                form=w['form'], lang=w['lang'], course=w['course'], user=User.objects.get(pk=2), year=w['year'])
    p.save()
    p.author.add(author)
    p.prof.add(prof)
    if w['file']:
        file = save_file(w['file'])
        p.file = file
    p.save()

