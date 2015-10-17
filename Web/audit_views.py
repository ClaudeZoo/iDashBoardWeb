__author__ = 'Claude'
import json
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from Web.views import is_admin
from Web.models import CreateApplication
from Web.models import DeleteApplication
from Web.models import PortApplication
from Web.create_vm_views import create_vm
from Web.delete_vm_views import delete_vm
from Web.nat_views import execute_nat


@login_required
def audit_view(request):
    is_administer = is_admin(request.user)
    create_application_list = CreateApplication.objects.filter(state='pending')
    create_application_num = create_application_list.count()
    create_applications = list()
    for create_application in create_application_list:
        create_applications.append(create_application.audit_info())

    delete_application_list = DeleteApplication.objects.filter(state='pending')
    delete_application_num = delete_application_list.count()
    delete_applications = list()
    for delete_application in delete_application_list:
        delete_applications.append(delete_application.audit_info())

    port_application_list = PortApplication.objects.filter(state='pending')
    port_application_num = port_application_list.count()
    port_applications = list()
    for port_application in port_application_list:
        port_applications.append(port_application.audit_info())
    return render_to_response('audit.html', locals())


def approve_single_creation(request):
    application_id = int(request.POST.get('id', ''))
    application = create_vm(application_id)
    if application:
        application.reviewer = request.user
        application.save()
        return HttpResponse('1')
    else:
        return HttpResponse('0')


def refuse_single_creation(request):
    application_id = int(request.POST.get('id', ''))
    application = CreateApplication.objects.get(id=application_id)
    application.state = 'rejected'
    application.reviewer = request.user
    application.save()
    return HttpResponse("1")


def approve_all_creation(request):
    application_list = json.loads(request.body.decode())
    for application_id in application_list:
        create_vm(application_id)
    return HttpResponse('1')


def approve_single_delete(request):
    application_id = request.POST.get('id', '')
    application = delete_vm(application_id)
    if application:
        application.reviewer = request.user
        application.save()
        return HttpResponse('1')
    else:
        return HttpResponse('0')


def refuse_single_delete(request):
    application_id = int(request.POST.get('id', ''))
    application = DeleteApplication.objects.get(id=application_id)
    application.state = 'rejected'
    application.reviewer = request.user
    application.save()
    return HttpResponse("1")


def approve_all_delete(request):
    application_list = json.loads(request.body.decode())
    for application_id in application_list:
        delete_vm(application_id)
    return HttpResponse('1')


def approve_single_nat(request):
    application_id = int(request.POST.get('id', ''))
    application = execute_nat(application_id)
    if application:
        application.reviewer = request.user
        application.save()
        return HttpResponse("1")
    else:
        return HttpResponse("0")


def refuse_single_nat(request):
    application_id = int(request.POST.get('id', ''))
    application = PortApplication.objects.get(id=application_id)
    ports = json.loads(application.host.ports_info)
    ports['free'].append(application.host_port)
    ports['used'].remove(application.host_port)
    application.host.ports_info = json.dumps(ports)
    application.host.save()
    application.state = 'rejected'
    application.reviewer = request.user
    application.save()
    return HttpResponse("1")


def approve_all_nat(request):
    pass