from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите почту")
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О.", help_text="Введите Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, help_text="Добавьте комментарий")

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

    def __str__(self):
        return f"{self.full_name} <{self.email}>"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма", help_text="Введите тему")
    body = models.TextField(verbose_name="Тело письма", help_text="Введите текст сообщения")

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return self.subject
