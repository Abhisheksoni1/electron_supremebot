import json
from django.http import HttpResponse
from django.shortcuts import render
import tasker
from supreme.management.commands.manage_worker import settings
# Create your views here.s
from django.views.decorators.csrf import csrf_exempt
import requests
from supreme.forms import LoginForm, SaveTaskForm, SaveProfileForm, SaveProxyForm, SaveSettingForm, EditProfileForm, \
    EditTaskForm
from supreme.models import SupremeTask, Profile, Setting, Proxy
import time

from supreme.utils import test_proxy

SIZE_DICT = {'54150': 'small',
             }


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = json.loads(requests.post("https://supreme-admin.herokuapp.com/register_key",
                                            data={'key': form.cleaned_data['password']}).text)
            if data.get('success'):
                Setting.objects.create(key=form.cleaned_data['password'])
                return dashboard(request)
            elif data.get('error'):

                return render(request, "login.html", {'error': data.get('error')})

        else:
            return render(request, "login.html", {'error': "Error!!  please enter the license key to enter into bot"})
    return render(request, "login.html")


@csrf_exempt
def deactivate(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = json.loads(requests.post("https://supreme-admin.herokuapp.com/deactivate_key",
                                            data={'key': form.cleaned_data['password']}).text)
            if data.get('success'):
                Setting.objects.all().delete()
                return HttpResponse(json.dumps({'status': 200}), content_type='application/json')
            elif data.get('error'):
                return HttpResponse(json.dumps({'status': 400}), content_type='application/json')

    return HttpResponse(json.dumps({'status': 400}), content_type='application/json')


def dashboard(request):
    s = Setting.objects.all()
    if s.count():
        return render(request, "dashboard.html", {'setting': s[0]})
    else:
        return login(request)


def task(request):
    tasks = SupremeTask.objects.all()
    return render(request, "task.html", {'tasks': tasks})


def newtask(request):
    tasks = SupremeTask.objects.all()
    profiles = Profile.objects.all()
    proxies = Proxy.objects.all()
    return render(request, "edittask.html", {'tasks': tasks,
                                             'profiles': profiles,
                                             'proxies': proxies})


def get_task(request, id=None):
    if id:
        task = SupremeTask.objects.get(id=id)
        content = {
            'size': task.size,
            'color': task.color,
            'keyword': task.keyword,
            'category': task.category,
            'timer': task.timer,
            'proxy': task.proxy,
            'profile': task.profile.name
        }
        return HttpResponse(json.dumps(content), content_type='application/json')
    else:
        tasks = SupremeTask.objects.all()
        content = {}
        for task in tasks:
            content[task.id] = task.progress
        return HttpResponse(json.dumps(content), content_type='application/json')


def get_profile(request, id):
    profile = Profile.objects.get(id=id)
    content = {
        'address1': profile.address1,
        'address2': profile.address2,
        'city': profile.city,
        'zip_code': profile.zip_code,
        'payment_option': profile.payment_option,
        'country': profile.country,
        'name': profile.name,
        'card_number': profile.card_number,
        'month': profile.expiry,
        'year': profile.year,
        'cvv': profile.cvv,
        'phone': profile.phone,
        'email': profile.email
    }
    return HttpResponse(json.dumps(content), content_type='application/json')


@csrf_exempt
def save_task(request):
    if request.method == "POST":
        try:
            form = SaveTaskForm(request.POST)
            if form.is_valid():
                user_profile = Profile.objects.get(id=form.cleaned_data['profile'])
                SupremeTask.objects.create(profile=user_profile, size=form.cleaned_data['size'],
                                           color=form.cleaned_data['color'],
                                           keyword=form.cleaned_data['keyword'], category=form.cleaned_data['category'],
                                           timer=int(form.cleaned_data['timer']), proxy=form.cleaned_data['proxy'])
                return HttpResponse(json.dumps({'status': 200}), content_type='application/json')
            else:
                # print(form.errors)
                return HttpResponse(json.dumps({'status': 400, 'error': form.errors}), content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps({'status': 400, 'error': 'fill all details'}),
                                content_type='application/json')
    else:
        HttpResponse(json.dumps({'status': 403, 'error': 'no get method allow'}), content_type='application/json')


@csrf_exempt
def edit_task(request):
    if request.method == "POST":
        form = EditTaskForm(request.POST)
        if form.is_valid():
            user_profile = Profile.objects.get(id=form.cleaned_data['profile'])
            supremetask = SupremeTask.objects.get(id=form.cleaned_data['id'])
            supremetask.profile = user_profile
            supremetask.size = form.cleaned_data['size']
            supremetask.color = form.cleaned_data['color']
            supremetask.keyword = form.cleaned_data['keyword']
            supremetask.category = form.cleaned_data['category']
            supremetask.timer = int(form.cleaned_data['timer'])
            supremetask.proxy = form.cleaned_data['proxy']
            supremetask.save()
            return HttpResponse(json.dumps({'status': 200}), content_type='application/json')
        else:
            print(form.errors)
    return HttpResponse(json.dumps({'status': 400, 'error': 'fill all details'}), content_type='application/json')


def profile(request):
    profiles = Profile.objects.all()
    return render(request, "profile.html", {'profiles': profiles})


@csrf_exempt
def save_profile(request):
    if request.method == "POST":
        form = SaveProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'status': 200}), content_type='application/json')
    return HttpResponse(json.dumps({'status': 400, 'error': 'fill all details'}), content_type='application/json')


