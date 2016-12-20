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
    node_subnets = dict()
    hosts = Host.objects.all()
    for host in hosts:
        nodes.append(dict(id=host.info_id, group=host.info_id, size=40, name=host.ip))
        for vm in host.vms.all().exclude(state="deleted"):
            nodes.append(dict(id=vm.info_id, group=host.info_id, size=10+vm.memory/512 * 5, name=vm.name, uuid=vm.uuid,
                              memory=vm.memory))
            links.append(dict(source=host.info_id, target=vm.info_id, group=0, value=2))
    for i in range(len(hosts) - 1):
        links.append(dict(source=hosts[i].info_id, target=hosts[i+1].info_id, group=0, value=10))
    #links.append(dict(source=hosts[-1].info_id, target=hosts[0].info_id, group=0, value=10))
    for network in Network.objects.all():
        machines = json.loads(network.machines)
        if len(machines) > 1:
            for i in range(len(machines) - 1):
                links.append(dict(source=machines[i], target=machines[i+1], group=network.id, value=5))
            links.append(dict(source=machines[-1], target=machines[0], group=network.id, value=5))

    #node_subnets
    for interface in NetInterface.objects.all():
        vm_info_id = (VM.objects.get(id=interface.vm_id)).info_id
        network1_dict, network2_dict, network3_dict = "", "", ""
        if interface.eth1_network_id:
            network1 = Network.objects.get(id=interface.eth1_network_id)
            network1_dict = {'name':network1.name,'id':network1.id}
        if interface.eth2_network_id:
            network2 = Network.objects.get(id=interface.eth2_network_id)
            network2_dict = {'name':network2.name,'id':network2.id}
        if interface.eth3_network_id:
            network3 = Network.objects.get(id=interface.eth3_network_id)
            network3_dict = {'name':network3.name,'id':network3.id}
        node_subnets[vm_info_id] = [network1_dict, network2_dict, network3_dict]
    ret = dict(nodes=nodes, links=links, node_subnets=node_subnets)
    return HttpResponse(json.dumps(ret))

