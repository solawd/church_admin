__author__ = 'dkarchmer@gmail.com'
# slightly edited by solawd@gmail.com

from django.conf import settings
from django.core.management.base import BaseCommand
from members.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        if CustomUser.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = 'admin'
                print('Creating account for %s (%s)' % (username, email))
                admin = CustomUser.objects.create_superuser(email=email, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')