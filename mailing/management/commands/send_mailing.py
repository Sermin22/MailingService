from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from mailing.models import MailingModel
from django.conf import settings


class Command(BaseCommand):
    help = 'Отправить рассылку вручную по ID через командную строку'

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='ID рассылки')

    def handle(self, *args, **kwargs):
        pk = kwargs['pk']
        try:
            mailing = MailingModel.objects.get(pk=pk)
        except MailingModel.DoesNotExist:
            raise CommandError('Рассылка не найдена.')

        if mailing.status == 'finished':
            self.stdout.write(self.style.ERROR('Рассылка завершена. Отправка невозможна.'))
            return

        subject = mailing.message.subject
        body = mailing.message.body
        subscriber = mailing.subscriber.all()
        emails = [p.email for p in subscriber]

        if not emails:
            self.stdout.write(self.style.WARNING('Нет получателей.'))
            return

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False,
        )
        mailing.status = 'started'
        mailing.save()

        self.stdout.write(self.style.SUCCESS(f'Отправлено {len(emails)} писем.'))

        # отправляется рассылка командой python manage.py send_mailing 7 (7 - это ID рассылки)
        # Если принимать несколько ID, можно использовать nargs='+':
        # parser.add_argument('pk', type=int, nargs='+', help='ID одной или нескольких рассылок')
        # отправляются командой python manage.py send_mailing 3 5 7 (3,5,7 - это ID рассылок)
