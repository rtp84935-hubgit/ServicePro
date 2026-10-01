"""
URL configuration for ServiceProviders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from myapp import views

urlpatterns = [
   path('login_page/',views.login_page),
   path('signupchoice/',views.signupchoice),
   path('login_post/',views.login_post),
   path('logout_page/',views.logout_page),
# ========================CUSTOMER=========================
   path('customersignup/',views.customersignup),
   path('customersignup_post/',views.customersignup_post),
   path('checkusername/',views.checkusername),
   path('customer_home/',views.customer_home),
   path('manage_customer_profile/',views.manage_customer_profile),
   path('edit_customer_profile/<id>',views.edit_customer_profile),
   path('edit_customer_profile_post/',views.edit_customer_profile_post),
   path('changepassword/',views.changepassword),
   path('changepassword_post/',views.changepassword_post),
#    path('view_replay/<id>',views.view_replay),
# =======================SERVICE PROVIDER ===========================





   path('provider_signup/',views.provider_signup),
   path('provider_signup_post/',views.provider_signup_post),
   path('provider_home/',views.provider_home),
   path('provider_profile/',views.provider_profile),
   path('provider_editprofile/',views.provider_editprofile),
   path('provider_editprofile_post/',views.provider_editprofile_post),
   path('view_providers/',views.view_providers),
   path('send_request/<id>',views.send_request),
   path('send_request_post/',views.send_request_post),
   path('request_status/',views.request_status),
   path('payment/',views.payment),
   path('view_request/',views.view_request),
   path('accept_request/<id>',views.accept_request),
   path('reject_request/<id>',views.reject_request),
   path('completed/<id>',views.completed),
   path('add_payment_amount_post/<id>',views.add_payment_amount_post),
   path('userpayment/<bid>/<amount>/',views.userpayment),
   path('raz_pay/<amount>',views.raz_pay),
   path('userpayment_post/',views.userpayment_post),
   path('forgot_password/',views.forgot_password),
   path('forgotpassword_post/',views.forgotpassword_post),
   path('send_complaint/<id>',views.send_complaint),
   path('send_complaint_post/',views.send_complaint_post),



# ================================================ADMIN=====================================

   path('admin_home/',views.admin_home),
   path('view_serviceproviders/',views.view_serviceproviders),
   path('providers_requests/',views.providers_requests),
   path('verify_provider/<id>',views.verify_provider),
   path('view_customers/',views.view_customers),
   path('view_complaints/',views.view_complaints),
   path('replay/<int:id>',views.replay),
   path('replay_post/',views.replay_post),
   path('block_provider/<id>',views.block_provider),




]
