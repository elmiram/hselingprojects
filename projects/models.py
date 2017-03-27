from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
import os


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

    def save(self, *args, **kwargs):
        if self.id:
            old = UserProfile.objects.get(pk=self.id)
            if not old.is_approved == self.is_approved and self.is_approved:
                subject = 'Аккаунт подтвержден - Проекты Школы Лингвистики'
                mesagge = 'Здравствуйте, {}!\n\nВаш аккаунт на сайте "Проекты Школы Лингвистики" подтвержден. Теперь вы можете загружать проекты и просматривать файлы работ.\n\nКоманда сайта "Проекты Школы Лингвистики"'.format(self.user.first_name)
                from_email = settings.EMAIL_HOST_USER
                send_mail(subject, mesagge, from_email, [self.user.email], fail_silently=False)
            if not old.is_declined == self.is_declined and self.is_declined:
                subject = 'Аккаунт не подтвержден - Проекты Школы Лингвистики'
                mesagge = 'Здравствуйте, {}!\n\nВаш аккаунт на сайте "Проекты Школы Лингвистики" не подтвержден. Модератор сайта не смог установить, что вы действительно являетесь студентом или сотрудником Школы Лингвистики.\n\nЕсли вы считаете, что это произошло по ошибке, пожалуйста, свяжитесь с модераторами сайта по адресам, указанным в разделе "Помощь".\n\nКоманда сайта "Проекты Школы Лингвистики"'.format(
                    self.user.first_name)
                from_email = settings.EMAIL_HOST_USER
                send_mail(subject, mesagge, from_email, [self.user.email], fail_silently=False)
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
    keywords = models.TextField(verbose_name=_('ключевые слова на русском'))
    keywords_en = models.TextField(verbose_name=_('ключевые слова на английском'))
    abstract = models.TextField(verbose_name=_('аннотация на русском'))
    abstract_en = models.TextField(verbose_name=_('аннотация на английском'))
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
