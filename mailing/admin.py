from django.contrib import admin
from .models import Subscriber, Message, MailingModel


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment', 'owner')
    search_fields = ('email', 'full_name', 'owner')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body', 'owner')
    list_filter = ('subject', 'body', 'owner')
    search_fields = ('subject',)


#admin.site.register(MailingModel)
@admin.register(MailingModel)
class MailingModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'beginning_sending', 'end_sending', 'is_active', 'owner')
    list_filter = ('is_active', 'owner')
