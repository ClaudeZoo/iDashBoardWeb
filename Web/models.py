import json
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DUser(models.Model):
    user = models.OneToOneField(User)
    department = models.CharField(max_length=100, null=True)
    phone = models.PositiveIntegerField(null=True)


class Host(models.Model):
    info = models.OneToOneField('MachineInfo')
    state = models.CharField(max_length=15, null=True)
    ip = models.CharField(max_length=20, null=True)
    vm_manager_port = models.IntegerField(null=True)
    ports_info = models.TextField(null=True)


class VM(models.Model):
    info = models.OneToOneField('MachineInfo')
    state = models.CharField(max_length=15)
    user = models.ForeignKey(User, related_name='my_vms', null=True)
    host = models.ForeignKey('Host', related_name='vms', null=True)
    uuid = models.TextField(null=True)
    name = models.TextField(null=True)
    os = models.CharField(max_length=20, null=True)
    memory = models.IntegerField(null=True)
    vm_type = models.CharField(max_length=10, null=True)
    nat_rules = models.TextField(null=True)

    def vm_info(self):
        info_dict = dict(id=self.id, uuid=self.uuid, name=self.name, ip=self.info.wan_ip, ssh_port=self.info.ssh_port, 
                         state=self.state, last_connect_time=self.info.last_connect_time, os=self.os,
                         memory=self.memory, vm_type=self.vm_type, host=self.host.id)
        return info_dict


class CreateApplication(models.Model):
    applicant = models.ForeignKey(User, null=False, related_name='my_create_applications')
    reviewer = models.ForeignKey(User, null=True, related_name='create_applications')
    submission_time = models.DateTimeField(auto_now_add=True)
    review_time = models.DateTimeField(null=True, auto_now=True)
    vm_type = models.CharField(max_length=10, null=True)
    os = models.CharField(max_length=30, null=True)
    host_name = models.CharField(max_length=20, null=True)
    user_name = models.TextField(max_length=30, null=True)
    password = models.TextField(null=True)
    memory = models.IntegerField(null=True)
    state = models.CharField(max_length=10)
    error = models.TextField(null=True)
    vm = models.ForeignKey(VM, null=True)
    host = models.ForeignKey('Host', null=True)

    class Meta:
        ordering = ['-submission_time']

    def audit_info(self):
        info_dict = dict(id=self.id, applicant=self.applicant.username, submission_time=self.submission_time,
                         vm_type=self.vm_type, os=self.os, memory=self.memory)
        return info_dict

    def application_info(self):
        if self.vm:
            vm_name = self.vm.name
        else:
            vm_name = "None"
        info_dict = dict(id=self.id, submission_time=self.submission_time, review_time=self.review_time,
                         vm_type=self.vm_type, os=self.os, memory=self.memory, state=self.state, error=self.error,
                         vm_name=vm_name, reviewer=self.reviewer.username)
        return info_dict


class DeleteApplication(models.Model):
    applicant = models.ForeignKey(User, null=False, related_name='my_delete_applications')
    reviewer = models.ForeignKey(User, null=True, related_name='delete_applications')
    vm = models.ForeignKey('VM')
    host = models.ForeignKey('Host')
    submission_time = models.DateTimeField(auto_now_add=True)
    review_time = models.DateTimeField(null=True, auto_now=True)
    state = models.CharField(max_length=10)
    error = models.TextField(null=True)

    class Meta:
        ordering = ['-submission_time']

    def audit_info(self):
        info_dict = dict(id=self.id, applicant=self.applicant.username, submission_time=self.submission_time,
                         host_ip=self.host.info.wan_ip, vm_name=self.vm.name, vm_uuid=self.vm.uuid)
        return info_dict

    def application_info(self):
        info_dict = dict(id=self.id, submission_time=self.submission_time, review_time=self.review_time,
                         state=self.state, error=self.error, vm_name=self.vm.name, reviewer=self.reviewer.username,
                         host_ip=self.host.info.wan_ip)
        return info_dict


