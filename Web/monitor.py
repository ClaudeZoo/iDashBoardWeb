from django.shortcuts import HttpResponse
from Web.models import VM
from Web.communication import communicate


def online(request):
    if 'uuid' in request.POST and request.POST['uuid']:
        uuid = request.POST['uuid'].strip('\n')
        vm = VM.objects.get(uuid=uuid)
        vm.state = 'Online'
        vm.save()
        request_dict = dict(request_id=0, vm_uuid=uuid, type='end')
        communicate(request_dict, vm.host.ip, vm.host.vm_manager_port)
    return HttpResponse("Ok")
