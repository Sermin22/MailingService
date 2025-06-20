from django.db import models
from users.models import CustomUser


# Модель Получатель рассылки (подписчик)
class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите почту")
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О.", help_text="Введите Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, help_text="Добавьте комментарий")
    owner = models.ForeignKey(
        CustomUser,
        verbose_name='Владелец',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

    def __str__(self):
        return f"{self.full_name} <{self.email}>"


# Модель Сообщение
class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма", help_text="Введите тему")
    body = models.TextField(verbose_name="Тело письма", help_text="Введите текст сообщения")
    owner = models.ForeignKey(
        CustomUser,
        verbose_name='Владелец',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return self.subject


# Модель Рассылка
class MailingModel(models.Model):
    CREATED = "created"
    STARTED = "started"
    FINISHED = "finished"

    STATUSES_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (FINISHED, "Завершена"),
    ]
    beginning_sending = models.DateTimeField(
        verbose_name="Начало рассылки",
        help_text="Укажите время в формате ДД.ММ.ГГГГ ЧЧ:ММ:СС"
    )
    end_sending = models.DateTimeField(
        verbose_name="Конец рассылки",
        help_text="Укажите время в формате ДД.ММ.ГГГГ ЧЧ:ММ:СС"
    )
    status = models.CharField(max_length=20, choices=STATUSES_CHOICES, default=CREATED, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение", related_name="messages")
    subscriber = models.ManyToManyField(
        Subscriber,
        verbose_name="Получатель рассылки",
        related_name="subscribers",
        help_text="Удерживайте “Control“ (или “Command“ на Mac), чтобы выбрать несколько значений."
    )
    is_active = models.BooleanField(
        verbose_name="Активна",
        default=True,
    )
    owner = models.ForeignKey(
        CustomUser,
        verbose_name='Владелец',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-beginning_sending"]
        permissions = [
            ("can_disable_mailing", "Can disable mailing"),
        ]

    def __str__(self):
        return f"Рассылка #{self.pk} - {self.status}"


# Модель попытка рассылки
class MailingAttempt(models.Model):
    SUCCESSFULLY = "successfully"
    NOT_SUCCESSFULL = "not_successful"

    STATUSES_CHOICES = [
        (SUCCESSFULLY, "Успешно"),
        (NOT_SUCCESSFULL, "Не успешно"),
    ]

    date_and_time = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    status = models.CharField(max_length=20, choices=STATUSES_CHOICES, verbose_name="Статус отправки")
    server_mail_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(MailingModel, on_delete=models.CASCADE, related_name='mailings')

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-date_and_time"]

    def __str__(self):
        return f"{self.date_and_time} - {self.status}"
