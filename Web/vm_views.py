__author__ = 'Claude'
import datetime
import json
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from Web.models import VM
from Web.models import Host


@login_required
def refresh_homepage(request):
    pass


@login_required
def refresh_vms(request):
    vm_info_list = get_vm_info_list()
    response = dict(data=vm_info_list)
    response['Access-Control-Allow-Origin'] = '*'
    return HttpResponse(json.dumps(response))


@login_required
def refresh_hosts(request):
    host_info_list = get_host_info_list()
    response = dict(data=host_info_list)
    response['Access-Control-Allow-Origin'] = '*'
    return HttpResponse(json.dumps(response))


def get_vm_info_list():
    t = datetime.datetime.now()
    t -= datetime.timedelta(seconds=60)
    vms = VM.objects.exclude(state='deleted')
    vm_info_list = []
    for vm in vms:
        info = vm.info
        try:
            disk_used = get_disk_used(info.disk)
            memory = str(int(float(info.memory.split()[1].rstrip('k')) /
                             float(info.memory.split()[0].rstrip('k')) * 100 + 0.5)) + '%'
            cpu = str(int(100 - float(info.percent_cpu.split()[3].split('%')[0]) + 0.5)) + '%'
        except Exception, e:
            disk_used = '0%'
            memory = '0%'
            cpu = '0%'
        finally:
            if info.last_connect_time < t:
                state = "offline"
            else:
                state = 'online'
            info_dict = dict(state=state, ip=info.lan_ip, wan_ip=info.wan_ip, port=info.ssh_port,
                             os=info.os_info[0:-8], vm_name=vm.name, Disk=disk_used,
                             Memory=memory, CPU=cpu, id=vm.id)
            vm_info_list.append(info_dict)
    return vm_info_list


def get_disk_used(disk_info):
    disk_list = disk_info.split()
    used = 0
    size = 0
    if (len(disk_list) - 7) % 6 == 0:
        disk_number = (len(disk_list) - 7) / 6
        for index in range(1, disk_number):
            size_info = disk_list[index*6 + 2]
            size = calculate_size(size_info, size)
            used_info = disk_list[index*6 + 3]
            used = calculate_size(used_info, used)
    return str(int(100 * used / size + 0.5)) + '%'


def get_host_info_list():
    t = datetime.datetime.now()
    t -= datetime.timedelta(seconds=60)
    hosts = Host.objects.filter(state="Online")
    host_info_list = []
    for host in hosts:
        info = host.info
        try:
            if host.lan_ip == '10.0.0.121':
                disk_used = get_host2_disk_used(info.disk)
            else:
                disk_used = get_host1_disk_used(info.disk)
            memory = str(int(float(info.memory.split()[1].rstrip('k'))
                         / float(info.memory.split()[0].rstrip('k')) * 100 + 0.5)) + '%'
            cpu = str(int(100 - float(info.percent_cpu.split()[3].split('%')[0]) + 0.5)) + '%'
        except Exception:
            disk_used = '0%'
            memory = '0%'
            cpu = '0%'
        finally:
            if info.last_connect_time < t:
                state = "Offline"
            else:
                state = 'Online'
            info_dict = dict(state=state, ip=info.lan_ip, wan_ip=info.wan_ip, os=info.os_info[0:-8],
                             Disk=disk_used, Memory=memory, CPU=cpu, id=host.id)
            host_info_list.append(info_dict)
    return host_info_list


def get_host1_disk_used(disk_info):
    disk_list = disk_info.split()
    used = 0
    size = 0
    if (len(disk_list) - 6) % 6 == 0:
        disk_number = (len(disk_list) - 6) / 6
        for index in range(1, disk_number+1):
            size_info = disk_list[index*6 + 4]
            size = calculate_size(size_info, size)
            print(size)
            used_info = disk_list[index*6 + 5]
            used = calculate_size(used_info, used)
    return str(int(100 * used / size + 0.5)) + '%'


def get_host2_disk_used(disk_info):
    disk_list = disk_info.split()
    used = 0
    size = 0
    if (len(disk_list) - 7) % 6 == 0:
        disk_number = (len(disk_list) - 7) / 6
        for index in range(1, disk_number+1):
            size_info = disk_list[index*6 + 2]
            size = calculate_size(size_info, size)
            used_info = disk_list[index*6 + 3]
            used = calculate_size(used_info, used)
    return str(int(100 * used / size + 0.5)) + '%'


def calculate_size(info, size):
    if info[-1] == 'K':
        size += float(info[:-1])
    elif info[-1] == 'M':
        size += float(info[:-1]) * 1024
    elif info[-1] == 'G':
        size += float(info[:-1]) * 1024 * 1024
    else:
        size += 0
    return size