import json
from django.shortcuts import render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from Web.views import is_admin
from Web.models import Host, VM, MachineInfo, NetInterface, Network


@login_required
def topology_view(request):
    return render_to_response('topology.html', locals())


@login_required
def topology_data(request):
    nodes = list()
    links = list()
    hosts = Host.objects.all()
    for host in hosts:
        nodes.append(dict(id=host.info_id, group=host.info_id, size=40, name=host.ip))
        for vm in host.vms.all().exclude(state="deleted"):
            nodes.append(dict(id=vm.info_id, group=host.info_id, size=10+vm.memory/512 * 5, name=vm.name, uuid=vm.uuid,
                              memory=vm.memory))
            links.append(dict(source=host.info_id, target=vm.info_id, group=0, value=2))
    for network in Network.objects.all():
        machines = json.loads(network.machines)
        if len(machines) > 1:
            for i in range(len(machines) - 1):
                links.append(dict(source=machines[i], target=machines[i+1], group=network.id, value=5))
            links.append(dict(source=machines[-1], target=machines[0], group=network.id, value=5))
    ret = dict(nodes=nodes, links=links)
    return HttpResponse(json.dumps(ret))

