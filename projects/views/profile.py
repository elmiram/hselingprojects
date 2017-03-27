from django.conf import settings
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, HttpResponse, render_to_response
from projects.forms import DictFileForm, UserCreationForm, ProjectForm, AuthorForm, TeacherForm, FieldForm
from projects.models import UserProfile, DictFile, Author, Teacher, Field, Project

import os
from django.utils.html import escape

from django.contrib.auth.decorators import login_required


@login_required
def newAuthor(request):
    return handlePopAdd(request, AuthorForm, 'author')


@login_required
def newTeacher(request):
    return handlePopAdd(request, TeacherForm, 'prof')


@login_required
def newField(request):
    return handlePopAdd(request, FieldForm, 'field')


def handlePopAdd(request, addForm, field):
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError as error:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">window.opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
        (escape(newObject._get_pk_val()), escape(newObject)))
    else:
        form = addForm()
    return render(request, "popupform.html", locals())


def register_callback(user):
    user_profile = UserProfile(user=user)
    user_profile.save()


def approved_check(user):
    return UserProfile.objects.get(user=user).is_approved


def profile(request, username):
    if request.method == 'POST':
        values = request.POST.getlist('files[]')
        action = request.POST['action']
        if action == 'delete':
            for i in values:
               Project.objects.get(pk=int(i)).delete()
    pr = Project.objects.filter(user=request.user)
    return render(request, 'profile.html', {'files': pr})


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            is_student = form.cleaned_data['is_student']
            is_teacher = form.cleaned_data['is_teacher']

            if User.objects.filter(username=username):
                error = 'Пользователь с таким логином уже существует'
                return render(request, 'register.html', locals())

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            fathers_name = form.cleaned_data['fathers_name']

            user = User.objects.create_user(username, email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            user_profile = UserProfile(user=user, fathers_name=fathers_name, is_student=is_student, is_teacher=is_teacher)
            user_profile.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(request.GET.get('next', '/') or '/')

    form = UserCreationForm()
    next_page = request.GET.get('next', '/')
    return render(request, 'register.html', locals())


def model_form_upload(request, user):
    authors = Author.objects.all()
    teachers = Teacher.objects.all()
    fields = Field.objects.all()
    langs = Project.langChoices
    project_types = Project.formChoices
    courses = Project.courseChoices
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            p = project_form.save(commit=False)
            file_form = DictFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                newdoc = DictFile(file=request.FILES['file'], user=request.user)
                newdoc.save()
            else:
                newdoc = None
            p.file = newdoc
            p.save()
            p.author.add(*request.POST.getlist('author'))
            p.field.add(*request.POST.getlist('field'))
            p.prof.add(*request.POST.getlist('prof'))
            p.save()
            show_form = False
            valid = True
            return render(request, 'project_upload.html', locals())
        else:
            errors = project_form.errors
            show_form = True
            valid = False
            render(request, 'project_upload.html', locals())
    else:
        project_form = ProjectForm()
        file_form = DictFileForm()
        show_form = True
        valid = True
    return render(request, 'project_upload.html', locals())


def handle_uploads(request, user):
    if request.method == 'POST':
        values = request.POST.getlist('files[]')
        action = request.POST['action']
        if action == 'delete':
            for i in values:
               Project.objects.get(pk=int(i)).delete()
    pr = Project.objects.filter(user=request.user)
    return render(request, 'user_files.html', {'files': pr})


def edit_project(request, user, p_id):
    authors = Author.objects.all()
    teachers = Teacher.objects.all()
    fields = Field.objects.all()
    langs = Project.langChoices
    project_types = Project.formChoices
    courses = Project.courseChoices
    p = Project.objects.get(pk=p_id)
    if request.method == 'POST':
        pr = ProjectForm(request.POST, request.FILES)
        if pr.is_valid():
            file_form = DictFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                p.file.file = request.FILES['file']
            p.author.add(*request.POST.getlist('author'))
            p.field.add(*request.POST.getlist('field'))
            p.prof.add(*request.POST.getlist('prof'))
            p.title = request.POST['title']
            p.title_en = request.POST['title_en']
            p.keywords = request.POST['keywords']
            p.keywords_en = request.POST['keywords_en']
            p.abstract = request.POST['abstract']
            p.abstract_en = request.POST['abstract_en']
            p.link = request.POST['link']
            p.course = request.POST['course']
            p.form = request.POST['form']
            p.lang = request.POST['lang']
            p.save()
            show_form = False
            valid = True
            return render(request, 'edit.html', locals())
        else:
            errors = pr.errors
            show_form = True
            valid = False
            render(request, 'edit.html', locals())
    else:
        p = Project.objects.get(pk=p_id)
        project_form = ProjectForm()
        file_form = DictFileForm()
        show_form = True
        valid = True
        field_set = set(p.field.values_list('id', flat=True))
        prof_set = set(p.prof.values_list('id', flat=True))
        author_set = set(p.author.values_list('id', flat=True))
    return render(request, 'edit.html', locals())