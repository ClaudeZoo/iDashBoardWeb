__author__ = 'Claude'
import json
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from Web.models import VM
from Web.models import OperationRecord
from Web.communication import communicate


@login_required
def control_vm(request):
    request_type = request.POST['request_type']
    vm = VM.objects.get(uuid=request.POST['uuid'])
    operation = OperationRecord(vm=vm, user=request.user, type=request_type)
    operation.save()
    host = vm.host
    request_dict = dict(request_id=operation.id, request_type=request_type, request_userid=request.user.id,
                        vm_name=vm.name, vm_uuid=vm.uuid)
    response = communicate(request_dict, host.ip, host.vm_manager_port)
    if response and response['request_result'] == 'success':
        operation.result = 'success'
        if request_type == 'start':
            vm.state = 'Online'
        elif request_type == 'shutdown':
            vm.state = 'Offline'
        else:
            vm.state = 'Hibernating'
        vm.save()
    elif response:
        operation.result = response['request_result']
        operation.information = response['error_information']
    else:
        operation.result = response['network_error']
    operation.save()
    return HttpResponse(json.dumps(dict(request_result=operation.result, error_information=operation.information)))