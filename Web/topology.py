import json
from django.shortcuts import render_to_response, HttpResponse
from django.contrib.auth.decorators import login_required
from Web.views import is_admin
from Web.models import Host, VM, MachineInfo, NetInterface, Network
from Web.vp_interface import *
from Web.views import is_admin


# @login_required
def topology_view(request):
    is_administer = is_admin(request.user)
    return render_to_response('topology.html', locals())


# @login_required
def topology_data(request):
    nodes = list()
    links = list()
    node_subnets = dict()
    hosts = Host.objects.all()
    for host in hosts:
        nodes.append(dict(id=host.info_id, group=host.info_id, size=70, name=host.info.hostname))
        for vm in host.vms.filter(state="Online"): # all().exclude(state="deleted"):
            nodes.append(
                dict(id=vm.info_id, group=host.info_id, size=35 + vm.memory / 512 * 5, name=vm.name, uuid=vm.uuid,
                     memory=vm.memory))
            links.append(dict(source=host.info_id, target=vm.info_id, group=0, value=2))
    for network in Network.objects.all():
        all_machines = json.loads(network.machines)
        machines = []
        if network.type != BRIDGE:
            for machine in all_machines:
                if VM.objects.get(info_id=machine).state == "Online":
                    machines.append(machine)
        if network.type == INTNET:
            if len(machines) > 1:
                for i in range(len(machines) - 1):
                    links.append(dict(source=machines[i], target=machines[i + 1], group=network.id, value=5))
            if len(machines) > 2:
                links.append(dict(source=machines[-1], target=machines[0], group=network.id, value=5))
        if network.type == HOSTONLY:
            if len(machines) >= 1:
                links.append((dict(source=network.host.info_id, target=machines[0], group=network.id, value=5)))
                for i in range(len(machines) - 1):
                    links.append(dict(source=machines[i], target=machines[i + 1], group=network.id, value=5))
            if len(machines) >= 2:
                links.append(dict(source=machines[-1], target=network.host.info_id, group=network.id, value=5))
        if network.type == BRIDGE:
            machines = all_machines
            if len(machines) > 1:
                for i in range(len(machines) - 1):
                    links.append(dict(source=machines[i], target=machines[i + 1], group=network.id, value=10))
            if len(machines) > 2:
                links.append(dict(source=machines[-1], target=machines[0], group=network.id, value=10))

    # node_subnets
    for interface in NetInterface.objects.all():
        vm_info_id = (VM.objects.get(id=interface.vm_id)).info_id
        network1_dict, network2_dict, network3_dict = "", "", ""
        if interface.eth1_network_id:
            network1 = Network.objects.get(id=interface.eth1_network_id)
            network1_dict = {'name': network1.name, 'id': network1.id}
        if interface.eth2_network_id:
            network2 = Network.objects.get(id=interface.eth2_network_id)
            network2_dict = {'name': network2.name, 'id': network2.id}
        if interface.eth3_network_id:
            network3 = Network.objects.get(id=interface.eth3_network_id)
            network3_dict = {'name': network3.name, 'id': network3.id}
        node_subnets[vm_info_id] = [network1_dict, network2_dict, network3_dict]
    ret = dict(nodes=nodes, links=links, node_subnets=node_subnets)
    return HttpResponse(json.dumps(ret))
