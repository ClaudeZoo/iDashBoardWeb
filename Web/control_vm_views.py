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
        print request_type
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


def start_vm(request):
    if int(request.POST['current_process']) == 0:
        request_type = request.POST['request_type']
        vm = VM.objects.get(uuid=request.POST['uuid'])
        operation = OperationRecord(vm=vm, user=request.user, type=request_type)
        operation.save()
        host = vm.host
        request_dict = dict(request_id=operation.id, request_type=request_type, request_userid=request.user.id,
                            vm_name=vm.name, vm_uuid=vm.uuid)
        response = communicate(request_dict, host.ip, host.vm_manager_port)
        monitor_req_dict = dict(vm_uuid=vm.uuid, type='start')
        communicate(monitor_req_dict, host.ip, 8777)
        if response and response['request_result'] == 'success':
            return HttpResponse(json.dumps(dict(request_result='success')))
        elif response:
            operation.result = response['request_result']
            operation.information = response['error_information']
        else:
            operation.result = response['network_error']
        operation.save()
        return HttpResponse(json.dumps(dict(request_result=operation.result, error_information=operation.information)))
    else:
        return powering_process_vm(request)


def powering_process_vm(request):
    current_process = float(request.POST['process'])
    #if current_process <= 90:
    #   return HttpResponse(json.dumps(dict(request_result='success', request_process=current_process+10, next_state=0)))
    #else:
    #    return HttpResponse(json.dumps(dict(request_result='success', request_process=100, next_state=5)))
    vm = VM.objects.get(uuid=request.POST['uuid'])
    if not OperationRecord.objects.filter(vm=vm).exists():
        return HttpResponse(json.dumps(dict(request_result='error', error_information='The VM hasn\'t start')))
    host = vm.host
    monitor_req_dict = dict(vm_uuid=vm.uuid, type='query')
    response = communicate(monitor_req_dict, host.ip, 8777)
    if response and response['result'] == 'success':
        result_process = float(response['process'])
        print result_process
        next_state = 0
        if result_process >= 100 or current_process >= 100 or vm.state == 'Online':
            vm.state = 'Online'
            vm.save()
            result_process = 100
            next_state = 5
        elif int(current_process) > result_process or result_process <= 0:
            result_process = int(current_process)
        return HttpResponse(json.dumps(dict(request_result='success', request_process=result_process, next_state=next_state)))
    elif response:
        result = response['result']
    else:
        result = 'Abortion connection'
    return HttpResponse(json.dumps(dict(request_result=result)))

