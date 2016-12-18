import json
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from models import Network, NetInterface, Host, VM, MachineInfo
from communication import communicate
from vp_interface import *
from util import *


@login_required
def network_view(request):
    operation_type = request.POST['operation_type']


@login_required
def network_test(request):
    host = Host.objects.get(pk=1)
    create_intnet(request.user, host, "intnet2", "192.168.24.0", "255.255.255.0", "192.168.24.2", "192.168.24.99")
    network1 = Network.objects.get(name="intnet1")
    network2 = Network.objects.get(name="intnet2")
    vm1 = VM.objects.get(name="80qRxKDk")
    vm2 = VM.objects.get(name="w4vH3Sq0")
    vm3 = VM.objects.get(name="AOKGFHDp")
    vm4 = VM.objects.get(name="YH4mguSn")
    add_vm_to_intnet(request.user, network2, vm1)
    add_vm_to_intnet(request.user, network1, vm2)
    add_vm_to_intnet(request.user, network1, vm3)
    add_vm_to_intnet(request.user, network2, vm4)

    # remove_vm_from_intnet(request.user, vm1, network1)
    return HttpResponse("Be happy")


def create_intnet(user, host, net_name, ip, netmask, lower_ip, upper_ip):
    data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                     operation_type=CREATE_INTNET, net_name=net_name,
                     ip=ip, netmask=netmask, lower_ip=lower_ip, upper_ip=upper_ip)

    communicate(data_dict, host.ip, host.vm_manager_port)
    network = Network(name=net_name, type="intnet", host=host, ip=ip, netmask=netmask, lower_ip=lower_ip,
                      upper_ip=upper_ip, machines=json.dumps([]))
    network.save()
    pass


def delete_intnet(user, host, net_name):
    data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                     operation_type=DELETE_INTNET, net_name=net_name)
    communicate(data_dict, host.ip, host.vm_manager_port)
    network_to_delete = Network.objects.get(name=net_name)
    network_to_delete.delete()
    pass


def add_vm_to_intnet(user, network, vm):
    try:
        vm_interface = NetInterface.objects.get(vm=vm)
    except ObjectDoesNotExist:
        vm_interface = NetInterface(vm=vm, eth0_type=NULL, eth1_type=NULL, eth2_type=NULL, eth3_type=NULL)
        vm_interface.save()
        if_code = 4
        if_no = 1
    else:
        if_code = calculate_if_code(vm_interface)

        free_ifs = if_code ^ 7
        if free_ifs >= 4:
            if_no = 1
            if_code += 4
            vm_interface.eth1_type = INTNET
            vm_interface.eth1_network = network
        elif free_ifs >= 2:
            if_no = 2
            if_code += 2
            vm_interface.eth2_type = INTNET
            vm_interface.eth2_network = network
        elif free_ifs >= 1:
            if_no = 3
            if_code += 1
            vm_interface.eth3_type = INTNET
            vm_interface.eth3_network = network
        else:
            if_no = 0

    if if_no > 0:
        print(vm.name)
        data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                         operation_type=ADD_VM_TO_INTNET, net_name=network.name, vm_name=vm.name, if_code=if_code,
                         if_no=if_no)
        communicate(data_dict, vm.host.ip, vm.host.vm_manager_port)
        vm_interface.save()
        machines = json.loads(network.machines)
        machines.append(vm.info_id)
        network.machines = json.dumps(machines)
        network.save()


def remove_vm_from_intnet(user, vm, network):
    vm_if = NetInterface.objects.get(vm=vm)

    if_no = 0
    if vm_if.eth1_network == network:
        vm_if.eth1_type = NULL
        vm_if.eth1_network = None
        if_no = 1
    elif vm_if.eth2_network == network:
        vm_if.eth2_type = NULL
        vm_if.eth2_network = None
        if_no = 2
    elif vm_if.eth3_network == network:
        vm_if.eth3_type = NULL
        vm_if.eth3_network = None
        if_no = 3
    else:
        pass

    if_code = calculate_if_code(vm_if)

    machines = json.loads(network.machines)
    print(machines)
    print(vm.info_id)
    machines.remove(vm.info_id)
    network.machines = json.dumps(machines)
    network.save()
    data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                     operation_type=REMOVE_VM_FROM_NETWORK, net_name=network.name, vm_name=vm.name, if_no=if_no,
                     if_code=if_code)
    communicate(data_dict, vm.host.ip, vm.host.vm_manager_port)
    print(vm.name)


def create_hostonly():
    pass


def delete_hostonly():
    pass


def add_vm_to_hostonly():
    pass


def remove_vm_from_hostonly():
    pass


def create_intnet_with_vms(request):
    try:
        vms = (request.POST.get('vms', '')).split(',')
        host_id = request.POST.get('host', '')
        host = Host.objects.get(pk=host_id)
        net_name = request.POST.get('net_name', '')
        net_ip = request.POST.get('net_ip', '')
        net_mask = request.POST.get('net_mask', '')
        lower_ip = request.POST.get('lower_ip', '')
        upper_ip = request.POST.get('upper_ip', '')
        create_intnet(request.user, host, net_name, net_ip, net_mask, lower_ip, upper_ip)
        for vm_name in vms:
            vm = VM.objects.get(name=vm_name)
            network = Network.objects.get(name=net_name)
            add_vm_to_intnet(request.user, network, vm)
        return HttpResponse('Succeed')
    except:
        return HttpResponse('Failed')


def create_hostonly_with_vms():
    pass
