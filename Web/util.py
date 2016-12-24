# coding:utf-8
import random
import string
from django.db.models import ObjectDoesNotExist
from vp_interface import *
from models import NetInterface
from network_view import remove_vm_from_network


def random_str(random_length=8):  # 获取8位随机虚拟机名字
    return ''.join(random.sample(string.ascii_letters + string.digits, random_length))


def calculate_if_code(vm_net_if):
    if_code = 0
    if vm_net_if.eth1_type != NULL:
        if_code += 4
    if vm_net_if.eth2_type != NULL:
        if_code += 2
    if vm_net_if.eth3_type != NULL:
        if_code += 1
    return if_code


def set_vm_network(vm, network):
    try:
        vm_interface = NetInterface.objects.get(vm=vm)
    except ObjectDoesNotExist:  # 如果该 VM 还没有网卡的记录条目，就创建一个
        vm_interface = NetInterface(vm=vm, eth0_type=NULL, eth1_type=NULL, eth2_type=NULL, eth3_type=NULL)
        vm_interface.eth1_type = network.type
        vm_interface.eth1_network = network
        vm_interface.save()
        if_code = 4  # 因为此前没有使用 eth1 - eth3 号网卡，所以 eth1 可用，code 值为 4，no 值为 1
        if_no = 1

    else:
        if_code = calculate_if_code(vm_interface)

        free_ifs = if_code ^ 7  # 异或操作，值为 1 的位即是可用的
        if free_ifs >= 4:  # 如果eth1 可用，优先使用eth1
            if_no = 1
            if_code += 4
            vm_interface.eth1_type = network.type
            vm_interface.eth1_network = network
        elif free_ifs >= 2:  # eth2 可用
            if_no = 2
            if_code += 2
            vm_interface.eth2_type = network.type
            vm_interface.eth2_network = network
        elif free_ifs >= 1:  # eth3 可用
            if_no = 3
            if_code += 1
            vm_interface.eth3_type = network.type
            vm_interface.eth3_network = network
        else:
            if_no = 0
    return if_code, if_no, vm_interface


def cascaded_delete_interface(network):
    for vm in network.eth1_vms.all():
        remove_vm_from_network(vm.user, vm, vm.eth1_network)
        vm.eth1_network = None
        vm.eth1_type = NULL
        vm.save()
    for vm in network.eth2_vms.all():
        remove_vm_from_network(vm.user, vm, vm.eth2_network)
        vm.eth2_network = None
        vm.eth2_type = NULL
        vm.save()
    for vm in network.eth3_vms.all():
        remove_vm_from_network(vm.user, vm, vm.eth3_network)
        vm.eth3_network = None
        vm.eth3_type = NULL
        vm.save()
