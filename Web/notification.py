__author__ = 'Claude'
from django.utils import timezone
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from Web.models import VM
from Web.models import MachineInfo
from Web.models import CreateApplication
from Web.models import DeleteApplication


def handle_notification(request):
    print(request.body)
    request_id = request.POST.get('request_id', '')
    request_type = request.POST.get('request_type', '')
    request_result = request.POST.get('request_result', '')
    port = request.POST.get('port', '')
    print("%s %s %s" % (request_id, request_type, request_result))
    if request_type == 'new':
        try:
            create_application = CreateApplication.objects.get(id=request_id)
            create_application.state = request_result
            if request_result == 'success':
                info = MachineInfo(last_connect_time=timezone.now(), wan_ip=create_application.host.ip,
                                   ssh_port=port, os_info=create_application.os)
                info.save()
                vm = VM(info=info, state='Offline', user=create_application.applicant, host=create_application.host,
                        uuid=request.POST.get('vm_uuid', ''), name=request.POST.get('vm_name', ''), os=create_application.os,
                        memory=create_application.memory, vm_type=create_application.vm_type)
                vm.save()
            else:
                create_application.error = request.POST.get('error_information', '')
            create_application.save()
            return HttpResponse('hehe')
        except ObjectDoesNotExist:
            return HttpResponse('')