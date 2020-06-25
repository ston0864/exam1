from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('quotes', views.quotes),
    path('myaccount/<userid>', views.edit_account),
    path('logout', views.logout),
    path('add_quote', views.add_quote),
    path('user/<userid>', views.user_quotes),
    path('update/<userid>', views.update_account),
    path('add_like/<postid>', views.add_like),
    path('delete_post/<postid>', views.delete_post)
]