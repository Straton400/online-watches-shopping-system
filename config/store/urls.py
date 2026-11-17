from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product-details/', views.product_details, name='product_details'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/products/', views.admin_products, name='admin_products'),
    path('dashboard/products/add/', views.add_watch, name='add_watch'),
    path('product/<int:watch_id>/',views.product_details,name='product_details'),
    path('dashboard/products/edit/<int:watch_id>/',views.edit_watch,name='edit_watch'),

    path('dashboard/products/delete/<int:watch_id>/',views.delete_watch,name='delete_watch'),
    
    path('cart/add/<int:watch_id>/',views.add_to_cart,name='add_to_cart'),
path(
    'cart/',views.cart,name='cart'),

    path('cart/update/<int:watch_id>/',views.update_cart,name='update_cart'),

    path('cart/remove/<int:watch_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('dashboard/orders/',views.admin_orders,name='admin_orders'),

    path('dashboard/orders/<int:order_id>/',views.admin_order_details,name='admin_order_details'),

    path('dashboard/orders/<int:order_id>/update-status/',views.update_order_status,name='update_order_status'),

    path('checkout/',views.checkout,name='checkout'),
    path('order-success/<int:order_id>/',views.order_success,name='order_success'),

    path('track-order/',views.track_order,name='track_order'),

    path('track-order/results/',views.track_order_results,name='track_order_results'),

    # Display the TimeLux Watches About Us page
     path('about/', views.about, name='about'),

     
     # Display the TimeLux Watches Contact page
    path('contact/', views.contact, name='contact'),
]