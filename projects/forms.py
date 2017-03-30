# -*- coding: utf-8 -*-

from django import forms
from projects.models import DictFile, Project, Author, Teacher, Field
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings


from django.template.loader import render_to_string


class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("add_button_template.html", {'field': name})
        return html+popupplus


class MultipleSelectWithPop(forms.SelectMultiple):
    def render(self, name, *args, **kwargs):
        html = super(MultipleSelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("add_button_template.html", {'field': name})
        return html+popupplus


class UserCreationForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    fathers_name = forms.CharField(required=False)
    is_teacher = forms.BooleanField(required=False)
    is_student = forms.BooleanField(required=False)


class DictFileForm(forms.ModelForm):
    class Meta:
        model = DictFile
        fields = ('file', 'user')


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('a_second_name', 'a_first_name', 'a_fathers_name', 'a_second_name_en',
                  'a_first_name_en', 'admission_year', 'a_email')


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ('name', 'name_en',)


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('t_second_name', 't_first_name',  't_fathers_name', 't_second_name_en',
                  't_first_name_en', 'department', 'position', 'degree', 't_email')


class ProjectForm(forms.ModelForm):
    author = forms.ModelMultipleChoiceField(Author.objects, required=True, widget=MultipleSelectWithPop)
    prof = forms.ModelMultipleChoiceField(Teacher.objects, required=True, widget=MultipleSelectWithPop)
    field = forms.ModelMultipleChoiceField(Field.objects, required=True, widget=MultipleSelectWithPop)

    class Meta:
        model = Project
        fields = ('user', 'author', 'prof', 'year', 'title', 'keywords', 'abstract',
                  'title_en', 'keywords_en', 'abstract_en',  'link', 'field', 'lang', 'form', 'course', 'mark')