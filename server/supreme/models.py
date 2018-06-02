from django.db import models
# Create your models here.
ACTIONS = (('1', 'Start'),
           ('0', 'STOP'),
           ('-1', 'PAUSE'))


class Profile(models.Model):
    name = models.CharField(max_length=64)
    phone = models.IntegerField()
    email = models.EmailField()
    card_number = models.IntegerField()
    cvv = models.IntegerField()
    expiry = models.IntegerField()
    year = models.IntegerField()
    address1 = models.CharField(max_length=32)
    address2 = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=32)
    payment_option = models.CharField(max_length=32)
    country = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class SupremeTask(models.Model):
    profile = models.ForeignKey(Profile)
    size = models.CharField(max_length=32)
    color = models.CharField(max_length=16)
    product = models.CharField(max_length=16, default=" ")
    progress = models.CharField(max_length=16, default="Initialise!")
    action = models.CharField(choices=ACTIONS, max_length=4, default='0')
    keyword = models.CharField(max_length=32)
    category = models.CharField(max_length=32)
    timer = models.IntegerField()
    proxy = models.CharField(max_length=32)

    def long_task(self):
        self.progress = "Working!"
        self.save()
        while True:
            pass

    def __str__(self):
        return self.profile.name + self.keyword


class Proxy(models.Model):
    name = models.CharField(max_length=32)
    status = models.CharField(choices=(('success', 'success'), ('error', 'error')), max_length=10, default='success')
    speed = models.CharField(max_length=10, default=80)
    action = models.CharField(choices=ACTIONS, max_length=10, default='0')

    def __str__(self):
        return self.name


class Setting(models.Model):
    key = models.CharField(max_length=128)
    moniter = models.IntegerField(default=0)
    checkout_delay = models.IntegerField(default=0)
    gmail = models.CharField(max_length=32, default="", blank=True)
    mode = models.CharField(max_length=10, choices=(('headless', 'HEADLESS'), ('normal', 'NORMAL')), default='headless')

    def __str__(self):
        return self.key
