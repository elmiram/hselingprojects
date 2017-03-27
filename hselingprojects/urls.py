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
from django.contrib import admin

from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from projects.views.pages import index, about, help, project
from projects.views.profile import profile, register_user
from projects.views.profile import newAuthor, newField, newTeacher
from projects.views.profile import edit_project, model_form_upload

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name='about'),
    url(r'^help/', help, name='help'),
    url(r'^project/([^/]+)', project, name='project'),

    url(r'^accounts/register/$', register_user, name='register'),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),
    url(r'^accounts/', include('password_reset.urls')),

    url(r'^profile/([^/]+)/$', profile, name="profile"),
    url(r'^upload$', model_form_upload, name="upload"),
    url(r'^edit/([^/]+)$', edit_project, name="edit"),

    url(r'^add/author/?$', newAuthor, name="new_author"),
    url(r'^add/prof/?$', newTeacher, name="new_teacher"),
    url(r'^add/field/?$', newField, name="new_field"),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(r'media/', document_root=settings.MEDIA_ROOT)