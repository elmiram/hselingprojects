from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from projects.models import *
from django.utils.translation import ugettext_lazy as _
from django.forms import TextInput, Select
from django.contrib.admin import AdminSite


class ProjectsAdminSite(AdminSite):
    site_header = _('Проекты Школы Лингвистики')
    site_title = _('Проекты Школы Лингвистики - Управление')
    index_title = _('Управление проектами')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'authors', 'course')  # в таблице
    fieldsets = (
        (None, {'fields': [('user', 'visible_to_all')]}),
    )

    def authors(self, instance):
        return ', '.join(a.a_second_name for a in instance.author.all())


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en')


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('a_second_name', 'a_first_name', 'a_first_name_en', 'a_second_name_en')
    list_display = ('name', 'english_name', 'admission_year')
    fieldsets = (
        (_('Имя на русском'), {'fields': [('a_second_name', 'a_first_name', 'a_fathers_name')]}),
        (_('Имя на английском'), {'fields': [('a_first_name_en', 'a_second_name_en')]}),
        (None, {'fields': [('admission_year', 'a_email')]}),
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})}
    }

    def name(self, i):
        return '{} {} {}'.format(i.a_second_name, i.a_first_name, i.a_fathers_name).strip()
    name.short_description = _("Имя на русском")
    name.admin_order_field = 'a_second_name'

    def english_name(self, i):
        return '{} {}'.format(i.a_first_name_en, i.a_second_name_en).strip()
    english_name.short_description = _("Имя на английском")
    english_name.admin_order_field = 'a_second_name_en'


class TeacherAdmin(admin.ModelAdmin):
    search_fields = ('t_second_name', 't_first_name', 't_first_name_en', 't_second_name_en')
    list_display = ('name', 'english_name')
    fieldsets = (
        (_('Имя на русском'), {'fields': [('t_second_name', 't_first_name', 't_fathers_name')]}),
        (_('Имя на английском'), {'fields': [('t_first_name_en', 't_second_name_en')]}),
        (None, {'fields': [('department', 'position', 'degree')]}),
        (None, {'fields': [('t_email')]}),
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})}
    }

    def name(self, i):
        return '{} {} {}'.format(i.t_second_name, i.t_first_name, i.t_fathers_name).strip()
    name.short_description = _("Имя на русском")
    name.admin_order_field = 't_second_name'

    def english_name(self, i):
        return '{} {}'.format(i.t_first_name_en, i.t_second_name_en).strip()
    english_name.short_description = _("Имя на английском")
    english_name.admin_order_field = 't_second_name_en'


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    max_num = 1
    can_delete = False


class StatusFilter(admin.SimpleListFilter):
    title = _("статус")
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [('approved', _('подтвержден')), ('declined', _('отклонен')), ('pending', _('требует подтверждения'))]

    def queryset(self, request, queryset):
        if self.value() is None:
            return User.objects.all()
        val = self.value()
        if val == 'declined':
            return queryset.filter(profile__is_declined=True)
        if val == 'approved':
            return queryset.filter(profile__is_approved=True)
        return queryset.filter(profile__is_approved=False).filter(profile__is_declined=False)


def make_approved(modeladmin, request, queryset):
    q = UserProfile.objects.filter(user__in=queryset)
    q.update(is_approved=True, is_declined=False)
    for user in q:
        user.send_letter(approved=True)
make_approved.short_description = _("Подтвердить выделенных пользователей")


def make_declined(modeladmin, request, queryset):
    q = UserProfile.objects.filter(user__in=queryset)
    q.update(is_declined=True, is_approved=False)
    for user in q:
        user.send_letter(declined=True)
make_declined.short_description = _("Отклонить выделенных пользователей")


class MyUserAdmin(UserAdmin):
    readonly_fields = ('username',)
    list_display = ('username', 'last_name', 'first_name', 'fathers_name', 'email', 'is_moderator', 'is_student', 'is_teacher', 'is_approved')
    inlines = [UserProfileInline]
    list_filter = (StatusFilter, 'groups')
    actions = [make_approved, make_declined]

    def is_student(self, i):
        return i.profile.is_student
    is_student.boolean = True
    is_student.short_description = _("Студент")

    def is_teacher(self, i):
        return i.profile.is_teacher
    is_teacher.boolean = True
    is_teacher.short_description = _("Преподаватель")

    def is_moderator(self, i):
        group = Group.objects.get(name='moderator')
        return i.is_staff and group in i.groups.all()
    is_moderator.boolean = True
    is_moderator.short_description = _("Модератор")

    def is_approved(self, i):
        return i.profile.is_approved
    is_approved.boolean = True
    is_approved.short_description = _("Подтвержден")

    def fathers_name(self, i):
        return i.profile.fathers_name
    fathers_name.short_description = _("Отчество")


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Основная информация'), {'fields': [('first_name', 'last_name', 'email')]}),
        (_('Права доступа'), {'fields': [('is_active', 'is_staff'), ('groups')]}),
    )

    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})}
    }


site_admin = ProjectsAdminSite(name='admin')
site_admin.register(User, MyUserAdmin)
site_admin.register(Group)
site_admin.register(DictFile)
site_admin.register(Author, AuthorAdmin)
site_admin.register(Teacher, TeacherAdmin)
site_admin.register(Field, FieldAdmin)
site_admin.register(Project, ProjectAdmin)

