"""hselingprojects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from projects.admin import site_admin

from projects.views.pages import index, about, help, project, author_view, teacher_view, set_lang
from projects.views.profile import profile, register_user
from projects.views.profile import newAuthor, newField, newTeacher
from projects.views.profile import edit_project, model_form_upload

urlpatterns = [
    url(r'^admin/', site_admin.urls),
    url(r'^set_lang$', set_lang, name='set_lang'),
    ]

urlpatterns += i18n_patterns(
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name='about'),
    url(r'^help/', help, name='help'),
    url(r'^project/([^/]+)', project, name='project'),  # id проекта
    url(r'^author/([^/]+)', author_view, name='author'),  # id
    url(r'^teacher/([^/]+)', teacher_view, name='teacher'),  # id
    url(r'^profile/([^/]+)/$', profile, name="profile"),  # username
    url(r'^upload$', model_form_upload, name="upload"),
    url(r'^edit/([^/]+)$', edit_project, name="edit"),  # id проекта

    url(r'^accounts/register/$', register_user, name='register'),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),
    url(r'^accounts/', include('password_reset.urls')),

    url(r'^add/author/?$', newAuthor, name="new_author"),
    url(r'^add/prof/?$', newTeacher, name="new_teacher"),
    url(r'^add/field/?$', newField, name="new_field"),
    prefix_default_language=False
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(r'media/', document_root=settings.MEDIA_ROOT)
urlpatterns += url(r'^i18n/', include('django.conf.urls.i18n')),