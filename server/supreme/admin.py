from django.contrib import admin

# Register your models here.
from supreme.models import *

admin.site.register(Profile)
admin.site.register(SupremeTask)
admin.site.register(Proxy)
admin.site.register(Setting)