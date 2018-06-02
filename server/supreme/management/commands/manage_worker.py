from django.core.management import BaseCommand
from django.forms import model_to_dict
from time import sleep
from supreme.models import SupremeTask
from django.conf import settings
import tasker
import threading


class Command(BaseCommand):
    help = 'start captcha server to bypass it'

    def handle(self, *args, **options):
        while True:
            tasks = SupremeTask.objects.all()
            for i in tasks:
                if not settings.CURRENT_TASK.get(i.id):
                    settings.CURRENT_TASK[i.id] = i
                    threading.Thread(target=tasker.manage_task, args=[i.id]).start()
                    # query = {"category":"accessories","size":50894,"color":"Black"}
                    # del_details = {"firstname":"gaurav","lastname":"singh","email":"gaurav@moonraft.com","phone":"9898989898","state":" 愛知県","city":"asdf","add":"ffhsyfgshfgsgfghsgdfhdf","zip":"676498"}
                    # payment_details = {"method":"jcb","cardno":"7787987897667031","expmonth":"01","expyear":"2021","cvv":"569"}
                    # # settings.TASKS_OUTPUT[i.id] = list(init_task(query, del_details, payment_details))
                    #
                    # print(settings.CURRENT_TASK)
                    # # print(settings.TASKS_OUTPUT)
                    # print("++++++++++++++++++++++++++++++++++++++")
            sleep(5)