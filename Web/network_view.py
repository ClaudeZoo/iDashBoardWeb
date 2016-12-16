# coding: utf-8
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
    if operation_type == CREATE_INTNET:
        pass
    elif operation_type == DELETE_INTNET:
        pass
    else:
        pass


@login_required
def network_test(request):
    host = Host.objects.get(pk=1)
    # remove_vm_from_intnet(request.user, vm1, network1)
    return HttpResponse("Be happy")


def create_intnet(user, host, net_name, ip, netmask, lower_ip, upper_ip):
    data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                     operation_type=CREATE_INTNET, net_name=net_name,
                     ip=ip, netmask=netmask, lower_ip=lower_ip, upper_ip=upper_ip)

    communicate(data_dict, host.ip, host.vm_manager_port)
    network = Network(name=net_name, type=INTNET, host=host, ip=ip, netmask=netmask, lower_ip=lower_ip,
                      upper_ip=upper_ip, machines=json.dumps([]))
    network.save()


def delete_intnet(user, host, network):
    data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                     operation_type=DELETE_INTNET, net_name=network.name)
    communicate(data_dict, host.ip, host.vm_manager_port)
    network_to_delete = Network.objects.get(name=network.name)
    network_to_delete.delete()


def add_vm_to_intnet(user, network, vm):
    if_code, if_no, vm_interface = set_vm_network(vm, network)

    if if_no > 0:
        data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                         operation_type=ADD_VM_TO_INTNET, net_name=network.name, vm_name=vm.name, if_code=if_code,
                         if_no=if_no)
        communicate(data_dict, vm.host.ip, vm.host.vm_manager_port)
        vm_interface.save()
        machines = json.loads(network.machines)
        machines.append(vm.info_id)
        network.machines = json.dumps(machines)
        network.save()


def remove_vm_from_network(user, vm, network, operation_type):
    # 虚拟机必须是开机状态
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
    machines.remove(vm.info_id)
    network.machines = json.dumps(machines)
    network.save()
    data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                     operation_type=operation_type, net_name=network.name, vm_name=vm.name, if_no=if_no,
                     if_code=if_code)
    communicate(data_dict, vm.host.ip, vm.host.vm_manager_port)


def create_hostonly(user, host, ip, netmask, lower_ip, upper_ip):
    data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                     operation_type=CREATE_HOSTONLY, ip=ip, netmask=netmask, lower_ip=lower_ip, upper_ip=upper_ip)

    response_dict = communicate(data_dict, host.ip, host.vm_manager_port)
    net_name = response_dict["net_name"]
    network = Network(name=net_name, type=INTNET, host=host, ip=ip, netmask=netmask, lower_ip=lower_ip,
                      upper_ip=upper_ip, machines=json.dumps([]))
    network.save()


def delete_hostonly(user, host, network):
    data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                     operation_type=DELETE_HOSTONLY, net_name=network.name)
    communicate(data_dict, host.ip, host.vm_manager_port)
    network.delete()


def add_vm_to_hostonly(user, network, vm):
    if_code, if_no, vm_interface = set_vm_network(vm, network)
    if if_no > 0:
        data_dict = dict(request_type="network", request_id=random_str(), request_userid=user.id,
                         operation_type=ADD_VM_TO_HOSTONLY, net_name=network.name, vm_name=vm.name, if_code=if_code,
                         if_no=if_no)
        communicate(data_dict, vm.host.ip, vm.host.vm_manager_port)
        vm_interface.save()
        machines = json.loads(network.machines)
        machines.append(vm.info_id)
        network.machines = json.dumps(machines)
        network.save()


def create_intnet_with_vms():
    pass


def create_hostonly_with_vms():
    pass