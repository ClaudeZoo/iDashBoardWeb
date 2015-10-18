__author__ = 'Claude'
import json
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from Web.views import is_admin
from Web.models import MachineInfo


@login_required
def detail_view(request):
    is_administer = is_admin(request.user)
    return render_to_response('detail.html', locals())


@login_required
def get_detail(request, vm_id):
    if request.user.is_authenticated():
        vmDetail = {}
        try:
            vm = MachineInfo.objects.filter(id=vm_id)
            if len(vm) != 0:
                vmDetail = {'data': vm_id, 'Access-Control-Allow-Origin': '*'}
                vmDetail['uName'] = vm[0].os_info[0:-8]
                vmDetail['cpuInfo'] = vm[0].cpu_info
                vmDetail['memory'] = vm[0].memory
                vmDetail['memory_swap'] = vm[0].swap
                vmDetail['cpuLoad'] = vm[0].percent_cpu
                vmDetail['tasks'] = vm[0].tasks
                vmDetail['userName'] = vm[0].username
                vmDetail['ipv4'] = vm[0].inet4
                vmDetail['ipv6'] = vm[0].inet6
                vmDetail['broadcast'] = vm[0].broadcast
                vmDetail['mask'] = vm[0].mask
                vmDetail['dns'] = vm[0].dns
                vmDetail['process'] = []
                if len(vm[0].process) != 0:
                    process = vm[0].process.split("\n")
                    pinfodic = {}
                    for p in process:
                        pinfo = p.split()
                        if len(pinfo) < 12:
                            break
                        pinfodic['PID'] = pinfo[0]
                        pinfodic['USER'] = pinfo[1]
                        pinfodic['cpu'] = pinfo[8]
                        pinfodic['mem'] = pinfo[9]
                        pinfodic['cmd'] = pinfo[11]
                        vmDetail['process'].append(pinfodic.copy())
            else:
                vmDetail = {'IPAddress': [], 'stateInfo': []}
        except Exception, e:
            print e
            return HttpResponse(e)
        return HttpResponse(json.dumps(vmDetail))
    return render_to_response('index.html', locals())
