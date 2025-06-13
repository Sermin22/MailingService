from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (
    HomeView,
    SubscriberListView,
    SubscriberDetailView,
    SubscriberCreateView,
    SubscriberUpdateView, SubscriberDeleteView,
)

app_name = MailingConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("subscribers/", SubscriberListView.as_view(), name="subscriber_list"),
    path("subscribers/<int:pk>/", SubscriberDetailView.as_view(), name="subscriber_detail"),
    path("subscribers/create/", SubscriberCreateView.as_view(), name="subscriber_create"),
    path("subscribers/<int:pk>/update/", SubscriberUpdateView.as_view(), name="subscriber_update"),
    path('subscribers/<int:pk>/delete/', SubscriberDeleteView.as_view(), name='subscriber_delete'),
]
