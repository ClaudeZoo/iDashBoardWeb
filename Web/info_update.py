import datetime
from django.contrib.sessions.models import Session
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from Web.models import VM
from Web.models import Host


def update_info(request):
    if 'uuid' in request.POST and request.POST['uuid']:
        uuid = request.POST['uuid'].strip('\n')
        try:
            vm = VM.objects.get(uuid=uuid)
            info = vm.info
        except ObjectDoesNotExist:
            return HttpResponse('error')
    elif 'IPAddress' in request.POST and request.POST['IPAddress']:
        ip = request.POST['IPAddress'].split('\n')[0]
        try:
            host = Host.objects.get(info__wan_ip=ip)
            info = host.info
        except ObjectDoesNotExist:
            return HttpResponse('error')
    else:
        return HttpResponse('error')
    if 'stateInfo' in request.POST and request.POST['stateInfo']:
        state_info = eval(request.POST['stateInfo'])
        info.update_info(state_info)
        info.save()
    t = datetime.datetime.now()
    s = Session.objects.filter(expire_date__gte=t)
    response = HttpResponse()
    if len(s) != 0:
        response["content"] = "someone"
    else:
        response.write("noone")
        response["content"] = "noone"
    return response


def hello_server(request):
    if 'uuid' in request.POST and request.POST['uuid']:
        uuid = request.POST['uuid'].strip('\n')
        try:
            vm = VM.objects.get(uuid=uuid)
            vm.info.save()
        except ObjectDoesNotExist:
            print e
    elif 'IPAddress' in request.POST and request.POST['IPAddress'] and 'Port' in request.POST and request.POST['Port']:
        ip = request.POST['IPAddress'].split('\n')[0]
        port = request.POST['Port']
        try:
            host = Host.objects.get(info__wan_ip=ip)
            host.vm_manager_port = port
            host.save()
        except ObjectDoesNotExist:
            return
    else:
        return
    r = HttpResponse()
    r.write("hello world")
    r["content"] = "helloworld"
    return r