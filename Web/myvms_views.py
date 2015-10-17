__author__ = 'Claude'
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from Web.models import VM
from Web.views import is_admin


@login_required
def my_vms_view(request):
    is_administer = is_admin(request.user)
    vm_list = VM.objects.filter(user=request.user).exclude(state='deleted')
    vms = list()
    for vm in vm_list:
        vms.append(vm.vm_info())
    return render_to_response('myVMs.html', locals())