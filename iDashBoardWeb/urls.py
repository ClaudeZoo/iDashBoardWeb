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
from settings import CSS_DIR, JS_DIR, IMG_DIR, LIB_DIR

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Web.views.home'),
    url(r'^home/$', 'Web.views.home'),
    url(r'^apply/$', 'Web.apply_views.apply_view'),
    url(r'^audit/$', 'Web.audit_views.audit_view'),
    url(r'^myVMs', 'Web.myvms_views.my_vms_view'),
    url(r'^applications/$', 'Web.application_views.applications_view'),
    url(r'^detail/\d+/$', 'Web.detail_views.detail_view'),
    url(r'^login/$', 'Web.views.user_login'),
    url(r'^logout/$', 'Web.views.user_logout'),
    url(r'^signup/$', 'Web.views.sign_up'),
    url(r'^settings/$', 'Web.views.settings'),
    url(r'^saveUserInfo', 'Web.views.save_user_info'),
    url(r'^changePassword', 'Web.views.change_password'),
    url(r'^validateUserName', 'Web.views.validate_username'),
    url(r'^refreshHomePage/$', 'Web.vm_views.refresh_homepage'),
    url(r'^refreshSimplePage/$', 'Web.vm_views.refresh_vms'),
    url(r'^refreshSimplePageHost/$', 'Web.vm_views.refresh_hosts'),
    url(r'^get-detail/(?P<vm_id>\d+)/$', 'Web.detail_views.get_detail'),
    url(r'^helloServer/$', 'Web.info_update.hello_server'),
    url(r'^saveVMState/$', 'Web.info_update.update_info'),
    url(r'^control_vm/$', 'Web.control_vm_views.control_vm'),
    url(r'^apply_new_vm/$', 'Web.create_vm_views.apply_new_vm'),
    url(r'^apply_nat/$', 'Web.nat_views.apply_nat'),
    url(r'^delete_apply/$', 'Web.delete_vm_views.apply_delete_vm'),
    url(r'^reply_vmHost/$', 'Web.notification.handle_notification'),
    url(r'^approve_single_creation/$', 'Web.audit_views.approve_single_creation'),
    url(r'^approve_all_creation', 'Web.audit_views.approve_all_creation'),
    url(r'^approve_single_delete', 'Web.audit_views.approve_single_delete'),
    url(r'^approve_all_delete', 'Web.audit_views.approve_all_delete'),
    url(r'^approve_single_nat', 'Web.audit_views.approve_single_nat'),
    url(r'^refuse_single_nat', 'Web.audit_views.refuse_single_nat'),
    url(r'^refuse_single_creation/$', 'Web.audit_views.refuse_single_creation'),
    url(r'^refuse_single_delete/$', 'Web.audit_views.refuse_single_delete'),
    url(r'^free_ports', 'Web.nat_views.get_free_ports'),
    url(r'^css/(?P<path>.*)', 'django.views.static.serve', {'document_root': CSS_DIR}),
    url(r'^js/(?P<path>.*)', 'django.views.static.serve', {'document_root': JS_DIR}),
    url(r'^img/(?P<path>.*)', 'django.views.static.serve', {'document_root': IMG_DIR}),
    url(r'^lib/(?P<path>.*)', 'django.views.static.serve', {'document_root': LIB_DIR}),
]
