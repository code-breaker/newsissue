from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.conf import settings

from markdown import markdown

from datetime import datetime, timedelta
import re

class short_description(object):
    def __init__(self, desc):
        self.desc = desc
    def __call__(self, func):
        func.short_description = self.desc
        return func


class PublishedEntryManager(models.Manager):
    def get_query_set(self):
        return super(PublishedEntryManager, self).get_query_set().filter(draft=False, pub_date__lte=datetime.now())

class Category(models.Model):
    name = models.CharField('category name', max_length=20, unique=True)
    def __unicode__(self):
        return self.name
class Entry(models.Model):
    title = models.CharField(max_length=65)
    author = models.ForeignKey(User, blank=True)
    body = models.TextField()
    body_html = models.TextField(blank=True)
    category = models.ForeignKey(Category, blank=True)
    pub_date = models.DateTimeField(default=datetime.now)
    draft = models.BooleanField(default=False)
    views = models.IntegerField(max_length=11,default=0 )
    good = models.PositiveIntegerField(blank=True, default=0)
    bad = models.PositiveIntegerField(blank=True, default=0)
    
    objects = models.Manager()
    published = PublishedEntryManager()
    class Meta:
        verbose_name = "entry"
	verbose_name_plural = 'entries'
    def __unicode__(self):
        return self.title

    def next(self):
        if not hasattr(self, '_next'):
            try:
                self._next = Entry.objects.filter(pk__gt=self.pk)[0]
            except IndexError:
                self._next = None

        return self._next

    def prev(self):
        if not hasattr(self, '_prev'):
            try:
                self._prev = Entry.objects.filter(pk__lt=self.pk)[0]
            except IndexError:
                self._prev = None

        return self._prev


    def save(self, *args, **kwargs):
        self.body_html = markdown(self.body)
        published_now = False
        if not self.draft and self.pub_date < datetime.now() + timedelta(seconds=5):
            if not self.pk or Entry.objects.get(pk=self.pk).draft != self.draft:
                self.pub_date = datetime.now()
                published_now = True

        super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return settings.URL + 'entry/%s/' % self.id

    @property
    def description(self):
        return mark_safe(self.body_html)

    @property
    def slug_generator(self):
        return self.title





