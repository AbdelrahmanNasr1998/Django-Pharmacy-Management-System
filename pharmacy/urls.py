from . import views
from django.urls import path

urlpatterns = [
    path('pharmacy/<username>/', views.account, name='account'),
    path('pharmacy/<username>/category/', views.category, name='category'),
    path('pharmacy/<username>/category/new_category/', views.new_category, name='new_category'),
    path('pharmacy/<username>/category/update_category/<int:id>/', views.update_category, name='update_category'),
    path('pharmacy/<username>/category/delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('pharmacy/<username>/medicine/', views.medicine, name='medicine'),
    path('pharmacy/<username>/medicine/new_medicine/', views.new_medicine, name='new_medicine'),
    path('pharmacy/<username>/medicine/update_medicine/<int:id>/', views.update_medicine, name='update_medicine'),
    path('pharmacy/<username>/medicine/delete_medicine/<int:id>/', views.delete_medicine, name='delete_medicine'),
    path('pharmacy/<username>/medicine/new_payment/', views.new_payment, name='new_payment'),
    path('pharmacy/<username>/payment/', views.payment, name='payment'),
    path('pharmacy/<username>/payment/add_payment/', views.add_payment, name='add_payment'),
    path('pharmacy/<username>/payment/update_payment/<int:id>/', views.update_payment, name='update_payment'),
    path('pharmacy/<username>/payment/delete_payment/<int:id>/', views.delete_payment, name='delete_payment'),
    path('pharmacy/<username>/expiration/', views.expiration, name='expiration'),
    path('pharmacy/<username>/end_expiration/', views.end_expiration, name='end_expiration'),
    path('pharmacy/<username>/settings/', views.settings, name='settings'),
    path('pharmacy/<username>/shortcomings/', views.shortcomings, name='shortcomings'),
]
