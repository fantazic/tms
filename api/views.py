from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from datetime import timedelta, datetime

from .models import Task, Setting


def signup(request):
    username = request.POST['username']
    password = request.POST['password']

    user = User.objects.filter(username=username)
    if len(user) > 0:
        response = {'message': ' Username is already in use'}
    else:
        User.objects.create_user(username=username, password=password)

        user = authenticate(username=username, password=password)
        Setting.objects.create(user=user, preferred_hour=0)

        login(request, user)
        date = timezone.now().date()
        tasks = _get_tasks(user, date)
        dates = _get_dates(user, date)

        response = {'message': 'Success', 'date': date, 'tasks': tasks, 'dates': dates, 'preferredHour': 0}

    return JsonResponse(response)


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        date = timezone.now().date()
        tasks = _get_tasks(user, date)
        dates = _get_dates(user, date)

        response = {'message': 'Success', 'status': user.is_active, 'date': date, 'tasks': tasks, 'dates': dates,
                    'preferredHour': user.setting.preferred_hour}
    else:
        user = User.objects.filter(username=username)
        if len(user) > 0:
            response = {'message': 'Wrong Password'}
        else:
            response = {'message': 'Wrong Username'}

    return JsonResponse(response)


def logout_user(request):
    logout(request)

    return JsonResponse({'message': 'Success'})


def me(request):
    if request.user.is_authenticated():
        date = timezone.now().date()
        tasks = _get_tasks(request.user, date)
        dates = _get_dates(request.user, date)

        response = {'message': 'Login', 'user': {'username': request.user.username, 'password': ''},
                    'date': date, 'tasks': tasks, 'dates': dates, 'preferredHour': request.user.setting.preferred_hour}
    else:
        response = {'message': 'Logout'}

    return JsonResponse(response)


def update_task(request):
    if request.user.is_authenticated():
        task_id = request.POST['task_id']
        note = request.POST['note']
        date = request.POST['date']
        hour = request.POST['hour']
        action = request.POST['action']

        if action == 'Edit':
            Task.objects.filter(pk=task_id).update(note=note, date=date, hour=hour)
        elif action == 'Delete':
            Task.objects.get(pk=task_id).delete()

        tasks = _get_tasks(request.user, date)
        dates = _get_dates(request.user, date)

        response = {'message': 'Success', 'date': date, 'tasks': tasks, 'dates': dates}
    else:
        response = {'message': 'Login first'}

    return JsonResponse(response)


def add_task(request):
    if request.user.is_authenticated():
        date = request.POST['date']
        hour = request.POST['hour']
        note = request.POST['note']

        task = request.user.task_set.create(date=date, hour=hour, note=note)
        tasks = _get_tasks(request.user, date)
        dates = _get_dates(request.user, date)

        if task:
            response = {'message': 'Success', 'date': date, 'tasks': tasks, 'dates': dates}
        else:
            response = {'message': 'The task creation failed'}
    else:
        response = {'message': 'Login first'}

    return JsonResponse(response)


def get_tasks(request):
    if request.user.is_authenticated():
        date = request.GET.get('date', timezone.now().date())
        tasks = _get_tasks(request.user, date)

        response = ({'message': 'Success', 'tasks': tasks, 'date': date})
    else:
        response = ({'message': 'Login first'})

    return JsonResponse(response)


def get_dates(request):
    if request.user.is_authenticated():
        date = request.GET.get('date', timezone.now().date())
        dates = _get_dates(request.user, date)

        response = ({'message': 'Success', 'dates': dates, 'date': date})
    else:
        response = ({'message': 'Login first'})

    return JsonResponse(response)


def set_hour(request):
    if request.user.is_authenticated():
        hour = int(request.POST.get('hour', 0))
        date = request.POST['date']

        Setting.objects.filter(pk=request.user).update(preferred_hour=hour)
        dates = _get_dates(request.user, date)

        response = ({'message': 'Success', 'dates': dates})
    else:
        response = ({'message': 'Login first'})

    return JsonResponse(response)


def export(request):
    if request.user.is_authenticated():
        date_from = request.GET['from']
        date_to = request.GET['to']

        dates = _get_date_range(date_from, date_to)

        export_dates = [{'date': date, 'tasks': _get_tasks(request.user, date),
                         'totalHours': _get_total_hours(_get_tasks(request.user, date))} for date in dates]

        response = ({'message': 'Success', 'exportDates': export_dates})
    else:
        response = ({'message': 'Login first'})

    return JsonResponse(response)


def _get_tasks(user, date):
    tasks = [task.to_json() for task in Task.objects.filter(user=user, date=date)]

    return tasks


def _get_dates(user, date):
    if isinstance(date, basestring):
        date = datetime.strptime(date, '%Y-%m-%d').date()

    days = range(-3, 4)
    dates = [{'date': date + timedelta(days=d), 'under': user.setting.is_under(date + timedelta(days=d))}
             for d in days]

    return dates


def _get_date_range(date_from, date_to):
    d1 = datetime.strptime(date_from, '%Y-%m-%d').date()
    d2 = datetime.strptime(date_to, '%Y-%m-%d').date()

    delta = d2 - d1

    if delta.days < 0:
        return []

    dates = []
    for i in range(delta.days + 1):
        dates.append(d1 + timedelta(days=i))

    return dates


def _get_total_hours(tasks):
    return sum([task['hour'] for task in tasks])
