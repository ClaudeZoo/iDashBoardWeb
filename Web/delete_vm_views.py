__author__ = 'Claude'
import json
from django.utils import timezone
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from Web.models import VM
from Web.models import DeleteApplication
from Web.communication import communicate


@login_required
def apply_delete_vm(request):
    user = request.user
    vm_uuid = request.POST.get('uuid', '')
    try:
        vm = VM.objects.get(uuid=vm_uuid)
        if vm.user == user:
            application = DeleteApplication(applicant=user, vm=vm, host=vm.host, state='pending')
            application.save()
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    except ObjectDoesNotExist:
        return HttpResponse('0')


def delete_vm(application_id):
    try:
        application = DeleteApplication.objects.get(id=application_id)
        host = application.host
        request_dict = dict(request_id=application.id, request_type='delete', request_userid=application.applicant.id,
                            vm_name=application.vm.name, vm_uuid=application.vm.uuid)
        response = communicate(request_dict, host.ip, host.vm_manager_port)
        if response and response['request_result'] == 'success':
            application.state = 'success'
            application.vm.state = 'deleted'
            application.vm.save()
            ports = json.loads(host.ports_info)
            nat_rules = json.loads(application.vm.nat_rules)
            for rule in nat_rules:
                ports["free"].append(rule["host_port"])
                ports["used"].remove(rule["host_port"])
            ports["free"].append(application.vm.info.ssh_port)
            ports["used"].remove(application.vm.info.ssh_port)
            host.ports_info = json.dumps(ports)
            host.save()
        elif response:
            application.state = response['request_result']
            application.error = response['error_information']
        application.save()
        return application
    except ObjectDoesNotExist:
        return None

