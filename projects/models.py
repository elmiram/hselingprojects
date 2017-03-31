from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.core.mail import EmailMessage
import os
import json


def get_name(self):
    name = '{1} {0}'.format(self.first_name, self.last_name)
    return '{} ({})'.format(name, self.username)
User.add_to_class("__str__", get_name)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class DictFile(models.Model):
    user = models.ForeignKey(User, auto_created=True, verbose_name=_('пользователь'))
    file = models.FileField(upload_to=user_directory_path, verbose_name=_('файл'))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_('загружен'))

    def __str__(self):
        return os.path.basename(self.file.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('пользователь'))  # SET_NULL ?
    fathers_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('отчество'))
    is_teacher = models.BooleanField(default=False, verbose_name=_('является преподавателем'))
    is_student = models.BooleanField(default=False, verbose_name=_('является студентом'))
    is_approved = models.BooleanField(default=False, verbose_name=_('подтвержден'))
    is_declined = models.BooleanField(default=False, verbose_name=_('отклонен'))

    def __str__(self):
        return '{0} {1} ({2})'.format(self.user.first_name, self.user.last_name, self.user.username)

    def send_letter(self, approved=False, declined=False):
        with open(os.path.join(settings.BASE_DIR, 'templates', 'status_email', 'user_status.json'),
                  encoding='utf-8') as f:
            email_content = json.loads(f.read())
        status_email = email_content[get_language()]
        subj, text = '', ''
        if approved:
            subj = 'approved_subject'
            text = 'approved'
        elif declined:
            subj = 'declined_subject'
            text = 'declined'
        if subj and text:
            subject = status_email[subj]
            message = status_email[text].format(self.user.first_name)
            from_email = settings.EMAIL_HOST_USER
            msg = EmailMessage(subject, message, from_email, [self.user.email])
            msg.content_subtype = "html"
            msg.send()

    def save(self, *args, **kwargs):
        # todo сейчас письмо всегда будет отправлять на русском. нужно добавить язык пользователя в модель.
        if self.id:
            old = UserProfile.objects.get(pk=self.id)
            if not old.is_approved == self.is_approved and self.is_approved:
                self.send_letter(approved=True)
            if not old.is_declined == self.is_declined and self.is_declined:
                self.send_letter(declined=True)
        super(UserProfile, self).save()


class Author(models.Model):
    a_first_name = models.CharField(max_length=20, verbose_name=_('имя на русском'))
    a_second_name = models.CharField(max_length=20, verbose_name=_('фамилия на русском'))
    a_first_name_en = models.CharField(max_length=20, verbose_name=_('имя на английском'))
    a_second_name_en = models.CharField(max_length=20, verbose_name=_('фамилия на английском'))
    a_fathers_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('отчество'))
    admission_year = models.IntegerField(validators=[MinValueValidator(2010)], verbose_name=_('год поступления'))
    a_email = models.EmailField(verbose_name=_('email'), blank=True, null=True)

    def __str__(self):
        return '{0} {1} {2}'.format(self.a_second_name, self.a_first_name, self.a_fathers_name).strip()

    @property
    def full(self):
        return '{0} {1} {2}'.format(self.a_second_name, self.a_first_name, self.a_fathers_name).strip()


class Teacher(models.Model):
    t_first_name = models.CharField(max_length=20, verbose_name=_('имя на русском'))
    t_second_name = models.CharField(max_length=20, verbose_name=_('фамилия на русском'))
    t_first_name_en = models.CharField(max_length=20, verbose_name=_('имя на английском'))
    t_second_name_en = models.CharField(max_length=20, verbose_name=_('фамилия на английском'))
    t_fathers_name = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('отчество'))
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('департамент'))
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('должность'))
    degree = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('степень'))
    t_email = models.EmailField(verbose_name=_('email'), blank=True, null=True)

    def __str__(self):
        return '{0} {1} {2}'.format(self.t_second_name, self.t_first_name, self.t_fathers_name).strip()

    @property
    def full(self):
        return '{0} {1} {2}'.format(self.a_second_name, self.a_first_name, self.a_fathers_name).strip()


class Field(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('сфера на русском'))
    name_en = models.CharField(max_length=50, verbose_name=_('сфера на английском'))

    def __str__(self):
        return '{0}'.format(self.name)


class Project(models.Model):
    formChoices = (('thesis', _('ВКР')),
                   ('workshop', _('мастерская')),
                   ('course', _('курсовая работа')),
                   ('project', _('проект')))

    langChoices = (('ru', _('русский')),
                   ('en', _('английский')),
                   ('fr', _('французский')),
                   ('ge', _('немецкий')))

    courseChoices = ((1, _('1 бак')),
                     (2, _('2 бак')),
                     (3, _('3 бак')),
                     (4, _('4 бак')),
                     (5, _('1 маг')),
                     (6, _('2 маг')),
                     (7, _('межкурсовой')),
                     )

    user = models.ForeignKey(User)
    author = models.ManyToManyField(Author, verbose_name=_('авторы'))
    prof = models.ManyToManyField(Teacher, verbose_name=_('руководители'))
    year = models.IntegerField(validators=[MinValueValidator(2010)], verbose_name=_('год'))
    title = models.CharField(max_length=200, verbose_name=_('название на русском'))
    title_en = models.CharField(max_length=200, verbose_name=_('название на английском'))
    keywords = models.TextField(verbose_name=_('ключевые слова на русском'), blank=True, null=True)
    keywords_en = models.TextField(verbose_name=_('ключевые слова на английском'), blank=True, null=True)
    abstract = models.TextField(verbose_name=_('аннотация на русском'), blank=True, null=True)
    abstract_en = models.TextField(verbose_name=_('аннотация на английском'), blank=True, null=True)
    mark = models.IntegerField(verbose_name=_('оценка'), blank=True, null=True,
                               validators=[MinValueValidator(0), MaxValueValidator(10)])
    file = models.ForeignKey(DictFile, blank=True, null=True, verbose_name=_('файл'))
    link = models.CharField(max_length=1000, blank=True, null=True, verbose_name=_('ссылка'))
    field = models.ManyToManyField(Field, verbose_name=_('сфера'), blank=True)
    lang = models.CharField(max_length=2, choices=langChoices, verbose_name=_('язык работы'), default='ru')
    form = models.CharField(max_length=8, choices=formChoices, verbose_name=_('тип работы'))
    course = models.IntegerField(choices=courseChoices, verbose_name=_('курс'))
    editable = models.BooleanField(default=True)
    visible_to_all = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return '{0} {1}'.format(self.title, self.year)

    def delete(self, *args, **kwargs):
        # todo если удалять проект, то соответствующий DictFile не удаляется..
        if self.file:
            self.file.delete()
        super(Project, self).delete()

    @property
    def project_type(self):
        return dict(self.formChoices)[self.form]

    @property
    def course_verbose(self):
        return dict(self.courseChoices)[self.course]