class PortApplication(models.Model):
    applicant = models.ForeignKey(User, null=False, related_name='my_port_applications')
    reviewer = models.ForeignKey(User, null=True, related_name='port_applications')
    vm = models.ForeignKey('VM')
    host = models.ForeignKey('Host')
    protocol = models.TextField(max_length=5, null=True)
    vm_port = models.IntegerField()
    host_port = models.IntegerField()
    submission_time = models.DateTimeField(auto_now_add=True)
    review_time = models.DateTimeField(null=True, auto_now=True)
    state = models.CharField(max_length=10)
    error = models.TextField(null=True)

    class Meta:
        ordering = ['-submission_time']

    def audit_info(self):
        info_dict = dict(id=self.id, applicant=self.applicant.username, submission_time=self.submission_time,
                         protocol=self.protocol, host_ip=self.host.info.wan_ip, host_port=self.host_port,
                         vm_port=self.vm_port, vm_name=self.vm.name, vm_uuid=self.vm.uuid)
        return info_dict

    def application_info(self):
        info_dict = dict(id=self.id, submission_time=self.submission_time, review_time=self.review_time,
                         protocol=self.protocol, vm_port=self.vm_port, host_port=self.host_port,
                         host_ip=self.host.info.wan_ip, state=self.state, error=self.error, vm_name=self.vm.name,
                         reviewer=self.reviewer.username)
        return info_dict


class OperationRecord(models.Model):
    vm = models.ForeignKey('VM', related_name='vm_record')
    user = models.ForeignKey(User, related_name='my_operations')
    type = models.CharField(max_length=10)
    execute_time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=10, null=True)
    information = models.TextField(null=True)

    def get_info(self):
        info_dict = dict(execute_time=self.execute_time, vm_name=self.vm.name, type=self.type, result=self.result,
                         information=self.information)
        return info_dict


class MachineInfo(models.Model):
    wan_ip = models.TextField(null=True)
    lan_ip = models.TextField(null=True)
    ssh_port = models.PositiveIntegerField(null=True)
    last_connect_time = models.DateTimeField(null=True, auto_now=True)
    # when the client connect the server for the last time
    state_info = models.TextField(null=True)

    #from ifconfig command
    inet4 = models.TextField(null=True)
    broadcast = models.TextField(null=True)
    inet6 = models.TextField(null=True)
    mask = models.TextField(null=True)
    dns = models.TextField(null=True)

    #from top command
    users = models.TextField(null=True)
    load_average = models.TextField(null=True)
    tasks = models.TextField(null=True)
    percent_cpu = models.TextField(null=True)
    memory = models.TextField(null=True)
    swap = models.TextField(null=True)
    process = models.TextField(null=True)
    #others
    hostname = models.TextField(null=True)
    username = models.TextField(null=True)
    cpu_info = models.TextField(null=True)
    os_info = models.TextField(null=True)
    disk = models.TextField(null=True)

    def update_info(self, info):
        if "HostName" in info:
            self.hostname = info["HostName"]
        if "UserName" in info:
            self.username = info["UserName"]
        if "CPUInfo" in info:
            self.cpu_info = info["CPUInfo"]
        if "Tasks" in info:
            self.tasks = info["Tasks"]
        if "Memory" in info:
            self.memory = info["Memory"]
        if "percentCPU" in info:
            self.percent_cpu = info["percentCPU"]
        if "Swap" in info:
            self.swap = info["Swap"]
        if "inet4" in info:
            self.inet4 = info["inet4"]
            self.lan_ip = info["inet4"]
        if "bcast" in info:
            self.broadcast = info["bcast"]
        if "mask" in info:
            self.mask = info["mask"]
        if "DNS" in info:
            self.dns = info["DNS"]
        if "inet6" in info:
            self.inet6 = info["inet6"]
        if "os" in info:
            self.os_info = info["os"]
        if "process" in info:
            self.process = info["process"]
        if "Disk" in info:
            self.disk = info["Disk"]
