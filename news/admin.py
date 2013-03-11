from news.models import *

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['name'] }),
    )
admin.site.register(Category, CategoryAdmin)

class EntryAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Entry'), {'fields': ('title', 'body')}),
	(_('Category'), {'fields': ('category', )}),
        (_('Date published'), {'fields': ('pub_date', )}),
        (_('Options'), { 'fields': ('draft',)}),
    )

    list_display = ('title', 'pub_date')

    def save_form(self, request, form, change):
        form.instance.author = request.user
        return super(EntryAdmin, self).save_form(request, form, change)

admin.site.register(Entry, EntryAdmin)
