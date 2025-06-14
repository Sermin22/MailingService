from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.forms import SubscriberForm, MessageForm
from mailing.models import Subscriber, Message


class HomeView(TemplateView):
    template_name = 'mailing/home.html'


class SubscriberListView(ListView):
    model = Subscriber
    template_name = 'mailing/subscriber_list.html'  # можно не указывать, это стандартный путь
    context_object_name = 'subscriber_list'  # можно не указывать, если использовать это
    # стандартное название в шаблоне 'subscriber_list' или 'object_list'


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = 'mailing/subscriber_detail.html'  # можно не указывать, это стандартный путь
    context_object_name = 'subscriber'  # можно не указывать, стандартное название в шаблоне 'subscriber'


class SubscriberCreateView(CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'mailing/subscriber_form.html'
    success_url = reverse_lazy('mailing:subscriber_list')


class SubscriberUpdateView(UpdateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'mailing/subscriber_form.html'
    context_object_name = 'subscriber'

    def get_success_url(self):
        return reverse_lazy('mailing:subscriber_detail', kwargs={'pk': self.object.pk})


class SubscriberDeleteView(DeleteView):
    model = Subscriber
    template_name = 'mailing/subscriber_confirm_delete.html'
    context_object_name = 'subscriber'
    success_url = reverse_lazy('mailing:subscriber_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'message_list'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    context_object_name = 'message'

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mailing:message_list')
