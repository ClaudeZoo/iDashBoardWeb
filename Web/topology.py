from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from Web.views import is_admin


@login_required
def topology_view(request):
    return render_to_response('topology.html', locals())
