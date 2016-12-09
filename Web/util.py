# coding:utf-8
import random
import string
from vp_interface import *


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
