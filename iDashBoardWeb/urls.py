"""iDashBoardWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.contrib.auth import views as auth_views
from iDashBoardWeb.settings import CSS_DIR, JS_DIR, IMG_DIR, LIB_DIR
from Web import views, apply_views, audit_views, myvms_views, application_views
from Web import detail_views, vm_views, info_update, control_vm_views
from Web import create_vm_views, nat_views, delete_vm_views, notification
from Web import monitor, topology, network_view

urlpatterns = [
    url(r'^$', views.home),
    url(r'^home/$', views.home),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^css/(?P<path>.*)', serve, {'document_root': CSS_DIR}),
    url(r'^js/(?P<path>.*)', serve, {'document_root': JS_DIR}),
    url(r'^img/(?P<path>.*)', serve, {'document_root': IMG_DIR}),
    url(r'^lib/(?P<path>.*)', serve, {'document_root': LIB_DIR}),

    url(r'^topology/$', topology.topology_view),
    url(r'^apply/$', apply_views.apply_view),
    url(r'^audit/$', audit_views.audit_view),
    url(r'^myVMs', myvms_views.my_vms_view),
    url(r'^applications/$', application_views.applications_view),
    url(r'^detail/\d+/$', detail_views.detail_view),
    url(r'^get-detail/(?P<vm_id>\d+)/$', detail_views.get_detail),
    url(r'^login/$', views.user_login),
    url(r'^logout/$', views.user_logout),
    url(r'^signup/$', views.sign_up),
    url(r'^settings/$', views.settings),
    url(r'^saveUserInfo', views.save_user_info),
    url(r'^changePassword', views.change_password),
    url(r'^validateUserName', views.validate_username),
    url(r'^refreshHomePage/$', vm_views.refresh_homepage),
    url(r'^refreshSimplePage/$', vm_views.refresh_vms),
    url(r'^refreshSimplePageHost/$', vm_views.refresh_hosts),
    url(r'^get-detail/(?P<vm_id>\d+)/$', detail_views.get_detail),
    url(r'^helloServer/$', info_update.hello_server),
    url(r'^saveVMState/$', info_update.update_info),

    url(r'^start_vm/$', control_vm_views.start_vm),
    url(r'^start_monitor/$', control_vm_views.start_monitor),
    url(r'^control_vm/$', control_vm_views.control_vm),
    url(r'^apply_new_vm/$', create_vm_views.apply_new_vm),
    url(r'^apply_nat/$', nat_views.apply_nat),
    url(r'^delete_apply/$', delete_vm_views.apply_delete_vm),
    url(r'^reply_vmHost/$', notification.handle_notification),
    url(r'^apply_subnet/$', network_view.create_intnet_with_vms),
    url(r'^rm_vm_from_networks/$', network_view.rm_vm_from_networks),

    url(r'^approve_single_creation/$', audit_views.approve_single_creation),
    url(r'^approve_all_creation', audit_views.approve_all_creation),
    url(r'^approve_single_delete', audit_views.approve_single_delete),
    url(r'^approve_all_delete', audit_views.approve_all_delete),
    url(r'^approve_single_nat', audit_views.approve_single_nat),
    url(r'^refuse_single_nat', audit_views.refuse_single_nat),
    url(r'^refuse_single_creation/$', audit_views.refuse_single_creation),
    url(r'^refuse_single_delete/$', audit_views.refuse_single_delete),
    url(r'^free_ports', nat_views.get_free_ports),
    url(r'^iamonline', monitor.online),
    url(r'^network_test', network_view.network_test),
    url(r'^topology_data', topology.topology_data),
    url(r'^admin/', include(admin.site.urls)),
]
