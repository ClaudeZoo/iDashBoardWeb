__author__ = 'Claude'
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from Web.views import is_admin


@login_required
def apply_view(request):
    is_administer = is_admin(request.user)
    return render_to_response('apply.html', locals())