@csrf_exempt
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():
            userprofile = Profile.objects.get(id=form.cleaned_data['id'])
            userprofile.name = form.cleaned_data['name']
            userprofile.phone = form.cleaned_data['phone']
            userprofile.email = form.cleaned_data['email']
            userprofile.card_number = form.cleaned_data['card_number']
            userprofile.cvv = form.cleaned_data['cvv']
            userprofile.expiry = form.cleaned_data['expiry']
            userprofile.year = form.cleaned_data['year']
            userprofile.address1 = form.cleaned_data['address1']
            userprofile.address2 = form.cleaned_data['address2']
            userprofile.city = form.cleaned_data['city']
            userprofile.zip_code = form.cleaned_data['zip_code']
            userprofile.payment_option = form.cleaned_data['payment_option']
            userprofile.country = form.cleaned_data['country']
            userprofile.save()
            return HttpResponse(json.dumps({'status': 200}), content_type='application/json')
        else:
            print(form.errors)
    return HttpResponse(json.dumps({'status': 400, 'error': 'fill all details'}), content_type='application/json')


@csrf_exempt
def save_setting(request):
    if request.method == "POST":
        form = SaveSettingForm(request.POST)
        if form.is_valid():
            setting = Setting.objects.get(key=form.cleaned_data['key'])
            setting.moniter = form.cleaned_data['moniter']
            setting.checkout_delay = form.cleaned_data['checkout_delay']
            setting.gmail = form.cleaned_data['gmail']
            setting.mode = form.cleaned_data['mode']
            setting.save()
            return HttpResponse(json.dumps({'status': 200}), content_type='application/json')
    return HttpResponse(json.dumps({'status': 400, 'error': 'fill all details'}), content_type='application/json')


def setting(request):
    setting = Setting.objects.all()[0]
    return render(request, "setting.html", {'setting': setting})


@csrf_exempt
def add_proxy(request):
    if request.method == "POST":
        form = SaveProxyForm(request.POST)
        if form.is_valid():
            speed = test_proxy(form.cleaned_data['name'])
            proxy = Proxy.objects.create(name=form.cleaned_data['name'],
                                         status='error' if speed == 0 else 'success',
                                         speed=speed)
            return HttpResponse(json.dumps({'status': 200}), content_type='application/json')
    return HttpResponse(json.dumps({'status': 400, 'error': 'fill all details'}), content_type='application/json')


def proxy(request):
    proxy = Proxy.objects.all()
    return render(request, "proxy.html", {'proxies': proxy})


def start_proxy(request, id=None):
    if id:
        try:
            p = Proxy.objects.get(id=id)
            speed = test_proxy(p.name)
            p.status = 'error' if speed == 0 else 'success'
            p.speed = speed
            # start action for proxy
            p.action = '1'
            p.save()
            # # todo add your logic here
            return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')
        except Exception as e:
            print(e)
            HttpResponse(json.dumps({'task': e}), content_type='application/json')

    else:
        p = Proxy.objects.all()
        for tak in p:
            # todo add your logic here
            pass
        return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')


def stop_proxy(request, id=None):
    if id:
        try:
            p = Proxy.objects.get(id=id)
            # todo add your logic here
            return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')
        except Exception as e:
            print(e)

    else:
        p = Proxy.objects.all()
        for task in p:
            # todo add your logic here
            pass
        return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')


def delete_proxy(request, id=None):
    if id:
        p = Proxy.objects.get(id=id)
        p.delete()
        # todo before deleting also stop task if worker running
        return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')

    else:
        p = Proxy.objects.all().delete()
        # todo before deleting also stop task if worker running
        return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')


def start_task(request, id=None):
    if id:
        try:
            supremetask = SupremeTask.objects.get(id=id)
            supremetask.progress = "Started"
            supremetask.save()
            time.sleep(3)
            # query = {"category":"tops-sweaters","size":54159,"color":"Black"}
            # del_details = {"firstname":"gaurav","lastname":"singh","email":"gaurav@moonraft.com","phone":"9898989898","state":" 愛知県","city":"asdf","add":"ffhsyfgshfgsgfghsgdfhdf","zip":"676498"}
            # payment_details = {"method":"jcb","cardno":"7787987897667031","expmonth":"01","expyear":"2021","cvv":"569"}
            # driver, loadscript, script = tasker.init_task(query, del_details, payment_details)
            # tasker.start_task(driver, query['color'], query['size'], loadscript, script)
            # # todo add your logic here
            return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')
        except Exception as e:
            print(e)
            HttpResponse(json.dumps({'task': e}), content_type='application/json')

    else:
        tasks = SupremeTask.objects.all()
        for tak in tasks:
            tak.progress = "Started"
            tak.save()
            # todo add your logic here

        return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')


def stop_task(request, id=None):
    if id:
        try:
            supremetask = SupremeTask.objects.get(id=id)
            supremetask.progress = "Stopped"
            supremetask.save()
            # settings.TASKS_OUTPUT[id][0].close()
            # todo add your logic here
            return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')
        except Exception as e:
            print(e)

    else:
        tasks = SupremeTask.objects.all()
        for ta in tasks:
            ta.progress = "Stopped"
            ta.save()
            # todo add your logic here
            pass
        return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')


def delete_task(request, id=None):
    if id:
        task = SupremeTask.objects.get(id=id)

        # once task delete we need to handle this in try catch block for our worker
        task.delete()
        # todo before deleting also stop task if worker running
        return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')

    else:
        tasks = SupremeTask.objects.all().delete()
        # todo before deleting also stop task if worker running
        return HttpResponse(json.dumps({'task': "ok"}), content_type='application/json')


def delete_profile(request, id=None):
    if id:
        prof = Profile.objects.get(id=id)
        prof.delete()
        # todo before deleting also stop task if worker running
        return HttpResponse(json.dumps({'profile': "ok"}), content_type='application/json')

    else:
        prof = Profile.objects.all().delete()
        # todo before deleting also stop task if worker running
        return HttpResponse(json.dumps({'profile': "ok"}), content_type='application/json')
