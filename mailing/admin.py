from django.contrib import admin
from .models import Subscriber, Message, MailingModel


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment',)
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body',)
    list_filter = ('subject', 'body',)
    search_fields = ('subject',)


admin.site.register(MailingModel)
