__author__ = 'Claude'
from random import randint
from django.utils import timezone
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from Web.models import Host
from Web.models import CreateApplication
from Web.communication import communicate


@login_required
def apply_new_vm(request):
    if request.POST.get('vm_type', '') and request.POST.get('os', '') and request.POST.get('memory', ''):
        os = request.POST.get('os', '')
        memory = int(request.POST.get('memory', ''))
        vm_type = request.POST.get('vm_type', '')
        application = CreateApplication(applicant=request.user, vm_type=vm_type, os=os, memory=memory, state='pending')
        application.save()
        return HttpResponseRedirect('/apply/')
    else:
        return HttpResponseRedirect('/apply/')


def create_vm(application_id):
    host_list = Host.objects.all()
    try:
        application = CreateApplication.objects.get(id=application_id)
        if host_list.count() > 0:
            a = randint(0, host_list.count() - 1)
            host = host_list[a]
            request_dict = dict(request_id=application_id, request_type='new', request_userid=application.applicant.id)
            response = communicate(request_dict, host.ip, host.vm_manager_port)
            if response and response['request_response'] == 'received':
                application.state = 'In line'
                application.host = host
            elif not response:
                application.state = response['request_response']
        else:
            application.state = 'error'
        application.save()
        return application
    except ObjectDoesNotExist:
        return None

