"""ASST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name="welcome"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout, name="log"),
    path('secretary_signup/', views.secretarysignup, name="secretarysignup"),
    path('secretaryvalidation/<str:key>/<str:decision>',
         views.secretaryvalidation, name="secretaryvalidation"),
    path('visitorvalidation/<str:key>/<str:decision>',
         views.visitorvalidation, name="visitorvalidation"),

    path('createuser/', views.createuser, name="createuser"),
    path('visitcreate/', views.visitcreate, name="visitcreate"),
    path('admincreate/', views.admincreate, name="admincreate"),
    path('postsignin/', views.postsignin, name="postsignin"),
    path('output/', views.output, name="output"),
    path('adminusers/', views.adminusers, name="adminusers"),
    path('admins/', views.admins, name="admins"),
    path('forgotpass/', views.forgotpass, name="forgotpass"),
    path('panel/', views.panel, name="panel"),
    path('shift/', views.shift, name="shift"),
    path('fcmtoken_save/', views.fcmtoken_save, name="fcmtoken_save"),
    path('firebase-messaging-sw.js', (TemplateView.as_view(template_name='firebase-messaging-sw.js',
                                                           content_type='application/javascript', )), name='firebase-messaging-sw.js'),
    path('pending_visitors/', views.pending_visitors, name="pending_visitors"),
    path('watchmancreate/', views.watchmancreate, name="watchmancreate"),
    path('watchmanpanel/', views.watchmanpanel, name="watchmanpanel"),
    path('watchmanvalidate/<str:key>/<str:decision>/',
         views.watchmanvalidate, name="watchmanvalidate"),
    path('fcmtoken_save_watchman/', views.fcmtoken_save_watchman,
         name="fcmtoken_save_watchman"),
    path('get_excel_sheet/',
         views.get_excel_sheet, name="get_excel_sheet"),
    path('report/', views.report, name="report"),
     path('firebase_config.js', (TemplateView.as_view(template_name='firebase_config.js',
                                                           content_type='application/javascript', )), name='firebase_config.js'),



]
