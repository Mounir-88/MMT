from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', base_view, name='base'),
    path('register/', register, name='register'),
    path('wallet/', home_customer_wallet, name='home_customer_wallet'),
    path('newWallet', home_customer_wallet_new, name='home_customer_wallet_new'),
    path('login/', login_view, name='login'),
    path('success/', success, name='success'),
    path('cv_sent/<int:cv_id>/', cv_sent, name='cv_sent'),
    path('review-cvs/', review_cvs, name='review_cvs'),
    path('accept-cv/<int:cv_id>/', accept_cv, name='accept_cv'),
    path('reject-cv/<int:cv_id>/', reject_cv, name='reject_cv'),
    path('homeC/', home_customer, name='home_customer'),
    path('homeE/', home_employee, name='home_employee'),
    path('apply/', apply, name='apply'),
    path('logout/', logout_view, name='logout'),
    path('transfer/', transfer_view, name='transfer'),
    path('deposit/', deposit_view, name='deposit'),
    path('withdraw/', withdraw_view, name='withdraw'),
    path("chatPage/", chatPage, name="chatPage"),
    path('cv-details/<int:cv_id>/', cv_details, name='cv_details'),
    path('employees_list', employees_list, name='employees_list'),
    path('fire_employee/<int:employee_id>/', fire_employee, name='fire_employee'),
    path('data', data_view, name='data'),
    path('transaction-list/', transaction_list, name='transaction_list'),
    path('transaction/approve/<int:transaction_id>/', approve_transaction, name='approve_transaction'),
    path('transaction/decline/<int:transaction_id>/', decline_transaction, name='decline_transaction'),
    path('appointments/', appointment_list, name='appointment_list'),
    path('appointments/create/', create_appointment, name='create_appointment'),
    path('appointments/<int:appointment_id>/edit/', edit_appointment, name='edit_appointment'),
    path('appointments/<int:appointment_id>/delete/', delete_appointment, name='delete_appointment'),
]
