__author__ = 'Claude'
import json
from django.utils import timezone
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from Web.models import Host
from Web.models import VM
from Web.models import PortApplication
from Web.communication import communicate


@login_required
def apply_nat(request):
    user = request.user
    print(request.body)
    vm_uuid = request.POST.get('uuid', '')
    protocol = request.POST.get('protocol', '')
    vm_port = int(request.POST.get('vm_port', ''))
    host_port = int(request.POST.get('host_port', ''))
    try:
        vm = VM.objects.get(uuid=vm_uuid)
        if vm.user == user:
            application = PortApplication(applicant=user, vm=vm, host=vm.host, protocol=protocol,
                                          vm_port=vm_port, host_port=host_port, state='pending')
            ports = json.loads(vm.host.ports_info)
            ports['free'].remove(host_port)
            ports['used'].append(host_port)
            vm.host.ports_info = json.dumps(ports)
            vm.host.save()
            application.save()
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    except ObjectDoesNotExist:
        return HttpResponse('0')


def execute_nat(application_id):
    try:
        application = PortApplication.objects.get(id=application_id)
        host = application.vm.host
        request_dict = dict(request_id=application_id, request_type='add_nat_rule',
                            request_userid=application.applicant.id, protocol=application.protocol,
                            host_port=application.host_port, guest_port=application.vm_port,
                            vm_name=application.vm.name, vm_uuid=application.vm.uuid)
        response = communicate(request_dict, host.ip, host.vm_manager_port)
        if response and response['request_result'] == 'success':
            application.state = 'success'
            nat_rules = json.loads(application.vm.nat_rules)
            rule = dict(host_port=application.host_port, guest_port=application.vm_port, protocol=application.protocol)
            nat_rules.append(json.dumps(rule))
            application.vm.nat_rules = json.dump(nat_rules)
            application.vm.save()
        elif not response:
            application.state = response['request_response']
            application.error = response['error_information']
        else:
            application.state = 'network_error'
        application.save()
        return application
    except ObjectDoesNotExist:
        return None


def get_free_ports(request):
    host = Host.objects.get(id=request.GET['host'])
    ports_dict = json.loads(host.ports_info)
    free_ports_list = ports_dict["free"]
    return HttpResponse(json.dumps(free_ports_list))
