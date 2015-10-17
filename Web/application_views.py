__author__ = 'Claude'
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from Web.views import is_admin
from Web.models import CreateApplication
from Web.models import DeleteApplication
from Web.models import PortApplication
from Web.models import OperationRecord


@login_required
def applications_view(request):
    is_administer = is_admin(request.user)
    create_application_list = CreateApplication.objects.filter(applicant=request.user)
    create_applications = list()
    for create_application in create_application_list:
        create_applications.append(create_application.application_info())

    delete_application_list = DeleteApplication.objects.filter(applicant=request.user)
    delete_applications = list()
    for delete_application in delete_application_list:
        delete_applications.append(delete_application.application_info())

    port_application_list = PortApplication.objects.filter(applicant=request.user)
    port_applications = list()
    for port_application in port_application_list:
        port_applications.append(port_application.application_info())

    operation_list = OperationRecord.objects.filter(user=request.user)
    operations = list()
    for operation in operation_list:
        operations.append(operation.get_info())
    return render_to_response('applications.html', locals())
