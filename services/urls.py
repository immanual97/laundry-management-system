from django.urls import path
from . import views

urlpatterns = [
    path('active',views.active,name="active"),
    path('adddetails',views.adddetails,name="adddetails"),
    path('changepassword',views.changepassword,name="changepassword"),
    path('changestatus',views.changestatus,name="changestatus"),
    path('checkout',views.checkout,name="checkout"),
    path('newlaundry',views.newlaundry,name="newlaundry"),
    path('orderhistory',views.orderhistory,name="orderhistory"),
    path('profileupdate',views.profileupdate,name="profileupdate"),
    path('transaction',views.transaction,name="transaction"),
    path('adduser',views.adduser,name="adduser"),
    path('reports',views.reports,name="reports"),
    path('adddiscound',views.adddiscound,name="adddiscound"),
    path('allorders',views.allorders,name="allorders"),
    path('feedback',views.feedback,name="feedback"),
    path('vfeedback',views.vfeedback,name="vfeedback"),
    path('unpaid',views.unpaid,name="unpaid"),
    path('cdelivery',views.cdelivery,name="cdelivery")

]
