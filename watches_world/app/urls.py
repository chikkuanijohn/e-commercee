from django.urls import path
from . import views

urlpatterns=[
    path('',views.watches_world_login),
    path('shop_home',views.shop_home),
    path('logout',views.watches_world_logout),
    path('register',views.register),
    
    path('user_home',views.user_home),
    path('add_product',views.add_products),
    path('edit_product/<pid>',views.edit_product),
    path('delete_product/<pid>',views.delete_product),
    path('add_cate',views.add_category),
    path('view_bookings',views.view_bookings),
    path('about/', views.about),
    path('contact/',views.contact),
    path('booking/',views.booking),
    path('cart',views.cart),
    path('view_cart',views.view_cart),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('pro_buy/<pid>',views.pro_buy),
    


]