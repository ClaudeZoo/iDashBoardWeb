__author__ = 'Claude'
import json
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from Web.models import Host
from Web.models import CreateApplication
from Web.communication import communicate
from Web.views import is_admin


@login_required
def apply_new_vm(request):
    if request.POST.get('vm_type', '') and request.POST.get('os', '') and request.POST.get('memory', ''):
        os = request.POST.get('os', '')
        memory = int(request.POST.get('memory', ''))
        vm_type = request.POST.get('vm_type', '')
        reason = request.POST.get('reason', '')
        application = CreateApplication(applicant=request.user, vm_type=vm_type, os=os, memory=memory, reason=reason,
                                        state='pending')
        is_administer = is_admin(request.user)
        has_applied = 1
        application.save()
        return render_to_response('apply.html', locals())
    else:
        return HttpResponseRedirect('/apply/')


def create_vm(application_id):
    host_list = Host.objects.filter(state='Online')
    try:
        application = CreateApplication.objects.get(id=application_id)
        if host_list.count() > 0:
            i, max_length, max_index = 0, 0, 0
            while i < host_list.count():
                ports = json.loads(host_list[i].ports_info)
                if len(ports["free"]) > max_length:
                    max_index = i
                    max_length = len(ports["free"])
                i += 1
            if max_length > 0:
                host = host_list[max_index]
                ports = json.loads(host.ports_info)
                port = ports["free"][0]
                ports["free"].remove(port)
                ports["used"].append(port)
                request_dict = dict(request_id=application_id, request_type='new', port=port,
                                    request_userid=application.applicant.id, request_memory=application.memory)
                response = communicate(request_dict, host.ip, host.vm_manager_port)
                if response and response['request_response'] == 'received':
                    application.state = 'In line'
                    application.host = host
                elif not response:
                    ports["free"].append(port)
                    ports["used"].remove(port)
                    application.state = response['request_response']
                host.ports_info = json.dumps(ports)
                host.save()
            else:
                application.state = 'error'
                application.error = 'Run of out port'
        else:
            application.state = 'error'
            application.error = 'No host'
        application.save()
        return application
    except ObjectDoesNotExist:
        return None

