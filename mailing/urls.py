from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (HomeView, SubscriberListView, SubscriberDetailView, SubscriberCreateView,
                           SubscriberUpdateView, SubscriberDeleteView, MessageListView, MessageDetailView,
                           MessageCreateView, MessageUpdateView, MessageDeleteView)

app_name = MailingConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("subscribers/", SubscriberListView.as_view(), name="subscriber_list"),
    path("subscribers/<int:pk>/", SubscriberDetailView.as_view(), name="subscriber_detail"),
    path("subscribers/create/", SubscriberCreateView.as_view(), name="subscriber_create"),
    path("subscribers/<int:pk>/update/", SubscriberUpdateView.as_view(), name="subscriber_update"),
    path("subscribers/<int:pk>/delete/", SubscriberDeleteView.as_view(), name="subscriber_delete"),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
]
