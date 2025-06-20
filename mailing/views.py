from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from mailing.forms import SubscriberForm, MessageForm, MailingModelForm
from mailing.models import Subscriber, Message, MailingModel, MailingAttempt
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group


class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = MailingModel.objects.count()
        context['active_mailings'] = MailingModel.objects.filter(status=MailingModel.STARTED).count()
        context['unique_subscribers'] = Subscriber.objects.count()  # Если email уникальный в модели
        return context


class SubscriberListView(LoginRequiredMixin, ListView):
    model = Subscriber
    template_name = 'mailing/subscriber_list.html'  # можно не указывать, это стандартный путь
    context_object_name = 'subscriber_list'  # можно не указывать, если использовать это
    # стандартное название в шаблоне 'subscriber_list' или 'object_list'

    def get_queryset(self):
        user = self.request.user
        # Проверяем, состоит ли пользователь членом в группе "Менеджеры"
        managers_group = Group.objects.get(name="Managers")
        if managers_group in user.groups.all():
            # Менеджеры видят всех подписчиков
            return Subscriber.objects.all()
        elif user.is_superuser:
            # Суперпользователи тоже видят всех подписчиков
            return Subscriber.objects.all()
        else:
            # Пользователи видят только своих собственных подписчиков
            return Subscriber.objects.filter(owner=user)


class SubscriberDetailView(LoginRequiredMixin, DetailView):
    model = Subscriber
    template_name = 'mailing/subscriber_detail.html'  # можно не указывать, это стандартный путь
    context_object_name = 'subscriber'  # можно не указывать, стандартное название в шаблоне 'subscriber'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        managers_group = Group.objects.get(name="Managers")
        # Проверяем, является ли пользователь менеджером или суперпользователем
        if managers_group in user.groups.all() or user.is_superuser:
            return obj
        # Обычные пользователи видят только своих подписчиков
        elif user == obj.owner:
            return obj
        # Запрещаем доступ остальным пользователям
        raise PermissionDenied


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'mailing/subscriber_form.html'
    success_url = reverse_lazy('mailing:subscriber_list')

    def form_valid(self, form):
        subscriber = form.save()
        user = self.request.user
        subscriber.owner = user
        subscriber.save()
        return super().form_valid(form)


class SubscriberUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'mailing/subscriber_form.html'
    context_object_name = 'subscriber'

    def get_success_url(self):
        return reverse_lazy('mailing:subscriber_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == obj.owner:
            return obj
        raise PermissionDenied

    # def form_valid(self, form):
    #     subscriber = self.get_object()
    #     user = self.request.user
    #     # Если пользователь — владелец, разрешить всё
    #     if subscriber.owner == user:
    #         return super().form_valid(form)


class SubscriberDeleteView(LoginRequiredMixin, DeleteView):
    model = Subscriber
    template_name = 'mailing/subscriber_confirm_delete.html'
    context_object_name = 'subscriber'
    success_url = reverse_lazy('mailing:subscriber_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == obj.owner:
            return obj
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'message_list'

    def get_queryset(self):
        user = self.request.user
        # Проверяем, состоит ли пользователь членом в группе "Менеджеры"
        managers_group = Group.objects.get(name="Managers")
        if managers_group in user.groups.all():
            # Менеджеры видят всех подписчиков
            return Message.objects.all()
        elif user.is_superuser:
            # Суперпользователи тоже видят всех подписчиков
            return Message.objects.all()
        else:
            # Пользователи видят только своих собственных подписчиков
            return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        managers_group = Group.objects.get(name="Managers")
        # Проверяем, является ли пользователь менеджером или суперпользователем
        if managers_group in user.groups.all() or user.is_superuser:
            return obj
        # Обычные пользователи видят только своих подписчиков
        elif user == obj.owner:
            return obj
        # Запрещаем доступ остальным пользователям
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    context_object_name = 'message'

    def get_success_url(self):
        return reverse_lazy('mailing:message_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == obj.owner:
            return obj
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == obj.owner:
            return obj
        raise PermissionDenied


class MailingModelListView(LoginRequiredMixin, ListView):
    model = MailingModel
    template_name = 'mailing/mailingmodel_list.html'
    context_object_name = 'mailingmodel_list'

    def get_queryset(self):
        user = self.request.user
        # Проверяем, состоит ли пользователь членом в группе "Менеджеры"
        managers_group = Group.objects.get(name="Managers")
        if managers_group in user.groups.all():
            # Менеджеры видят всех подписчиков
            return MailingModel.objects.all()
        elif user.is_superuser:
            # Суперпользователи тоже видят всех подписчиков
            return MailingModel.objects.all()
        else:
            # Пользователи видят только своих собственных подписчиков
            return MailingModel.objects.filter(owner=user)



class MailingModelDetailView(LoginRequiredMixin, DetailView):
    model = MailingModel
    template_name = 'mailing/mailingmodel_detail.html'
    context_object_name = 'mailingmodel'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        managers_group = Group.objects.get(name="Managers")
        # Проверяем, является ли пользователь менеджером или суперпользователем
        if managers_group in user.groups.all() or user.is_superuser:
            return obj
        # Обычные пользователи видят только своих подписчиков
        elif user == obj.owner:
            return obj
        # Запрещаем доступ остальным пользователям
        raise PermissionDenied


class MailingModelCreateView(LoginRequiredMixin, CreateView):
    model = MailingModel
    form_class = MailingModelForm
    template_name = 'mailing/mailingmodel_form.html'
    success_url = reverse_lazy('mailing:mailingmodel_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingModelUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingModel
    form_class = MailingModelForm
    template_name = 'mailing/mailingmodel_form.html'
    context_object_name = 'mailingmodel'

    def get_success_url(self):
        return reverse_lazy('mailing:mailingmodel_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == obj.owner:
            return obj
        raise PermissionDenied


class MailingModelDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingModel
    template_name = 'mailing/mailingmodel_confirm_delete.html'
    context_object_name = 'mailingmodel'
    success_url = reverse_lazy('mailing:mailingmodel_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user == obj.owner:
            return obj
        raise PermissionDenied


class DisableMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Получаем объект модели
        mailing = get_object_or_404(MailingModel, pk=pk)
        # Получаем группу "менеджеры"
        managers_group = Group.objects.get(name="Managers")
        # Проверяем, состоит ли текущий пользователь в группе "менеджеры"
        if managers_group in request.user.groups.all():
            # Если пользователь входит в группу "менеджеры", отключаем рассылку
            mailing.is_active = False
            mailing.save()
            # Подтверждение успешной операции
            messages.success(request, "Рассылка успешно отключена!")
        else:
            # Иначе сообщаем об ошибке
            messages.warning(request, "У вас нет прав отключить рассылку.")
        return redirect('mailing:mailingmodel_list')


class SendingMailingView(LoginRequiredMixin, View):
    '''Класс осуществляющий отправку рассылки и формирующий попытку рассылки — это запись в БД о каждой
    попытке отправки сообщения по рассылке по каждому подписчику'''

    def get(self, request, pk):
        mailing = get_object_or_404(MailingModel, pk=pk)
        # Проверка владелец ли это данной рассылки
        if mailing.owner != request.user:
            messages.warning(request, 'У вас нет прав на управление этой рассылкой.')
            return redirect('mailing:mailingmodel_list')
        date_and_time_now = timezone.now()
        if date_and_time_now > mailing.end_sending:
            messages.warning(request, 'Время отправки рассылки закончилось! '
                                      'Статус рассылки будет изменен!')
            mailing.status = MailingModel.FINISHED
            mailing.save()
        if mailing.status == MailingModel.FINISHED:
            messages.warning(request, 'Нельзя отправить завершённую рассылку.')
            return redirect('mailing:mailingmodel_list')
        return render(request, 'mailing/confirm_send.html', {'mailing': mailing})

    def post(self, request, pk):
        mailing = get_object_or_404(MailingModel, pk=pk)
        subject = mailing.message.subject
        body = mailing.message.body
        subscriber = mailing.subscriber.all()

        emails = [p.email for p in subscriber]

        if emails:
            for email in emails:
                try:
                    send_mail(
                        subject=subject,
                        message=body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    messages.success(request, f'Рассылка отправлена получателю {email}.')
                    mailing.status = MailingModel.STARTED
                    mailing.save()

                    status_mailing_attempt = MailingAttempt.SUCCESSFULLY
                    server_mail_response = 'Письмо отправлено'

                except Exception as e:
                    status_mailing_attempt = MailingAttempt.NOT_SUCCESSFULL
                    server_mail_response = str(e)

                MailingAttempt.objects.create(
                    date_and_time=timezone.now(),
                    status=status_mailing_attempt,
                    server_mail_response=server_mail_response,
                    mailing=mailing
                )
        else:
            messages.warning(request, 'У рассылки нет получателей.')

        return redirect('mailing:mailingmodel_list')


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/mailingattempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        return MailingAttempt.objects.filter(mailing_id=self.kwargs['pk'] )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = MailingModel.objects.get(pk=self.kwargs['pk'])
        return context


# class SendingMailingView(View):
#     '''Класс осуществляющий отправку рассылки'''
#
#     def get(self, request, pk):
#         mailing = get_object_or_404(MailingModel, pk=pk)
#         if mailing.status == 'finished':
#             messages.error(request, 'Нельзя отправить завершённую рассылку.')
#             return redirect('mailing:mailingmodel_list')
#         return render(request, 'mailing/confirm_send.html', {'mailing': mailing})
#
#     def post(self, request, pk):
#         mailing = get_object_or_404(MailingModel, pk=pk)
#         subject = mailing.message.subject
#         body = mailing.message.body
#         subscriber = mailing.subscriber.all()
#
#         emails = [p.email for p in subscriber]
#
#         if emails:
#             send_mail(
#                 subject=subject,
#                 message=body,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=emails,
#                 fail_silently=False,
#             )
#             messages.success(request, f'Рассылка отправлена {len(emails)} получателям.')
#             mailing.status = 'started'
#             mailing.save()
#         else:
#             messages.warning(request, 'У рассылки нет получателей.')
#
#         return redirect('mailing:mailingmodel_list')
